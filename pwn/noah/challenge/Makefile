EXEC:= noah readint
OBJ:= mem.o

CFLAGS:=-fstack-protector-all -Wall

all: $(EXEC)

clean:
	rm -f $(EXEC)

mem.o:mem.S
	gcc -o $@ -c $(CFLAGS) -O3 $<

noah: $(OBJ)

noah: chal.c
	gcc -o $@ $(CFLAGS) -O3 $< $(OBJ)
#	nm $< > $(@).symbols
#	cp -pf $@ $@-unstripped
	strip -s -K map $@

readint: readint.c
	gcc -o $@ $(CFLAGS) -O3 $<


.SUFFIXES:
.PHONY: all clean
