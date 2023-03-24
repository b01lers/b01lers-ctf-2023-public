# voidciphr

## Author
enigcryptist

## Type
crypto

## Difficulty
Easy

## Description
For obfuscation, I had a void suck away part of my 🔑

Flag format: bctf{KEYPHRASE}

## Provides
- `dist/cipher.txt` (generate via `python3 src/SECRET/cipher.py`)

## Example Solution

This is a substitution cipher, with a couple twists... there are many possible ways to intuit how to crack classical ciphers by frequency analysis and word association, this is just how I solved it. If you solve it by hand, the hardest part of a substitution cipher is always starting.

For clarity, let uppercase letters `A, B, ..., Z` denote ciphertext letters, and let lowercase letters `a, b, ..., z` denote decoded plaintext letters. `_` denotes a currently unmapped letter ("blank"), and `␣` denotes whitespace.

0. Try inputting `cipher.txt` into [dcode.fr](dcode.fr/en) or [CyberChef](https://gchq.github.io/CyberChefi/)'s subroutines (e.g. `Magic`). (EDIT) Neither of these worked for me, but apparently both worked for some folks ¯\\\_(ツ)\_/¯ If you got valid plaintext from one of these tools, jump to Step 10. Steps 1-9 show how to do it by hand, just in case.
1. **ETAOIN:**

    As the tools likely had done, try basic frequency analysis assuming that it's just a simple substitution cipher: what do you see?
```python
from collections import Counter
c = Counter(ct) # cipher.txt
print(c.most_common())
```

    (' ', 252), ('X', 141), ('G', 126), ('M', 113), ('A', 104), ('P', 93), ('Q', 91), ...

Perhaps unusually, if we try and map the most common letters in the ciphertext to the 6 most common letters in the English language, ETAOIN, the output still looks meaningless. What else can we try?

---

**Historical Aside:** The technique used here, i.e. breaking simple substitution ciphers with frequency analysis and other statistical inference techniques, was first invented by Arab polymath and philosopher (Abū Yūsuf Yaʻqūb ibn ʼIsḥāq aṣ-Ṣabbāḥ) al-Kindī in the 9th century AD.

---

2. (Informal) **1-letter** and **2-letter** analysis:

    It's very helpful that the ciphertext includes spaces, because we know exactly where the 1- and 2-letter words are located. Easiest step to try by hand is to first to get an idea if this is even English and/or a substitution cipher...

    * If we assume that `X` is the most common letter in the English alphabet, then try replacing `X -?-> e`. That can't be right though, since the ciphertext **word** ` X ` occurs with very high frequency, and the word ` e ` doesn't even exist in the English language.
    * However, `X` shows up at the beginning of a lot of 2-letter words as well, so it's likely either the letter `a` or `i`, and both letters are also words themselves. Going by the most common letters in the English language ("ETAOIN"), try `X -> a` instead.
    * By the same argument, `M -/-> o` and it follows instead that `M -> i`.

3. (Informal) **3-letter** analysis:

    It now contains many `aAT` words. The most common matching English word is `and`, so try `A -> n` and `T -> d`.

    If you squint your eyes a bit now, you can see fragments of lowercase letters that look vaguely like English: we're on the right track! Lots of `-ian-` and `-in` letters in the middle of worlds, `an-` at the beginning of words, `-and` at the end of words, etc.

4. I'm feeling **indignant** for being forced to do a cipher chal by hand... (EDIT: or not)

    A word that nearly looks complete with this mapping is `indiYnanP`, as in `indignant`. So, try `Y -> g` and `P -> t`.

5. This chal is **insignificant** and not worth my time.

    Similarly, `inQigniBiUant` looks like `insignificant`, so try `Q -> s`, `B -> f`, and `U -> c`.

6. I'm glad my **initial** assumptions were correct though!

    `initiaF` looks like `initial`, so try `F -> l`. `staVt` looks like `start`, so try `V -> r`. `arGNnd` looks like `around`, so try `G -> o` and `N -> u`.

7. Did **politicians** in the past seriously think simple substitution ciphers were secure?

    From here, the plaintext will come together very quickly.
    `Zoliticians` looks like `politicians`, so try `Z -> p`. `Ouilding` looks like `building`, so try `O -> b`. By word associations, `rigRt Jing` looks like `right wing`, so try `R -> h` and `J -> w`.

8. I should take note of that in my **journal**, it might come in handy later.

    `Iournal` looks like `journal`, so try `I -> j`. `Kirtual` looks like `virtual`, so try `K -> v`. `hastilD` looks like `hastily`, so try `D -> y`. `huLan consuLption` looks like `human consumption`, so try `L -> m`.

9. Even without that knowledge, having a large **quantity** of ciphertext and other information to pull from helps.

    `hardworSing folS` looks like `hardworking folks`, so try `S -> k`. `hoaH` looks like `hoax`, so try `H -> x`. `Wuantity` looks like `quantity`, so try `W -> q`.

10. But where's the flag...?

    At this point, the plaintext is completely decrypted and clearly reads as English. However, the flag isn't mentioned anywhere in the text itself. Literally the only other place to check for a flag is your key mapping. If you look at only the decryption key (ordered by ciphertext alphabet), it looks like gibberish at first:

        CIPHR: A B _ D _ F G H I J K L M N O P Q R S T U V W X Y Z ␣
        plain: n f _ y _ l o x j w v m i u b z s h k d c r q a g p ␣

However, the other way of looking at the mapping is to look at the encryption key (ordered by plaintext alphabet), you might recognize something:

        plain: a b c d e f g h i j k l m n o p q r s t u v w x y z ␣
        CIPHR: X O U T _ B Y R M I S F L A G Z W V Q P N K J H D _ ␣

---

**(Actually Relevant) Historical Aside:** If you know anything about the history of cryptanalysis, since antiquity people have struggled to remember a random 26 letter key, and writing it down posed a significant security risk if it were stolen by enemy spies (just like you shouldn't write down your passwords on paper today...)! Instead, people often memorized what's often called a **keyphrase** which they could use to generate the encryption/decryption key by memory. Generally, they would use the following algorithm:

i. Memorize your favorite phrase.

ii. Ordering plaintext alphabet as `a b ... z` (or as appropriate for your language), populate the corresponding letters of ciphertext with your desired phrase, deleting repeat letters to ensure a correct mapping for substituting back and forth. For example, if our keyphrase was `HELLO WORLD`, our encryption key might start as something like the following:
        
        plain: a b c d e f g h i j k l m n o p q r s t u v w x y z ␣
        CIPHR: H E L O W R D _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ ␣

iii. Use some easy-to-remember algorithm to fill in the rest of the letters in the mapping from plaintext to ciphertext. For example, we could count alphebetically back from `Z Y ... A` (again, avoiding repeats) to get a valid permutation/key:
        
        plain: a b c d e f g h i j k l m n o p q r s t u v w x y z ␣
        CIPHR: H E L O W R D Z Y X V U T S Q P N M K J I G F C B A ␣

Of course, using a keyphrase often leads to a less random mapping, causing issues like having identity mappings between individual plaintext and ciphertext letters (for example, `p <-> P` above). If this method of generating the key was known, this also greatly limited the attacker's search space for brute-force attempts at deciphering the plaintext, especially if they had a **crib** which clued them in to what the keyphrase or plaintext might be. However, longer and carefully-chosen keyphrases at provided sufficient entropy to make the ciphertexts unreadable to the naked eye, at least. Although we know this technique to be extremely insecure today, for centuries (if not millenia) this was considered state-of-the-art in classical cryptography.

---

Even if you still don't notice the gimmick by this point (the plaintext letter `e` **never** shows up in the entire challenge, including the name and description!), the only ciphertext letters that have been left unmapped are `E` and `C`, and the only plaintext letters left unmapped are `e` and `z`. Also, even though it doesn't quite read like English, a couple words are clearly noticeable in the encryption key (spacing added):

        X OUT _ BY RM IS FLAG

 XOUT_BYRM**ISFLAG**. There's only a few things left to try to get the flag:

        bctf{XOUTEBYRM}
        bctf{XOUTEBYRMISFLAG}
        bctf{XOUTEBYRMISFLAGZWVQPNKJHDC}
        bctf{XOUTCBYRM}
        bctf{XOUTCBYRMISFLAG}
        bctf{XOUTCBYRMISFLAGZWVQPNKJHDE}
        bctf{XOUTBYRM}
        bctf{XOUTBYRMISFLAG}
        bctf{XOUTBYRMISFLAGZWVQPNKJHD}

The first one is the flag! (Mnemonic: `X [cross] out E by RM [removing from alphabet]`)

## Alternate "Solution"

Even if you correctly guessed that the flag was 1) in the encryption key, 2) consisted only of English letters and 3) was all in uppercase, the flag is long enough (7 characters) that it's not very feasible to solve the challenge by brute-force alone. Doing it by hand is almost certainly faster, and that's saying something.

## Additional Resources
* [La Disparition](https://bookshop.org/p/books/la-disparition-de-georges-perec-fiche-de-lecture-et-analyse-complete-de-l-oeuvre-georges-perec/14374058) ([A Void](https://bookshop.org/p/books/a-void-georges-perec/623575)) by Georges Perec: A 300-page French novel (with English translation), both written and translated without once using the letter `e`. **The plaintext is its opening paragraph.**
* [The Code Book](https://www.goodreads.com/book/show/17994.The_Code_Book) by Simon Singh: Directly inspired this challenge. Goes a lot more in-depth into the history of ciphers and modern cryptography.
* [ngram-scoring](http://practicalcryptography.com/cryptanalysis/letter-frequencies-various-languages/english-letter-frequencies/) (HTTP Only): One of many resources giving a list of English n-grams and an implementation of how to score them. **Extra Challenge**: try stripping the spaces from this chal's ciphertext and applying more complex techniques!
* [dcode.fr](dcode.fr/en) and [GCHQ's CyberChef](https://gchq.github.io/CyberChef/): I riffed on these tools a bit in this writeup, because it's good to at least know how to decrypt ciphers by hand and know **why** they're so easy to crack. You don't learn much by just throwing a tool at something. However, they're great tools for automating away the tedium of converting between different encodings, or cracking common classical ciphers.
