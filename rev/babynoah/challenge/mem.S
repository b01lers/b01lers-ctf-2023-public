#include "constants.h"

	.bss
	.align 8
        .global miles
miles:  .int 0
	.global stack_ptr
stack_ptr: .int 0
	.global stack
	.align 8
stack:  .fill 100,1
	.global map
	.align 8
map:    .fill MAPSIZE,1
	.global dirx
	.align 8
dirx:	.int 0
	.global diry
diry:	.int 0
	.global rows
rows:	.int 0
	.global cols
cols:	.int 0
	.global posx
posx:	.int 0
	.global posy
posy:	.int 0
	.global flag
	.align 8
flag:	.fill 64,1
.section .note.GNU-stack,"",%progbits
