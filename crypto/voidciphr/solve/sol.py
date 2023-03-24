#!/usr/bin/env python3

import os
import re
import string
from collections import Counter

# NOTE: Simple substitution cipher, same as src/SECRET/cipher.py

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

# Intended message/ciphertext is only English alphabetic characters, including spaces
regex = re.compile('[^a-zA-Z ]')

MISSING_LETTER = '_'

# For clarity, define A ... Z to denote enciphered letters (RHS), and a ... z to denote plaintext (LHS, once determined)
# You don't know any of the decrypted values by default, so start with identity permutation.
default_codebook = {
    'A':'A',
    'B':'B',
    'C':'C',
    'D':'D',
    'E':'E',
    'F':'F',
    'G':'G',
    'H':'H',
    'I':'I',
    'J':'J',
    'K':'K',
    'L':'L',
    'M':'M',
    'N':'N',
    'O':'O',
    'P':'P',
    'Q':'Q',
    'R':'R',
    'S':'S',
    'T':'T',
    'U':'U',
    'V':'V',
    'W':'W',
    'X':'X',
    'Y':'Y',
    'Z':'Z',
    ' ':' '
}

# Print pt-ct table. Default for missing letter (if unknown letter in key) is '_'
def print_key(codebook):

    print('Plain:\t', end='')
    # Print a ... z (as reference)
    for p_char in list(string.ascii_lowercase):
        print('%s' % p_char, end=' ')
    print('\nCiphr:\t', end='')
    # Print corresponding known letters of key for substitution cipher
    for c in list(string.ascii_lowercase):
        if (c in codebook) and c.upper() != codebook[c]:
            print('%s' % codebook[c], end=' ')
        else:
            print(MISSING_LETTER, end=' ')
    print('\n')



if __name__ == '__main__':

    os.chdir(os.path.dirname(__file__))

    # Get ciphertext
    ct = ''
    with open('../dist/cipher.txt', 'rt') as f:
        lines = f.readlines()
        for line in lines:
            ct += regex.sub('', line)

    print('Ciphr:\t%s' % ct)
    print('--------------------------------')

    # Attempt 1.A: Try dcode.fr's suggested transcriptions; doesn't get you there immediately
    # (looking ahead, there's no e in the plaintext---an excerpt from "The Void"---and e's assumed most common, so basic statistical analysis don't help you much
    # Attempt 1.B: just as dcode.fr above likely would have, blindly try basic frequency analysis (letter counting)
    c = Counter(ct)
    print(c.most_common())
    print('--------------------------------')
    print('\tAttempt 1\t')
    print('        Try ETAOIN')
    print('--------------------------------')
    
    """
    # Test-decrypt most common letter X -> e (as in ETAOIN)
    codebook1 = default_codebook
    codebook1['e'] = 'X'
    codebook1['t'] = 'G'
    codebook1['a'] = 'M'
    codebook1['o'] = 'A'
    codebook1['i'] = 'P'
    codebook1['n'] = 'Q'
    pt_guess1 = decipher(codebook1, ct)

    print_key(codebook1)
    print('Plain:\t%s' % pt_guess1)
    """

    # Observation: Suspiciously, it transcribes MANY single-letter X's to 'e': X -> e. ' a ' is the most common single-letter word and ' e ' is non-existent, so X -> e can't be right. Try 'a' first then. Similar observation for 'i' too:
    print('--------------------------------')
    print('\tAttempt 2\t')
    print('  Try X->a, M->i instead\t')
    print('--------------------------------')
    codebook2 = default_codebook
    codebook2['a'] = 'X'
    codebook2['i'] = 'M'
    pt_guess2 = decipher(codebook2, ct)

    print_key(codebook2)
    print('Plain:\t%s' % pt_guess2)

    # Observation: Lots of partially enciphered aAT in what vaguely look like connecting pieces between words. Likely 'and', so:
    print('--------------------------------')
    print('\tAttempt 3\t')
    print('    Try A->n, T->d\t')
    print('--------------------------------')
    codebook3 = codebook2
    codebook3['n'] = 'A'
    codebook3['d'] = 'T'
    pt_guess3 = decipher(codebook3, ct)

    print_key(codebook3)
    print('Plain:\t%s' % pt_guess3)

    # Keep making guesses based on what are obviously English words...
    print('--------------------------------')
    print('\tAttempt 4\t')
    print('      Try Y->g, P->t\t')
    print('--------------------------------')
    codebook4 = codebook3
    codebook4['g'] = 'Y'
    codebook4['t'] = 'P'
    pt_guess4 = decipher(codebook4, ct)

    print_key(codebook4)
    print('Plain:\t%s' % pt_guess4)

    print('--------------------------------')
    print('\tAttempt 5\t')
    print('  Try Q->s, B->f, U->c\t')
    print('--------------------------------')
    codebook5 = codebook4
    codebook5['s'] = 'Q'
    codebook5['f'] = 'B'
    codebook5['c'] = 'U'
    pt_guess5 = decipher(codebook5, ct)

    print_key(codebook5)
    print('Plain:\t%s' % pt_guess5)

    print('--------------------------------')
    print('\tAttempt 6\t')
    print(' Try F->l, V->r, G->o, N->u')
    print('--------------------------------')
    codebook6 = codebook5
    codebook6['l'] = 'F'
    codebook6['r'] = 'V'
    codebook6['o'] = 'G'
    codebook6['u'] = 'N'
    pt_guess6 = decipher(codebook6, ct)

    print_key(codebook6)
    print('Plain:\t%s' % pt_guess6)

    print('--------------------------------')
    print('\tAttempt 7\t')
    print('  Try Z->p, O->b, R->h, J->w')
    print('--------------------------------')
    codebook7 = codebook6
    codebook7['p'] = 'Z'
    codebook7['b'] = 'O'
    codebook7['h'] = 'R'
    codebook7['w'] = 'J'
    pt_guess7 = decipher(codebook7, ct)

    print_key(codebook7)
    print('Plain:\t%s' % pt_guess7)

    print('--------------------------------')
    print('\tAttempt 8\t')
    print('  Try I->j, K->v, D->y, L->m')
    print('--------------------------------')
    codebook8 = codebook7
    codebook8['j'] = 'I'
    codebook8['v'] = 'K'
    codebook8['y'] = 'D'
    codebook8['m'] = 'L'
    pt_guess8 = decipher(codebook8, ct)

    print_key(codebook8)
    print('Plain:\t%s' % pt_guess8)

    print('--------------------------------')
    print('\tAttempt 9\t')
    print('    Try S->k, H->x, W->q')
    print('--------------------------------')
    codebook9 = codebook8
    codebook9['k'] = 'S'
    codebook9['x'] = 'H'
    codebook9['q'] = 'W'
    pt_guess9 = decipher(codebook9, ct)

    print_key(codebook9)
    print('Plain:\t%s' % pt_guess9)

    # Ciphertext is now fully decrypted!
    codebook = codebook9
    pt = pt_guess9

    # Observation: You could check the plaintext. The flag isn't there, but...!
#    with open("dec-plain.txt", "w") as f:
#        f.write(pt)

    print('--------------------------------')
    print('\tAttempt 10\t')
    print('    Infer flag from key')
    print('--------------------------------')

    # The only other place to check for a flag is the keyphrase you just found, which indeed tells you that "XOUT_BYRMISFLAG". From there, it's obviously the E that's been "X"ed out, so submit flag.
    print('FINAL KEYPHRASE:')

    keyphrase = ''
    #f = open("keyphrase.txt", "wt")
    for p_char in string.ascii_lowercase:
        keyphrase += codebook[p_char] if (p_char in codebook) else '_'
    #f.write(keyphrase)
    print_key(codebook)

    print('bctf{%s}' % keyphrase[:keyphrase.find('FLAG')-2].replace('_', 'E'))
