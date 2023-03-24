	.file	"chal.c"
	.text
	.section	.rodata.str1.8,"aMS",@progbits,1
	.align 8
.LC0:
	.string	"(7) load pi    (8) load e     (9) show\n(4) add        (5) subtract   (6) multiply\n(1) push       (2) pop        (3) swap\n               (q) quit\n"
	.text
	.p2align 4
	.globl	menu
	.type	menu, @function
menu:
.LFB23:
	.cfi_startproc
	endbr64
	subq	$24, %rsp
	.cfi_def_cfa_offset 32
	movq	%fs:40, %rax
	movq	%rax, 8(%rsp)
	xorl	%eax, %eax
	movq	8(%rsp), %rax
	xorq	%fs:40, %rax
	jne	.L6
	leaq	.LC0(%rip), %rdi
	addq	$24, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 8
	jmp	puts@PLT
.L6:
	.cfi_restore_state
	call	__stack_chk_fail@PLT
	.cfi_endproc
.LFE23:
	.size	menu, .-menu
	.p2align 4
	.globl	readChar
	.type	readChar, @function
readChar:
.LFB24:
	.cfi_startproc
	endbr64
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset 3, -16
	subq	$16, %rsp
	.cfi_def_cfa_offset 32
	movq	stdin(%rip), %rdi
	movq	%fs:40, %rax
	movq	%rax, 8(%rsp)
	xorl	%eax, %eax
	call	getc@PLT
	movl	%eax, %ebx
	.p2align 4,,10
	.p2align 3
.L8:
	movq	stdin(%rip), %rdi
	call	getc@PLT
	cmpl	$10, %eax
	jne	.L8
	movq	8(%rsp), %rax
	xorq	%fs:40, %rax
	jne	.L12
	addq	$16, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 16
	movl	%ebx, %eax
	popq	%rbx
	.cfi_def_cfa_offset 8
	ret
.L12:
	.cfi_restore_state
	call	__stack_chk_fail@PLT
	.cfi_endproc
.LFE24:
	.size	readChar, .-readChar
	.p2align 4
	.globl	findTail
	.type	findTail, @function
findTail:
.LFB25:
	.cfi_startproc
	endbr64
	subq	$24, %rsp
	.cfi_def_cfa_offset 32
	pxor	%xmm0, %xmm0
	movq	%fs:40, %rax
	movq	%rax, 8(%rsp)
	xorl	%eax, %eax
	jmp	.L14
	.p2align 4,,10
	.p2align 3
.L16:
	addl	$1, %eax
	cmpb	$-128, %al
	je	.L15
.L14:
	movsbq	%al, %rdx
	ucomisd	(%rdi,%rdx,8), %xmm0
	jp	.L16
	jne	.L16
.L15:
	movq	8(%rsp), %rcx
	xorq	%fs:40, %rcx
	movsbl	%al, %eax
	jne	.L22
	addq	$24, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 8
	ret
.L22:
	.cfi_restore_state
	call	__stack_chk_fail@PLT
	.cfi_endproc
.LFE25:
	.size	findTail, .-findTail
	.section	.rodata.str1.8
	.align 8
.LC2:
	.string	"==============================================================\n== B01lers Calculator - Transcendental Figures edition 2023 ==\n==============================================================\n"
	.section	.rodata.str1.1,"aMS",@progbits,1
.LC3:
	.string	"choice: "
.LC6:
	.string	"idx: "
.LC7:
	.string	"-> value is %g\n\n"
	.section	.text.startup,"ax",@progbits
	.p2align 4
	.globl	main
	.type	main, @function
main:
.LFB26:
	.cfi_startproc
	endbr64
	pushq	%r12
	.cfi_def_cfa_offset 16
	.cfi_offset 12, -16
	leaq	.LC2(%rip), %rdi
	pushq	%rbp
	.cfi_def_cfa_offset 24
	.cfi_offset 6, -24
	leaq	.LC6(%rip), %rbp
	pushq	%rbx
	.cfi_def_cfa_offset 32
	.cfi_offset 3, -32
	leaq	.LC3(%rip), %rbx
	subq	$96, %rsp
	.cfi_def_cfa_offset 128
	movq	%fs:40, %rax
	movq	%rax, 88(%rsp)
	xorl	%eax, %eax
	movq	%rsp, %r12
	call	puts@PLT
	movl	$11, %ecx
	xorl	%eax, %eax
	movq	%r12, %rdi
	rep stosq
	.p2align 4,,10
	.p2align 3
.L24:
	xorl	%eax, %eax
	call	menu
	.p2align 4,,10
	.p2align 3
.L46:
	movq	%rbx, %rsi
	movl	$1, %edi
	xorl	%eax, %eax
	call	__printf_chk@PLT
	movq	stdout(%rip), %rdi
	call	fflush@PLT
	xorl	%eax, %eax
	call	readChar
	cmpb	$113, %al
	je	.L51
	cmpb	$10, %al
	je	.L46
	cmpb	$55, %al
	je	.L52
	cmpb	$56, %al
	je	.L53
	cmpb	$52, %al
	je	.L54
	cmpb	$53, %al
	je	.L55
	cmpb	$54, %al
	je	.L56
	cmpb	$49, %al
	je	.L57
	cmpb	$50, %al
	je	.L58
	cmpb	$51, %al
	je	.L59
	cmpb	$57, %al
	jne	.L46
	.p2align 4,,10
	.p2align 3
.L39:
	movq	%rbp, %rsi
	movl	$1, %edi
	xorl	%eax, %eax
	call	__printf_chk@PLT
	movq	stdout(%rip), %rdi
	call	fflush@PLT
	xorl	%eax, %eax
	call	readChar
	movsbl	%al, %eax
	subl	$48, %eax
	cmpl	$9, %eax
	jg	.L39
	cltq
	leaq	.LC7(%rip), %rsi
	movl	$1, %edi
	movsd	(%rsp,%rax,8), %xmm0
	movl	$1, %eax
	call	__printf_chk@PLT
	jmp	.L24
	.p2align 4,,10
	.p2align 3
.L51:
	movq	88(%rsp), %rax
	xorq	%fs:40, %rax
	jne	.L60
	addq	$96, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 32
	xorl	%eax, %eax
	popq	%rbx
	.cfi_def_cfa_offset 24
	popq	%rbp
	.cfi_def_cfa_offset 16
	popq	%r12
	.cfi_def_cfa_offset 8
	ret
	.p2align 4,,10
	.p2align 3
.L52:
	.cfi_restore_state
	movq	.LC4(%rip), %rax
	movq	%rax, (%rsp)
	jmp	.L24
	.p2align 4,,10
	.p2align 3
.L53:
	movq	.LC5(%rip), %rax
	movq	%rax, (%rsp)
	jmp	.L24
	.p2align 4,,10
	.p2align 3
.L54:
	movsd	(%rsp), %xmm0
	addsd	8(%rsp), %xmm0
	movsd	%xmm0, (%rsp)
	jmp	.L24
	.p2align 4,,10
	.p2align 3
.L55:
	movsd	(%rsp), %xmm0
	subsd	8(%rsp), %xmm0
	movsd	%xmm0, (%rsp)
	jmp	.L24
	.p2align 4,,10
	.p2align 3
.L56:
	movsd	(%rsp), %xmm0
	mulsd	8(%rsp), %xmm0
	movsd	%xmm0, (%rsp)
	jmp	.L24
	.p2align 4,,10
	.p2align 3
.L57:
	movq	%r12, %rdi
	call	findTail
	movl	%eax, %edx
	testb	%al, %al
	je	.L34
	.p2align 4,,10
	.p2align 3
.L35:
	movsbq	%dl, %rax
	leal	-1(%rax), %ecx
	movslq	%ecx, %rcx
	movsd	(%rsp,%rcx,8), %xmm0
	movsd	%xmm0, (%rsp,%rax,8)
	subb	$1, %dl
	jne	.L35
.L34:
	movq	$0x000000000, (%rsp)
	jmp	.L24
	.p2align 4,,10
	.p2align 3
.L58:
	movq	%r12, %rdi
	call	findTail
	testl	%eax, %eax
	je	.L24
	subl	$1, %eax
	leaq	8(%rsp), %rsi
	movq	%r12, %rdi
	leaq	8(,%rax,8), %rdx
	call	memmove@PLT
	jmp	.L24
	.p2align 4,,10
	.p2align 3
.L59:
	movapd	(%rsp), %xmm0
	shufpd	$1, %xmm0, %xmm0
	movaps	%xmm0, (%rsp)
	jmp	.L24
.L60:
	call	__stack_chk_fail@PLT
	.cfi_endproc
.LFE26:
	.size	main, .-main
	.section	.rodata.cst8,"aM",@progbits,8
	.align 8
.LC4:
	.long	1413754136
	.long	1074340347
	.align 8
.LC5:
	.long	2333366121
	.long	1074118410
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	 1f - 0f
	.long	 4f - 1f
	.long	 5
0:
	.string	 "GNU"
1:
	.align 8
	.long	 0xc0000002
	.long	 3f - 2f
2:
	.long	 0x3
3:
	.align 8
4:
