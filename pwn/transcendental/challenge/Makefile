EXEC:= chal chal.s

CFLAGS:=-fstack-protector-all -Wall -Qn

all: $(EXEC)

clean:
	rm -f $(EXEC)

%-O1.s:%.c
	gcc -o $(@) -S $(CFLAGS) -O1 $<
%-O2.s:%.c
	gcc -o $(@) -S $(CFLAGS) -O2 $<
%.s:%.c
	gcc -o $(@) -S $(CFLAGS) -O3 $<
%:%.s
	gcc -o $@ $<
	strip -s $@
	patchelf --set-rpath / $@


.SUFFIXES:
.PHONY: all clean
