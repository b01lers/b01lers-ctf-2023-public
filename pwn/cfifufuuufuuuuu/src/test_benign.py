import struct
import subprocess


p = subprocess.Popen(["python3", "./loader.pyc"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)

for i in range(31):
	"1",p.stdout.read(1)


tstr = b"A"*16
p.stdin.write(tstr)
p.stdin.flush()

for i in range(11):
	i,p.stdout.read(1)

kk = b""
for i in range(16):
	kk += p.stdout.read(1)

for i in range(22):
	i,p.stdout.read(1)

ss = b""
for i in range(16):
	ss += p.stdout.read(1)

for i in range(23):
	i,p.stdout.read(1)

p.stdin.write(ss)
p.stdin.flush()

p.stdin.write(kk+b"\n")
p.stdin.flush()

for i in range(33):
	i,p.stdout.read(1)

rr = b""
for i in range(50):
	rr += p.stdout.read(1)
print(rr, tstr)
assert rr[:15] == tstr[:15]
