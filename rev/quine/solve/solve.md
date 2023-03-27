---
title: b01lersCTF 2023 - padlock
---

# b01lersCTF 2023 - Padlock
## Introduction
For the past year, b01lers has been a huge success in my opion, with our 2023 edition of b01lers CTF, more interesting challeges are solved by the curious individuals. We received a lot of feedback, and most of them are positive! I'm glad for hosting such a wholesome event for everyone :)
<!--more-->

This year I created one reverse challenge - padlock. It has been a whlie since I've seen the crazy and fascinating entries to ioccc, the international obfuscated c contest. One entry in particular has been one of my favorate: [endoh2.c](https://www.youtube.com/watch?v=6Ak1DC1uBuc) from ioccc 2018 by Yusuke Endoh. So I decided to create something similar.

In this blog post I would like to go through my process of creating this challenge, how it's intended to be solved, how people actually approached it, and how it may be imrpoved.

## Parrot Quine
Before creating our own challenge, I need to first understand how the quine worked in our example. I'll focus on the generated quine itself. Running the quine with `gcc -E quine.c` give us the macro expending version of the quine. We can notice that a copy of the source is stored in `*Q`, but how is this possible? It turns out that the `#define` in c provides a helpful functionality to define functions, and even [inline the function source](https://gcc.gnu.org/onlinedocs/cpp/Stringizing.html#Stringizing) as the character array. 

In a later section, the source implements a decoding machenism to re-format the inline source, and a way to reconstruct the visual of the program. In this section you can see the program copying the inline source into a separate buffer, while skipping the control characters and the quotation marks that helps the formating. The copied source are then interpreted basically through a vm, perferming various operations based on the decoded character. This allows the program to format itself based on the current frame.

## Making a quine
Now that we somewhat understand how this quine work, lets write one ourselves. Since I'm lazy, instead of implementing a bytecode system, I do a simple substitution. Since we know that the macro expension turns new line into white spaces, we can substitude those back when printing, and this should give us back the source. However, there are still plenty of restrictions, firstly, the comments in the macro expension are ignored. I simply avoid using comment in that section. 

Another challenge is to reproduce the part before the macro. I end up putting a copy of the first part of the source also in the string after `return 0 **`. I also encoded the newline and whitespaces in different characters, so we can reproduce the shape. While writing the code, I realize how annonying it is to adjust the offsets, so I write a generator script to generate the final `quine.c` from a template `unquine.c`. I still endup needing to adjust the look of the final string, but it turns out nice.

## The idea of the challenge
Originally I want to make the challenge to visually display a circle or a cross in a digital lock fasion, so there will be a red circle or cross within the source depending on if the input is correct or not. This turns out to be more difficult than I thought, basically requiring the custom bytecode, as in the reference parrot quine. I end up settle with displaying a list of O and X at the top of the lock.

For the actual unlock logic, I didn't think that much. While most people think that brute forcing a challenge is less elegent, I think that there are some merit to it.  I think that sometimes when brute force are implemented correctly, it can save a lot of time while giving insight to the program. The final unlocking scheme i came up with compares each input bytes to a computed value, and output the result corresponding it. 

After a long time of fiddling with the look, the result is this challenge. So now lets solve it!


## Solving the challenge
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
Base on the observation, it's clear that each byte is compared individually. The idea is that we try each possible byte for each location, then we can get back which character outputs the O. After that, recover the key! See `solve.py` for an easy solve script.

## Actually reading the code
Another way of approaching the challenge is to de-obfuscate the source, and implement the logic yourself. We can first expend all the macro by running `gcc -E quine.c`. In the very end, you can see the expended source. The main logic is this short snippet
```
p(-b[1][u/4]+S[u++]-S[u++]+(S[u++]^S[u++])?88:79)
```
which expends (and de-obfuscates) to 
```
if(argv[1][u/4] == S[u++]-S[u++]+(S[u++]^S[u++]))
	putchar('X');
else
	putchar('O');
```
here u is a index pointing to each character of the input, and S points to the start of the chars after the `return ** "` (You can maybe find this by attaching gdb to a running program).

Therefore, to reverse the program, you can simply extract the first 64 characters of that string, and get all the values through a simple script (see `rev.py` for deatil)

Shout out to peace-ranger for another [wonderful writeup](https://github.com/peace-ranger/CTF-WriteUps/tree/main/2023/b01lers%20CTF/(rev)%20padlock) if you want to see more into this route

## Some edge cases / undefined behaviors
During the competition, some participant are attempting to compile the code in windows, and it seems like the windows c compiler optimized out a lot of the logic and make the not behaving as intended. I didn't know that using increment / decrement multiple times in the same line is an undefined behavior (actually it might be something else). I didn't release a warning on where the challenge are tested to be working. My appologies to anyone who can't run the program due to those issues.  
# Appendix A - quine.c
{% capture quine_c %}
```c
              #include/*firt*/<stdio.h>
           #define/*ah*/      p/**/putchar
         #define/*??*/         c/*cal*/char
        #define/*to*/           Q(q)int*P,u\
        /*why...*/=0,           M[99999],*C\
        =M,*S=M+293;c           *Q=#q/*am*/\
        ,H[99999],*D=           H;/*i*/int(\
        main)(int*a,c           **b){q;}/**/
/*quine*/Q(int*B=M+549;int/*ahhh*/l=strlen(b[1]);p(47);
p(47);for(;*Q;Q++){if(*Q==124)*C++=10;else/*haaa*/if(*Q
==126)*C++=32;else/*wtf_is_this*/if(*Q==33)*C++=34;else
/*woeira*/if(*Q>34)*C++=*Q;*D++=*Q==32?'\n':*Q;}for(int
u=-0;u<l*4;)p(-b[1][u/4]+S[u++]-S[u++]+(S[u++]^S[u++])?
88:79);p(10);/*weird___*/for(int*d=B;d<M+1280;)p(*d++);
printf("%s)",/*progra*/H+304);return/*UwU*/0**"^O{(u4X"
"z}e(tiIh.p+}Kj<&eb]0@sHecW^[.xroBCW=N3nG+r.]rGEs.UJw^"
"y'tn_Qv(y;Ed')#@q@xI1N:wH<X1aT)NtMvNlcY0;+x[cQ4j9>Qi2"
"#Yq&fR#os=ELTjS^/deJZ;EuY`#IQwKL)w<N<Zh,;W9X=&t0zX&E0"
"e<_3SVaLs(pXk6z-XGHTx8T/?-^`h[K0h}`dD6kX:vEeC,mI5fR9k"
"]{;yfO0Wg/1-Z^=WyUqN5XY1g25K1sJgKzfG.~~~~~~~~~~~~~~#i"
"nclude/*firt*/<stdio.h>|~~~~~~~~~~~#define/*ah*/~~~~~"
"~p/**/putchar|~~~~~~~~~#define/*??*/~~~~~~~~~c/*cal*/"
"char|~~~~~~~~#define/*to*/~~~~~~~~~~~Q(q)int*P,u\|~~~"
"~~~~~/*why...*/=0,~~~~~~~~~~~M[99999],*C\|~~~~~~~~=M,"
"*S=M+293;c~~~~~~~~~~~*Q=#q/*am*/\|~~~~~~~~,H[99999],*"
"D=~~~~~~~~~~~H;/*i*/int(\|~~~~~~~~main)(int*a,c~~~~~~"
"~~~~~**b){q;}/**/|/*quine*/Q(int*B=M+549;int/*ahhh*/l"
"=strlen(b[1]);p(47);|p(47);for(;*Q;Q++){if(*Q==124)*C"
"++=10;else/*haaa*/if(*Q|==126)*C++=32;else/*wtf_is_th"
"is*/if(*Q==33)*C++=34;else|/*woeira*/if(*Q>34)*C++=*Q"
";*D++=*Q==32?'\n':*Q;}for(int|u=-0;u<l*4;)p(-b[1][u/4"
"]+S[u++]-S[u++]+(S[u++]^S[u++])?|88:79);p(10);/*weird"
"___*/for(int*d=B;d<M+1280;)p(*d++);|printf(!%s)!,/*pr"
"ogra*/H+304);return/*UwU*//*quine*/Q(/*random_stuf*/")
```
{% endcapture %}

{% include widgets/toggle-field.html toggle-name="quine_c"
    button-text="Show quine.c" toggle-text=quine_c%}
# Appendix B - solve.py
{% capture sol_py %}
```python
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
#bctf{qu1n3_1s_4ll_ab0ut_r3p371t10n_4nD_m4n1pul4710n_OwO_OuO_UwU}
```
{% endcapture %}

{% include widgets/toggle-field.html toggle-name="sol_py"
    button-text="Show solve.py" toggle-text=sol_py%}
		
# Appendix C - rev.py
{% capture rev_py %}
```python
#!/usr/bin/python3
rev_string = b"^O{(u4Xz}e(tiIh.p+}Kj<&eb]0@sHecW^[.xroBCW=N3nG+r.]rGEs.UJw^y'tn_Qv(y;Ed')#@q@xI1N:wH<X1aT)NtMvNlcY0;+x[cQ4j9>Qi2#Yq&fR#os=ELTjS^/deJZ;EuY`#IQwKL)w<N<Zh,;W9X=&t0zX&E0e<_3SVaLs(pXk6z-XGHTx8T/?-^`h[K0h}`dD6kX:vEeC,mI5fR9k]{;yfO0Wg/1-Z^=WyUqN5XY1g25K1sJgKzfG."

output = []
for i in range(0, len(rev_string), 4):
    output.append(rev_string[i]-rev_string[i+1]+(rev_string[i+2]^rev_string[i+3]))

print(bytes(output))
#bctf{qu1n3_1s_4ll_ab0ut_r3p371t10n_4nD_m4n1pul4710n_OwO_OuO_UwU}
```
{% endcapture %}

{% include widgets/toggle-field.html toggle-name="rev_py"
    button-text="Show rev.py" toggle-text=rev_py%}
