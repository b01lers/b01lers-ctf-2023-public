import struct
import sys
import socket



if len(sys.argv) != 3:
    print("Usage: python3 ./test_all.py <IP> <PORT>")
    sys.exit(1)



print("BENIGN")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((sys.argv[1], int(sys.argv[2])))

for i in range(31):
	s.recv(1)

tstr = b"A"*16
s.sendall(tstr)

for i in range(11):
	s.recv(1)

kk = b""
for i in range(16):
	kk += s.recv(1)

for i in range(22):
	s.recv(1)

ss = b""
for i in range(16):
	ss += s.recv(1)

for i in range(23):
	s.recv(1)

s.sendall(ss)
s.sendall(kk+b"\n")

for i in range(33):
	s.recv(1)

rr = b""
for i in range(50):
	rr += s.recv(1)
print(rr, tstr)
assert rr[:15] == tstr[:15]



print("EXPLOITFAIL")
with open("../src/input_exploitfail", "rb") as fp:
    cc = fp.read()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((sys.argv[1], int(sys.argv[2])))
s.sendall(cc)

buf = b""
while True:
    t = s.recv(1)
    if len(t) == 0:
        break
    buf += t
    if b"!!!\n" in buf:
        break

print(buf)
assert b"\n!!!Stack Violation Detected!!!\n" in buf
s.close()



print("EXPLOIT")
with open("input_exploit", "rb") as fp:
    cc = fp.read()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((sys.argv[1], int(sys.argv[2])))
s.sendall(cc)

buf = b""
while True:
    t = s.recv(1)
    if len(t) == 0:
        break
    buf += t
    if b"bctf{a&X98k_FU!}\n" in buf:
        break

print(buf)
assert b"bctf{a&X98k_FU!}" in buf

p1 = buf.split(b"bctf{")[1]
p2 = p1.split(b"}")[0]
flag = b"bctf{"+p2+b"}"

print("FLAG:", flag)
s.close()
