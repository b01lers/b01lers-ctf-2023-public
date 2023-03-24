# stepper/simulator using gdb
#

from pwn import *

# memory
# offset in gdb (no aslr) is 0x555555554000
'''
0000000000004030 B miles
0000000000004034 B stack_ptr
0000000000004038 B stack
00000000000040a0 B map            stack+104
0000000000004550 B dirx           stack+1304
0000000000004554 B diry           stack+1308
0000000000004558 B rows           stack+1312
000000000000455c B cols           stack+1316
0000000000004560 B posx           stack+1320
0000000000004564 B posy
0000000000004568 B flag
'''

def readReg(r, regname):
   r.sendline( f"print ${regname}".encode() )
   in1 = r.recvuntil(b"(gdb)").split(b"\n")[0].split()[-1]
   return int(in1)

def readMem(r, addr, count):
   r.sendline( f"x/{count}x {hex(addr)}".encode() )
   in1 = r.recvuntil(b"(gdb)")
   in1 = in1.replace(b"\x1b[34m", b"")
   in1 = in1.replace(b"\x1b[m", b"")
   in1 = [ v.strip().split()[1:]  for v in in1.split(b"\n")[:-1] ]
   in1 = [ int(v, 16)  for v in sum(in1, []) ]
   return in1

def getInfo(r):
   in1 = r.recvuntil(b"(gdb)")
   if b"exited" in in1: return None
   # rax
   inst = readReg(r, "rax")
   #print(f"INST={inst} {chr(inst)}")
   # x,y
   dirx, diry, rows, cols, x, y = readMem(r, 0x555555558550, 6)
   if dirx >= 2**31: dirx -= 2**32
   if diry >= 2**31: diry -= 2**32
   # stackptr
   stackptr = readMem(r, 0x555555558034, 1)[0]
   # stack
   stack = readMem(r, 0x555555558038, (stackptr + 3) >> 2)
   stack = b"".join( [v.to_bytes(4, "little") for v in stack] )
   stack = [v for v in stack]
   #print(f"X={x} Y={y}")
   return inst, (dirx, diry, rows, cols, x,y), stackptr, stack

r = process(["gdb", "-nx", "--args", "chal", "16", "flag.txt"])
r.sendline(b"set disassembly-flavor intel")
r.sendline(b"set pagination off")

# break at the equivalent of --> in your LOCALLY RUN BINARY
'''
    1430:       f3 0f 1e fa             endbr64 
    1434:       53                      push   rbx
    1435:       48 8d 0d 64 2c 00 00    lea    rcx,[rip+0x2c64]        # 40a0 <map>
    143c:       48 83 ec 10             sub    rsp,0x10
    1440:       64 48 8b 04 25 28 00    mov    rax,QWORD PTR fs:0x28
    1447:       00 00 
    1449:       48 89 44 24 08          mov    QWORD PTR [rsp+0x8],rax
    144e:       8b 05 10 31 00 00       mov    eax,DWORD PTR [rip+0x3110]        # 4564 <map+0x4c4>
    1454:       8b 15 06 31 00 00       mov    edx,DWORD PTR [rip+0x3106]        # 4560 <map+0x4c0>
    145a:       8d 04 40                lea    eax,[rax+rax*2]
    145d:       8d 04 c2                lea    eax,[rdx+rax*8]
    1460:       48 98                   cdqe   
    1462:       0f be 1c 01             movsx  ebx,BYTE PTR [rcx+rax*1]
--> 1466:       89 d8                   mov    eax,ebx
    1468:       83 e8 21                sub    eax,0x21
'''

#r.sendline(b"b *0x555555555466")   
r.sendline(b"b *0x55555555545a")   

r.sendline(b"r")
r.recvuntil(b"Starting program:")
#r.interactive()

#             123456789012345678901234
payload1 = [b">0#!g>#<@@@@@@@@@@@@@@@@",
            b"#",
            b""]

# copy 2nd row 1-16 to first row 0-15
#             012345678901234567890123
payload2 = [b">0!###+g>>>>>>>>>#<<<AAv",
            b">#<C@EF#HI#K#MNOP#v<<<<#",
         b"^<\x12     v####-!-##<>#g^!",
            b"^       >-,##-!gp>|^+#!<",
            b"^<<<<<pg+#!#,!##-#<     ",
            b"                        ",
            b""]                     


# copy rows 7-8 to rows 0-1
#             012345678901234567890123
payload4 = [b">00!gv                  ",
            b"v    v                  ",
            b" >#<<<                 ^",
         b"\x18/>v>>#!!-####-!#+#+#+v^",
            b"##+#g|v+##!-####p,-##g<^",
            b" #+!,|>+#*g##/,p>>>>>>v^",
            b" >^>^|<<<<<<<<<<<<<<<<<^",
            b"     >#!#+#+g>>>>>>>>>>^", 
            b"3vCD#FG#I#KLMN#PQR#TU>#<",   # new row0
            b".>##!#!g,-##-#gg@:@tuvw^",   # new row1
            b""]



#payload = payload1
#payload = payload2
payload = payload4

payload = b"\n".join(payload)

r.sendline(payload)

#r.interactive()

Nshow = 50
iter = 0
while True:
   iter += 1
   info = getInfo(r)
   if info == None:  break
   inst, (dirx,diry,rows,cols,x,y), stackptr, stack  = info
   stackShown = " ".join( [hex(v)[2:].rjust(2, "0") for v in stack[max(0, stackptr - Nshow):stackptr] ] )
   print(f"{iter}: X={x}/{cols}/{dirx} Y={y}/{rows}/{diry} INST={inst} {chr(inst)} STACK=[{stackptr}] {stackShown}")
   #if iter == 4411:  r.interactive()
   r.sendline(b"conti")

