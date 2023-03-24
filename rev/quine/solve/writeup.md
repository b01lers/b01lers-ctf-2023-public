# Padlock
## Inspect
We are given the source of the program `quine.c`, however, the code is clearly obfuscated.
From this, there are two main approaches. The first one is to compile the program and then inspect the behavior, and the other one being compile then decompile to have a better view on the program. We will focus on the first approach.

We compile the program with `gcc -o quine quine.c` and run it. However it just segfaulted...
After some inspection on the source, we notice that you need to supply an argument when running it. This time the program first output a comment before printing it's own source.
```bash
> ./quine aaaaaaaa
//XXXXXXX
[... source ...]
```

If you then attempt to enter the flag format, it's clear that it checks the flag byte by byte and output the corresponding result.
```bash
> ./quine bctf{aaa}
//OOOOOXXXX
[... source ...]
```

## Brute force
Base on the observation, it's clear that each byte is compared individually, so we can easily bruteforce each byte. See `solve.py` for an easy solve script.