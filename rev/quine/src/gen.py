import string
import random
import functools
from pwn import xor


flag = open("../solve/flag.txt").read()
print(flag)
print(len(flag))

# Generate key checking constants
valid_chars = [i for i in string.printable[:-6] if i not in ['"',"\\","%","!","~","|"]]
print(valid_chars)
valid_chars = list(map(ord, valid_chars))

key1 = []
key2 = []
key3 = []
key4 = []

for ch in flag:
    while True:
        ch1, ch2, ch3 = random.sample(valid_chars, 3) 
        if (ord(ch) - ch1 + ch2) ^ ch3 in valid_chars:
            key1.append(ch1)
            key2.append(ch2)
            key3.append(ch3)
            key4.append((ord(ch) - ch1 + ch2) ^ ch3)
            break

print(len(key1+key2+key3+key4))
keys = list(zip(key1, key2, key3, key4))
keys = functools.reduce(lambda x, y: x+y, map(list, keys))
print("".join(map(chr, keys)))

key_const = keys[:] # make sure the list is copied
print(len(key_const))
# preemble: everything before the call to Q
preemble = open("unquine.c","rb").read().split(b"/*quine*/Q(")[0]
print(len(preemble))
print(preemble)
to_encode = open("unquine.c","rb").read().split(b"0**")[0]
main = open("unquine.c","rb").read().split(b"/*quine*/Q(")[1].split(b"**")[0]
main = main.replace(b"\t",b"")
offset = len([i for i in main if (i>34)])+2
for i in main.split(b"/*")[1:]:
    print(i.split(b"*/")[0])
    offset -= len(i.split(b"*/")[0])+4
print(f"S=M+{offset}")
print(f"*B=M+{offset+256}")

preemble = preemble.replace(b"S=M+999", f"S=M+{offset}".encode())
main = main.replace(b"H+999", f"H+{offset+13}".encode())
main = main.replace(b"*B=M+999", f"*B=M+{offset+256}".encode())
to_encode = to_encode.replace(b"S=M+999", f"S=M+{offset}".encode())
to_encode = to_encode.replace(b"H+999", f"H+{offset+14}".encode())
to_encode = to_encode.replace(b"*B=M+999", f"*B=M+{offset+256}".encode())

print(len(preemble), len(main), len(to_encode))
len_to_write = len(main)+len(key_const)+len(to_encode) - 76
print(len_to_write)
main = main.replace(b"M+8888", f"M+{len_to_write}".encode())
to_encode = to_encode.replace(b"M+8888", f"M+{len_to_write}".encode())

# the output should be a valid quine as long as there are no spaces in the program
with open("quine.c", "wb") as f:
    f.write(preemble)
    f.write(b"/*quine*/Q(")
    f.write(main)
    f.write(b"**\"")
    f.write(bytes(key_const))
    f.write(to_encode.replace(b"\n",b"|").replace(b" ", b"~").replace(b"\"",b"!"))
    f.write(b"/*quine*/Q(")
    f.write(b"\")")

# Output is then formatted manuelly :)


