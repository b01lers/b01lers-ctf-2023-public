use crate::arch::x64::*;

pub(super) const PICM_COMMAND: u16 = 0x20;
const PICM_DATA: u16 = 0x21;

pub(super) const PICS_COMMAND: u16 = 0xa0;
const PICS_DATA: u16 = 0xa1;

// code to tell pic to send more interrupts
pub(super) const PIC_EOI: u8 = 0x20;

// from osdev wiki
const ICW1_ICW4: u8 = 0x01; /* ICW4 (not) needed */
const ICW1_SINGLE: u8 = 0x02; /* Single (cascade) mode */
const ICW1_INTERVAL4: u8 = 0x04; /* Call address interval 4 (8) */
const ICW1_LEVEL: u8 = 0x08; /* Level triggered (edge) mode */
const ICW1_INIT: u8 = 0x10; /* Initialization - required! */

const ICW4_8086: u8 = 0x01; /* 8086/88 (MCS-80/85) mode */
const ICW4_AUTO: u8 = 0x02; /* Auto (normal) EOI */
const ICW4_BUF_SLAVE: u8 = 0x08; /* Buffered mode/slave */
const ICW4_BUF_MASTER: u8 = 0x0c; /* Buffered mode/master */
const ICW4_SFNM: u8 = 0x10; /* Special fully nested (not) */

// offsets of pics when enabled
pub const PICM_OFFSET: u8 = 32;
pub const PICS_OFFSET: u8 = 40;

// offsets of pics when disabled
const PICM_DISABLE_OFFSET: u8 = 0xf8;
const PICS_DISABLE_OFFSET: u8 = 0xf8;

// from osdev wiki
// offsets must be multiple of 8
pub fn remap(moffset: u8, soffset: u8) {
    // save masks
    let s1 = inb(PICM_DATA);
    let s2 = inb(PICS_DATA);

    // tell pics its time to remap
    outb(PICM_COMMAND, ICW1_INIT | ICW1_ICW4);
    outb(PICS_COMMAND, ICW1_INIT | ICW1_ICW4);

    // tell them offset
    outb(PICM_DATA, moffset);
    outb(PICS_DATA, soffset);

    // tell master pic it has slave pic chained at pin 2
    outb(PICM_DATA, 0b100);
    outb(PICS_DATA, 0b10);

    outb(PICM_DATA, ICW4_8086);
    outb(PICS_DATA, ICW4_8086);

    // restore masks from earlier
    outb(PICM_DATA, s1);
    outb(PICS_DATA, s2);
}

/// send EOI
pub fn eoi(secondary_pic: bool) {
    if secondary_pic {
        outb(PICS_COMMAND, PIC_EOI);
    }
    
    outb(PICM_COMMAND, PIC_EOI);
}

// disable the pic
pub fn disable() {
    // need to remap it to higher interrupt number so spurious interrupts dont cause problems
    remap(PICM_DISABLE_OFFSET, PICS_DISABLE_OFFSET);
    // mask all incoming interrupts, spurious interrupts might still occur
    outb(PICM_DATA, 0xff);
    outb(PICS_DATA, 0xff);
}
