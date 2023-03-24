from pwn import *

context.log_level = 'CRITICAL'

res = [0 for i in range(66)]
for ch in range(1,128):
    p = process(["./quine", chr(ch)*64])
    output = p.recvall()
    #print(output)
    for i in range(66):
        if output[i:i+1] == b'O':
            res[i] = ch
print(("".join(map(chr, res)))[2:])