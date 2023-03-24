//! Utility for iterating over arrays with different tag types that are commonly provided by multipboot and acpi

use core::iter::FusedIterator;
use core::marker::PhantomData;
use core::mem::size_of_val;

use crate::prelude::*;

pub trait HwaTag {
    type Elem<'a>: core::fmt::Debug
    where
        Self: 'a;

    // returns the size of the element, including the tag
    fn size(&self) -> usize;
    fn elem<'a>(&'a self) -> Self::Elem<'a>;

    // convinience function to get internal data
    unsafe fn raw_data<T>(&self) -> &T {
        assert!(size_of_val(self) + size_of::<T>() <= self.size());
        let addr = (self as *const Self as *const u8 as usize) + size_of_val(self);
        unsafe { (addr as *const T).as_ref().unwrap() }
    }

    // convinience function to get internal data and header
    unsafe fn raw_hd<T>(&self) -> &T {
        assert!(size_of::<T>() <= self.size());
        unsafe { (self as *const _ as *const T).as_ref().unwrap() }
    }
}

/// Hardware array iterator
/// Iterates over arrays of different sized elements with different type elements
pub struct HwaIter<'a, T: HwaTag> {
    // start address of elements
    addr: usize,
    // end address of elements
    end: usize,
    //  required alignment of elements
    align: usize,
    phantom: PhantomData<&'a T>,
}

impl<T: HwaTag> HwaIter<'_, T> {
    pub unsafe fn from(addr: usize, size: usize) -> Self {
        unsafe { Self::from_align(addr, size, 0) }
    }

    pub unsafe fn from_align(addr: usize, size: usize, align: usize) -> Self {
        HwaIter::<T> {
            addr,
            end: addr + size,
            align,
            phantom: PhantomData,
        }
    }

    pub unsafe fn from_struct<U>(data: &U, total_size: usize) -> Self {
        unsafe { Self::from_struct_align(data, total_size, 0) }
    }

    // makes an iterator starteing after data, with size total_size - size_of::<T>()
    pub unsafe fn from_struct_align<U>(data: &U, total_size: usize, align: usize) -> Self {
        assert!(size_of::<U>() <= total_size);
        let addr = (data as *const _ as usize) + size_of::<U>();
        let size = total_size - size_of::<U>();
        unsafe { Self::from_align(addr, size, align) }
    }
}

impl<'a, T: HwaTag> Iterator for HwaIter<'a, T> {
    type Item = T::Elem<'a>;

    fn next(&mut self) -> Option<Self::Item> {
        if self.addr >= self.end {
            None
        } else {
            let tag = unsafe { (self.addr as *const T).as_ref().unwrap() };

            self.addr += tag.size();
            if self.addr > self.end {
                return None;
            }

            if self.align != 0 {
                self.addr = align_up(self.addr, self.align);
            }

            Some(tag.elem())
        }
    }
}

impl<T: HwaTag> FusedIterator for HwaIter<'_, T> {}
