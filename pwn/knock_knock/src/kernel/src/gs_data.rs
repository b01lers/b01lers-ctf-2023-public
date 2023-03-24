use core::sync::atomic::{AtomicUsize, Ordering};

use crate::prelude::*;
use crate::arch::x64::{gs_addr, wrmsr, GSBASEK_MSR, GSBASE_MSR};

/// This is cpu local data stored pointed to by the GS_BASE msr
/// Used for things like finding the kernel stack from a syscall and cpu local scheduler data
#[repr(C)]
#[derive(Debug)]
pub struct GsData {
    /// This contains the address of this gsdata struct itself
    /// 
    /// We need this because lea doesn't work with the gs register,
    /// so the assembly looks at this field and returns the pointer to the rust code
    pub self_addr: AtomicUsize,
    /// This is the kernel rsp that will be loaded whenever a syscall is made
    /// 
    /// This is switched when switching to a different thread
    pub syscall_rsp: AtomicUsize,
}

impl GsData {
    pub fn set_self_addr(&self) {
        self.self_addr.store((self as *const _) as _, Ordering::Release);
    }
}

/// Sets the current cpu's local data
pub fn init() {
    let gs_data = GsData {
        self_addr: AtomicUsize::new(0),
        syscall_rsp: AtomicUsize::new(0),
    };

    let gs_data = Box::new(gs_data);
    gs_data.set_self_addr();

    let ptr = Box::into_raw(gs_data) as *mut _;
    
    wrmsr(GSBASE_MSR, ptr as u64);
    wrmsr(GSBASEK_MSR, ptr as u64);
}

/// Gets the current cpu's local data
pub fn cpu_local_data() -> &'static GsData {
    unsafe { (gs_addr() as *const GsData).as_ref().unwrap() }
}