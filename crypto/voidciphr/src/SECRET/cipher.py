#!/usr/bin/env python3

import os
import re
import string

from secret import codebook, pt

# Intended message/ciphertext should strip out all non-English alphabetic characters except spaces
regex = re.compile('[^a-zA-Z ]')

def encipher(codebook, pt):
    pt_clean = regex.sub('', pt)
    ct = ''
    for p_char in pt_clean:
        ct += codebook[p_char].upper()
    return ct

def decipher(codebook, ct):
    ct_clean = regex.sub('', ct)
    pt_new = ''
    for c_char in ct_clean:
        p_chars = list(filter(lambda x: (x in codebook) and codebook[x] == c_char, string.ascii_lowercase + ' '))
        if len(p_chars) == 0:
            pt_new += c_char
        else:
            pt_new += p_chars[0]
    return pt_new


if __name__ == '__main__':

    old_path = os.getcwd()
    os.chdir(os.path.dirname(__file__))

    # Generate ciphertext
    ct = encipher(codebook, pt)

    # Check that the deciphering works correctly
    pt_dec = decipher(codebook, ct)
    pt_clean = regex.sub('', pt)
    assert(pt_clean == pt_dec)

    # Store ciphertext at dist/cipher.txt
    with open('../../dist/cipher.txt', 'wt') as f:
        print("Saving ciphertext to dist/cipher.txt...")
        f.write(ct)
    print(ct)

    os.chdir(old_path)
