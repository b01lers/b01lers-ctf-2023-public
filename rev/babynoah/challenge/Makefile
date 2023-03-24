EXEC:= babynoah
OBJ:= mem.o

CFLAGS:=-fstack-protector-all -Wall

all: $(EXEC)

clean:
	rm -f $(EXEC)

mem.o:mem.S
	gcc -o $@ -c $(CFLAGS) -O3 $<

babynoah: $(OBJ)

babynoah: chal.c
	gcc -o $@ $(CFLAGS) -O3 $< $(OBJ)
#	nm $< > $(@).symbols
#	cp -pf $@ $@-unstripped
	strip -s -K map $@

.SUFFIXES:
.PHONY: all clean
