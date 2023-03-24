# Knock Knock

The idt has the cpl set to 3, which mans userspace code can use the int instruction to trigger interrupts for all interrupt handlers.

Some interrupts on x86, like page fault, generate an error code which is pushed on the stack after saved rip, rsp, rflags, cs, and ss.

However, when these same interrupts are generated with the int instruction, an error code is not pushed.
This can cause a misalignmant of the stack for interrupt handlers that expect an error code.

Normally, this is hard to exploit, since the saved rflags is interpreted as a saved cs register, and because rflags
interrupt bit will always be set, as well as several reserved bits, it is hard to make a valid kernel cs.

However, the interrupt handlers that expect an error code always set cs to 0x23, and ss to 0x1b, which are the values for userspace code.
This means a value can be written beyond the bottom of the stack.

This can be used to corrupt the next pointer of the simple freelist that keeps track of allocated pages.

Using this corruption, you can allocate a thread which has its kernel stack in userspace memory,
and ovewrite a return address from a different thread after issuing a syscall, which can lead to arbritrary code execution.