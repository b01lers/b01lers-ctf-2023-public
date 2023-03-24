use crate::linked_list::LinkedList;
use super::thread::Thread;
use crate::mem::MemOwner;
use crate::sync::IMutex;
use crate::prelude::*;

/// This stores all currently non running threads
#[derive(Debug)]
pub struct ThreadMap {
    ready_threads: IMutex<LinkedList<Thread>>,
}

impl ThreadMap {
    pub const fn new() -> Self {
        ThreadMap {
            ready_threads: IMutex::new(LinkedList::new()),
        }
    }

    /// Gets the next thread to run
    /// 
    /// Returns `None` if there are no available threads to run
    pub fn get_ready_thread(&self) -> Option<MemOwner<Thread>> {
        self.ready_threads.lock().pop_front()
    }

    /// Adds `thread_handle` to the list of ready threads
    pub fn insert_ready_thread(&self, thread_handle: MemOwner<Thread>) {
        self.ready_threads.lock().push(thread_handle);
    }
}

unsafe impl Send for ThreadMap {}
unsafe impl Sync for ThreadMap {}