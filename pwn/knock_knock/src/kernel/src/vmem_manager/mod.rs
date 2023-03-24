//! This has all the functions that have to do with mappind physical memory into virtual memory

use bitflags::bitflags;
use lazy_static::lazy_static;
use spin::Lazy;

use crate::arch::x64::invlpg;
use crate::mem::PhysFrame;
use crate::mem::VirtFrame;
use crate::prelude::*;
use crate::consts;
use crate::arch::x64::set_cr3;
use crate::sync::IMutex;
use page_table::{PageTable, PageTablePointer};

use self::page_table::PageTableFlags;

mod page_table;

lazy_static! {
	static ref HIGHER_HALF_PAGE_POINTER: PageTablePointer = PageTablePointer::new(*consts::KZONE_PAGE_TABLE_POINTER,
		PageTableFlags::PRESENT | PageTableFlags::WRITABLE | PageTableFlags::GLOBAL);
    
    /// Most permissive page table flags used by parent tables
    static ref PARENT_FLAGS: PageTableFlags = PageTableFlags::PRESENT | PageTableFlags::WRITABLE | PageTableFlags::USER;
}

bitflags! {
    /// Flags that represent properties of the memory we want to map
	pub struct PageMappingFlags: usize {
		const NONE =		0;
		const READ =		1;
		const WRITE =		1 << 1;
		const EXEC =		1 << 2;
		const USER = 		1 << 3;
	}
}

impl PageMappingFlags {
    /// Returns true if these page mapping flags specift memory that will actually exist in the address space
    fn exists(&self) -> bool {
		self.intersects(PageMappingFlags::READ | PageMappingFlags::WRITE | PageMappingFlags::EXEC)
	}
}

/// Use to take a large as possible page size for use with huge pages
struct PageMappingTaker {
    virt_range: AVirtRange,
    phys_range: APhysRange,
}

impl PageMappingTaker {
    fn take(&mut self) -> Option<(PhysFrame, VirtFrame)> {
        let take_size = core::cmp::min(
            self.phys_range.get_take_size()?,
            self.virt_range.get_take_size()?,
        );

        Some((
            self.phys_range.take(take_size)?,
            self.virt_range.take(take_size)?,
        ))
    }
}

/// This represents a virtual address space that can have memory mapped into it
#[derive(Debug)]
pub struct VirtAddrSpace {
    /// All virtual memory which is currently in use
    // TODO: write btreemap for this, it will be faster with many zones
    mem_zones: Vec<(AVirtRange, PhysAddr)>,
    /// Page table pointer which will go in the cr3 register, it points to the pml4 table
    cr3: PageTablePointer,
}

impl VirtAddrSpace {
    pub fn new() -> KResult<Self> {
        let mut pml4_table = PageTable::new(PageTableFlags::NONE)
            .ok_or(SysErr::OutOfMem)?;

        unsafe {
            pml4_table.as_mut_ptr()
                .as_mut()
                .unwrap()
                .add_entry(511, *HIGHER_HALF_PAGE_POINTER);
        }

        Ok(VirtAddrSpace {
            mem_zones: Vec::new(),
            cr3: pml4_table,
        })
    }

    pub fn cr3_addr(&self) -> PhysAddr {
        self.cr3.address()
    }

    /// Deallocates all the page tables in this address space
    /// 
    /// Call this before dropping the address space otherwise there will be a memory leak
    /// 
    /// # Safety
    /// 
    /// This address space must not be loaded when this is called
    pub unsafe fn dealloc_addr_space(&mut self) {
        unsafe {
            self.cr3.as_mut_ptr().as_mut().unwrap()
                .dealloc_all()
        }
    }

    /// Maps all the virtual memory ranges in the slice to point to the corresponding physical address
    /// 
    /// If any one of the memeory regions fails, none will be mapped
    pub fn map_memory(&mut self, virt_range: AVirtRange,  phys_addr: PhysAddr, flags: PageMappingFlags) -> KResult<()> {
        self.add_virt_addr_entry(virt_range, phys_addr)?;

        let phys_range = APhysRange::new(phys_addr, virt_range.size());

        let mut frame_taker = PageMappingTaker {
            virt_range,
            phys_range,
        };

        while let Some((phys_frame, virt_frame)) = frame_taker.take() {
            self.map_frame(virt_frame, phys_frame, flags);

            invlpg(virt_frame.start_addr().as_usize());
        }

        Ok(())
    }

    /// Unmaps all the virtual memory ranges in the slice
    /// 
    /// Phys addr must be the same memory it was mapped with
    /// 
    /// If any one of the memeory regions fails, none will be unmapped
    // FIXME: don't require phys addr to be passed in
    pub fn unmap_memory(&mut self, virt_range: AVirtRange) -> KResult<PhysAddr> {
        let phys_addr = self.remove_virt_addr_entry(virt_range)?;

        self.unmap_internal(virt_range, phys_addr);

        Ok(phys_addr)
    }

    /// Returns Some(index) if the given virt range in the virtual address space is not occupied
    /// 
    /// The index is the place where the virt_range can be inserted to maintain ordering in the list
    fn virt_range_unoccupied(&self, virt_range: AVirtRange) -> Option<usize> {
        // can't map anything beyond the kernel region
        if virt_range.end_usize() > *consts::KERNEL_VMA {
            return None;
        }

        match self.mem_zones.binary_search_by_key(&virt_range.addr(), |(virt_range, _)| virt_range.addr()) {
            // If we find the address it is occupied
            Ok(_) => None,
            Err(index) => {
                if (index == 0 || self.mem_zones[index - 1].0.end_addr() <= virt_range.addr())
                    && (index == self.mem_zones.len() || virt_range.end_addr() <= self.mem_zones[index].0.addr()) {
                    Some(index)
                } else {
                    None
                }
            },
        }
    }

    // this takes in a slice with the phys addrs as well because that is what map_memory takes in
    // CHALL FIXME: no need to handle oom here
    fn add_virt_addr_entry(&mut self, virt_range: AVirtRange, phys_addr: PhysAddr) -> KResult<()> {
        let index = self.virt_range_unoccupied(virt_range)
            .ok_or(SysErr::InvlMemZone)?;
        self.mem_zones.insert(index, (virt_range, phys_addr));
        
        Ok(())
    }

    fn remove_virt_addr_entry(&mut self, virt_range: AVirtRange) -> KResult<PhysAddr> {
        let index = self.mem_zones
            .binary_search_by_key(&virt_range.addr(), |(virt_range, _)| virt_range.addr())
            .or(Err(SysErr::InvlMemZone))?;

        let (_, phys_addr) = self.mem_zones.remove(index);

        Ok(phys_addr)
    }

    fn map_frame(&mut self, virt_frame: VirtFrame, phys_frame: PhysFrame, flags: PageMappingFlags) {
        let virt_addr = virt_frame.start_addr().as_usize();
        let page_table_indicies = [
            get_bits(virt_addr, 39..48),
			get_bits(virt_addr, 30..39),
			get_bits(virt_addr, 21..30),
			get_bits(virt_addr, 12..21),
        ];

        let (depth, huge_flag) = match virt_frame {
            VirtFrame::K4(_) => (4, PageTableFlags::NONE),
            VirtFrame::M2(_) => (3, PageTableFlags::HUGE),
            VirtFrame::G1(_) => (2, PageTableFlags::HUGE),
        };

        let mut page_table = unsafe {
            self.cr3.as_mut_ptr().as_mut().unwrap()
        };

        for level in 0..depth {
            let index = page_table_indicies[level];

            if level == depth - 1 {
                let flags = PageTableFlags::PRESENT | huge_flag | flags.into();
                page_table.add_entry(index, PageTablePointer::new(phys_frame.start_addr(), flags));
            } else {
                page_table = page_table
                    .get_or_alloc(index, *PARENT_FLAGS)
                    .expect("virtual memory mapper: out of memory");
            }
        }
    }

    /// Unmaps the given virtual memory frame
    /// 
    /// This function still works even if the frame isn't fully mapped, it will try and remove and partially mapped parent tables
    fn unmap_frame(&mut self, virt_frame: VirtFrame) {
        let virt_addr = virt_frame.start_addr().as_usize();
        let page_table_indicies = [
            get_bits(virt_addr, 39..48),
			get_bits(virt_addr, 30..39),
			get_bits(virt_addr, 21..30),
			get_bits(virt_addr, 12..21),
        ];

        let depth = match virt_frame {
            VirtFrame::K4(_) => 4,
            VirtFrame::M2(_) => 3,
            VirtFrame::G1(_) => 2,
        };

        let mut tables = [self.cr3.as_mut_ptr(), null_mut(), null_mut(), null_mut()];

        for a in 1..depth {
            unsafe {
                tables[a] = if let Some(page_table) = tables[a - 1].as_mut() {
                    page_table.get(page_table_indicies[a - 1])
                } else {
                    break
                };
            }
        }

        // the index of the first entry in tables that needs to be deallocated
        let mut dealloc_start_index = depth;

        for i in (0..depth).rev() {
            let current_table = unsafe {
                if let Some(table) = tables[i].as_mut() {
                    table
                } else {
                    continue;
                }
            };

            current_table.remove(page_table_indicies[i]);

            if i != 0 && current_table.entry_count() == 0 {
                dealloc_start_index = depth;
            } else {
                // don't continue removing this page table unless we have deallocated this table 
                break;
            }
        }

        // dealloc these in a later pass after all indexes are removed
        for i in dealloc_start_index..depth {
            unsafe {
                if let Some(table) = tables[i].as_mut() {
                    table.dealloc()
                } else {
                    break;
                }
            }
        }
    }

    fn unmap_internal(&mut self, virt_range: AVirtRange, phys_addr: PhysAddr) {
        let phys_range = APhysRange::new(phys_addr, virt_range.size());

        let mut frame_taker = PageMappingTaker {
            virt_range,
            phys_range,
        };

        while let Some((_, virt_frame)) = frame_taker.take() {
            self.unmap_frame(virt_frame);

            // TODO: check if address space is loaded
            invlpg(virt_frame.start_addr().as_usize());
        }
    }
}

pub static ADDR_SPACE: Lazy<IMutex<VirtAddrSpace>> = Lazy::new(
    || IMutex::new(VirtAddrSpace::new().expect("could not initialize virtual address space"))
);

pub fn init() {
    set_cr3(ADDR_SPACE.lock().cr3_addr().as_usize());
}