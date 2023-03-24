# poeticrypto

## Author
enigcryptist

## Difficulty
Intermediate

## Provides
- `dist/cipher.txt`
- `dist/poem.txt`
- `src/algo.py`

## Intended Solution

0. **Look at the files provided.**

    In `algo.py`, you're given a class `TreeOfLife` which takes in key length `key_len = KEY_SIZE = 32` and salt length `salt_len = PRIV_SALT_LEN = 16`. It implements one method, `tree.burn(key)`, which performs AES-GCM encryption of `FLAG` using `00..00` as a nonce.  Then, using this tree with a **secret** `getKey(tree, salt)` function, it returns a key which is used to encrypt the (also secret) `FLAG` with `burn(key)`. This is presumably where `cipher.txt` came from.

    The challenge, then, clearly expects you to decrypt `cipher.txt` back to `FLAG`. But how?

1. **Encryption is sketchy, but...**

    While you should **NEVER re-use nonces** under the same key with AES-GCM,the "nonce" is clearly fixed to `00..00` (DON'T TRY THIS AT HOME: nonce-misuse in AES-GCM allows attackers to perform the "forbidden attack" which castastrophically violates its security). However, a double-take at the code reveals that **this is a red herring**--- the `burn` function only permits encryption with a single message `FLAG`, and `cipher.txt` is clearly the only ciphertext this code could generate. The solution lies elsewhere...

2. **... why is `getKey` secret?**

    Also suspicious is that whoever hypothetically wrote this code kept `getKey` secret (**relying on security by obscurity is bad**). But with all our remaining clues from `algo.py` exhausted, we have to look somewhere else. The only thing we haven't looked at yet is `poem.txt`, so hopefully that'll reveal some clues (and it's in the challenge name, after all...)

3. **The words in this poem seem familiar...**

    Taking a read through the poem, on the surface it just seems to tell the story of a seed that grows into a hearty tree before being burned in a pyre. However, lots of these words seem familiar! `seed`, `tree [...] life`, `salt`, `burn[ed]`...
    
    * **Helpful note:** If you know anything about how people derive keys in practice too, some other words also stand out: `[key] stretched`, `[key] strengthened`, ~~`obscurity`~~, `little seed` , `hashed`... something's clearly going on here.

4. **A key derivation function!**

    Putting together the pieces of the puzzle, you're supposed to build a key derivation function using `poem.txt` as the design specs. `algo.py` even gave you a list of imported algorithms which it expects you to use. So, let's break this down.
    _____
    
    i. **Seed**

        The **little seed** awaited its day [...] **On the eve of a truly momentous undertaking**!

    This seems to imply is that the seed is small. And, indeed, `from Crypto.Protocol.KDF import PBKDF2` is a password-based key derivation function which is designed to create a random seed from an especially small initial inputs ("password").

    * **Key Note:** Catastrophically, whoever wrote the poem accidentally **revealed the seed format** too: it's a specific day associated with "the eve of a truly momentous undertaking". In particular, this day is **when the CTF containing this challenge started**! The description clearly hints at this too:

            I thought I'd write a poem to commemorate the day this CTF went live :)

    In any case, there are a few common choices for date format, including but not limited to:
        
            mm/dd/yyyy # (US)
            mm/dd/yy   # (US)
            mm/dd      # (US)
            yyyy-mm-dd # (ISO)
            dd/mm/yyyy # (International)
            dd/mm/yy   # (International)
            dd/mm      # (International)
            <integer variants>

        
    If you're not sure, just try one seed and enumerate over all the possibilities once you're done. The correct
seed is given below:        
    ```python
    SEED = b'03/17/2023'
    ```

   ii. **Key stretching phase**

   Now you have a candidate seed. Follow the code provided in `algo.py` to make a tree then start on `getKey` (cf. `findKey` in `sol.py`):
    ```python
    tree = TreeOfLife(SEED, PRIV_SALT_BITS, BLOCK_SIZE)
    key = findKey(tree, PUB_SALT)
    ```

   Where do we start? Well, let's keep reading:

        For **ten thousand days** the little sprout **first** grew
        Nourished **by the salt** of the earth, **it stretched** toward the sky!

   And, looking at the documentation for `PyCryptodome` (where `PBKDF2` import was implemented), it takes the following parameters:
    ```python
    Crypto.Protocol.KDF.PBKDF2(password, salt, dkLen, count, prf=None,hmac_hash_module=None)
    ```
    `password` is likely the seed since it's what is being "stretched" into a key. `PUB_SALT = b'Grow grow grow!!` is given. `dkLen` is likely `TreeOfLife.key_len = KEY_SIZE = 32`. `count` is likely the number of days mentioned in the first phase (10000). Lastly, PyCryptodome expects us to use an underlying cryptographic primitive to call `PBKDF2`. Looking at the documentation, we can either use `hmac_hash_module` (a `Crypto.Hash`) or we could use `prf`. But, since `algo.py` specified the algorithms we should use, including `from Crypto.Hash import SHA256` but no PRF, that's likely what it's expected to use here.
In summary: we get the following:
    ```python
    stretched_key = PBKDF2(SEED, PUB_SALT, dkLen=tree.key_len, count=10000, hmac_hash_module=SHA256)
    ```
    iii. **Key strengthening phase**

   Let's keep reading again:

        While the **salt had scattered** for a **hundred days after**,
        The little sprout discovered that [...]
        It had nevertheless **strengthened into a** hardy **tree**!

   The process is very similar here. However, there are a few key differences:

   * The salt had "scattered": we don't know what the salt is anymore (still need it though)
   * The number of iterations this time around is only a hundred "days" (100)

   So, we have no choice but to try and guess the private salt that `getKey` had originally used in this step, up to `2**tree.salt_len` (recalling that `tree.salt_len = PRIV_SALT_LEN = 16`):
    ```python
    for i in range(2**tree.salt_len):
        priv_salt = i.to_bytes(tree.salt_len//2, 'little') # endianness might not matter?
        key_material = PBKDF(stretched_key, priv_salt, dkLen=tree.key_len, count=100, hmac_hash_module=SHA256)
    ```
   iv. **Manual salting phase**
   
   The poem's not done yet though:
        
        The humans [...] **Split** the poor **tree* in two...
        **Half** **left** to rot **in obscurity**, **half** **added right** to the **pyre**!

   There's many plays-on-words going on here, but basically the "tree" (i.e., output of key strengthening) gets split in half, with the **left half** being **discarded** and the **right half** being **used** later
    ```python
    #kl = key_material[:tree.key_len//2]
    kr = key_material[tree.key_len//2:]
    ```
   Continuing on, notice that we're starting to see more references to `burn`:

        Oh, little seed, how you were **hashed**-then-burned **with the ultimate aphorism**:
        **For dust you are and to dust you shall return!**

   The wording of this is admittedly clunky (sorry), but it's saying we have to hash what's remaining of the tree (`kr`) after appending the exact aphorism in the poem ("For dust you are and to dust you shall return!"). Then "burning" this means you're done and the output of the hash is the AES key you need to use:
    ```python
    phrase = b'For dust you are and to dust you shall return!'
    # H(kr || phrase) in bytes
    ha = SHA256.new()
    ha.update(kr + phrase)
    key = ha.digest()
    ```
_____

5. **Testing candidate keys**

    How do you know you're done though? Invert the steps in `burn` to test-decrypt the ciphertext `ct` in `cipher.txt` and, if it gives you back plaintext that looks like `bctf{...}`, you're done!
    ```python
    pt = AES.new(key, AES.MODE_GCM, nonce=b'00000000').decrypt(ct).decode('ascii')
    if pt.startswith('bctf{'):
        FLAG = pt
        print(FLAG)
    # Else, try new keys/seed...
    ```
    Depending on how you implemented it though, you might receive a `UnicodeDecodeError` with most keys you attempt. Since `algo.py` made it clear that `FLAG` was encoded as ASCII, decode failing immediately implies that the key is incorrect. If you follow the instructions in `poem.txt`, try all `2**tree.key_len` private salts, and **still** don't find the flag, your seed is wrong and you should try a different date / date format.

    **Final note**: these parameters are incredibly weak for what you'd use in a real key derivation function (KDF), especially when considering how small and (relatively...) easily guessable the seed is in this challenge. See Additional Readings below for more details.

## Additional Readings

* [RFC 2898; Section 5.2] **[PKCS #5 (v2.0)](https://www.rfc-editor.org/rfc/rfc2898)**: original `PBKDF2` specifications
* [RFC 8018; Sections 4,5,8] **[PKCS #5 (v2.1)](https://www.rfc-editor.org/rfc/rfc8018)**: `PBKDF2` security recommendations
* Authentication failures in NIST version of GCM: **["forbidden attack"](https://csrc.nist.gov/csrc/media/projects/block-cipher-techniques/documents/bcm/comments/800-38-series-drafts/gcm/joux_comments.pdf)** on GCM nonce-reuse (not part of the challenge)


## Post-mortem

I apologize that this challenge involved so much guessing about what the instructions/hints meant. Lesson learned...




