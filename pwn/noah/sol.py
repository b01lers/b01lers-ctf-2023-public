# usage:
#
#    python3 sol.py     -> normal solver
#    python3 sol.py 1   -> golf solver


from pwn import *
import time
import sys


# memory offsets
'''
0000000000004030 B miles
0000000000004034 B stack_ptr
0000000000004038 B stack
00000000000040a0 B map            stack+104  
0000000000004550 B dirx           stack+1304 = map[0,50] = map[0,0] + 1200
0000000000004554 B diry           stack+1308
0000000000004558 B rows           stack+1312
000000000000455c B cols           stack+1316
0000000000004560 B posx           stack+1320
0000000000004564 B posy           stack+1324
0000000000004568 B flag           stack+1328 = map[0,51] = map[0,0] + 1224
                   flag+64        stack+1392 = map[16,53]
'''


def getOne(pos, GOLF = False, LOCAL = False):
   r = process(["chal", "20", "./flag.txt"])  if LOCAL  else  remote("127.0.0.1", 9103)

   if not LOCAL:
      r.recvuntil(b">")
      choice = 2  if GOLF  else  1
      r.sendline(f"{choice}".encode())
   r.recvuntil(b"voyage:")

   x = (pos + 1224) % 0x18
   y = (pos + 1224) // 0x18
   print(f"x={x} y={y}")

   # my standard solver, uses 10 rows
   #
   # copy rows 8-9 to rows 0-1, then execute
   #
   #             012345678901234567890123
   payload10 = [
              b">00!gv                  ",
              b"v    v                  ",
              b" >#<<<                 ^",
           b"\x18/>v>>#!!-####-!#+#+#+v^",
              b"##+#g|v+##!-####p,-##g<^",
              b" #+!,|>+#*g##/,p>>>>>>v^",
              b" >^>^|<<<<<<<<<<<<<<<<<^",
              b"     >#!#+#+g>>>>>>>>>>^", 
              b"AvCD#FG#I#KLMN#PQR#TU>#<",   # new row0
              b"a>##!#!g,-##-#gg:@stuvw^",   # new row1
              b""]


   # solver golfed down to 9 rows
   #
   # copy rows 8-7 to rows 0-1, then execute
   #
   #             012345678901234567890123
   payload9 = [
              b">00!gv                  ",
              b"v  v<<                  ",
              b" >#<     >-####-!#+#+#v^",
           b"\x18/>v>>#!!^v####p,-##g+<^",
              b"##+#g|    >-!#+#+#+#!!v^",
              b" #+!,|<<<<<<<<<p,/##g-<^",
              b" >^>^>#!#+#+g>>>>>>>>>>^",
              b"a>##!#!g,-##-#gg:@stuvw^",   # new row1
              b"AvCD#FG#I#KLMN#PQR#TU>#<",   # new row0
              b""]
   
   payload = payload9  if GOLF   else   payload10
      
   payload = b"\n".join(payload)
   payload = payload.replace(b"a", bytes([x + 0x23]))
   payload = payload.replace(b"A", bytes([y]))

   #print(payload)
   r.sendline(payload)

   while True:
      in1 = r.recvuntil(b"\n")
      #print(in1)
      if b"perished" in in1 or b"journeyed" in in1:  break
   r.close()
   print(in1)
   if b"far" in in1:
      ch = int(in1.split(b"thou")[0])
      miles = int( in1.split(b"(")[1].split()[0] )
      print(f"CH={ch} MILES={hex(miles)}")
   else:  ch = None
   return ch



GOLF = len(sys.argv) > 1

flag = []
while True:
   #ch = getOne(len(flag), GOLF, True)
   ch = getOne(len(flag), GOLF, False)
   if ch == None: break
   flag.append(ch)
   time.sleep(0.2)
   print(f"FLAG: {bytes(flag)}")
   if ch == ord("}"): break
