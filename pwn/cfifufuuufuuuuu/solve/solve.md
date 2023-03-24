`s` contains 3 main functions: `main`, `encrypt`, and `decrypt`.
It is compiled without linking it to `libc`, so it executes all the syscalls by itself.

The first challenge is to defeat obfuscation.
In fact, `s` cannot work alone, it is designed to run controlled by `loader.pyc`.
On one hand, `loader.pyc` "debugs" (using `ptrace`) `s`.
On the other hand, `s` contains several breakpoints (`int3`), which triggers `loader.pyc`.
One function in `s` (named `scall`) contains one of these `int3` instructions.
The goal of this function is to perform system calls.
Without the help of `loader.pyc`, this function will never work correctly, since `loader.pyc` has to move values between some registers.
For this reason, it is hard to analyze and reverse `s` without taking into account how it interacts with `loader.pyc`.

The same `int3` mechanism is used in the prolog and epilog of `main`, `encrypt`, and `decrypt`.
When `loader.pyc` is triggered by those prologs and epilogs, it implements very easy CFI checks (in particular, some sort of shadow stack).
Specifically, every time a prolog is called, the saved return address is stored in a set.
Every time an epilog is called, `loader.pyc` verifies whether the saved return address is stored in the same set.

The function `encrypt` contains a trivial buffer overflow on its stack.
However, exploiting it is not easy, given the shadow stack mechanism described above.
But, as mentioned, the shadow stack is based on a set.
For this reason, it not only allows a function to return to its legitimate caller, but also to its caller's caller.

Given that the legitimate call stack is `_start --> main --> encrypt`, it is possible to use the buffer overflow in `encrypt` to return to the location in `_start` just after the `call main` instruction.
Additionally, `_start` calls `main` in a loop, so going back to `_start` will effectively restart the execution of the program.
In summary, by exploiting the buffer overflow in `encrypt`, it is possible to "restart" the execution of the program without having the shadow stack mechanism detecting any violation of the implemented CFI policy.

When the program "restarts" a specific global variable is not reset, and its value increments by 1.
This value is used as an index into a global buffer used to store temporary data.
By "restarting" the program multiple times, it is possible to increase this global index to a point in which writing into the global buffer overflows into a place where the string `/dev/urandom` is stored.
This string is used as filename to open `urandom` and obtain some random data.
This random data is normally written to `stdout`.
An attacker can control this overflow and substitute `/dev/urandom` with `./flag.txt`.
In this way, the program will eventually print out the content of `./flag.txt` (i.e., the flag) instead of random data.

 