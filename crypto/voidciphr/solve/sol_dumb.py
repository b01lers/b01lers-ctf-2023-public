#!/usr/bin/env python3

import itertools
import os
import string
import time

# How many submissions would it take to brute force a flag that you know is in the keyphrase and is English letters only?
def generate_flags(n=7, upper=None):
    count = 0
    if upper == True:
        chars = string.ascii_uppercase
    elif upper == False:
        chars = string.ascii_lowercase
    else:
        chars = string.ascii_letters
    for item in itertools.product(chars, repeat=n):
        count += 1
        yield ''.join(item)

old_path = os.getcwd()
os.chdir(os.path.dirname(__file__))
# Flag format is given
with open('./flag.txt', 'rt') as f:
    FLAG = f.readline().strip()
    FLAG_PREFIX = FLAG.rsplit('{',1)[0] + '{'
    FLAG_POSTFIX = '}'
os.chdir(old_path)

if __name__ == '__main__':
    count = 0
    start_sec = time.time()
    # Make some guesses about the flag
    #crib = 'XOUTE'
    crib = ''
    for flag_len in range(max(0, len(crib)), 26):
        for flag in generate_flags(n=flag_len-len(crib), upper=True):
            count += 1
            if count % 10000000 == 0:
                curr_sec = time.time()
                print(count, flag, '%.3f sec' % (curr_sec - start_sec))
            if (FLAG_PREFIX + crib + flag + FLAG_POSTFIX) == FLAG:
                print('Found flag: %s' % flag);
                end_sec = time.time()
                print('Tries: %d' % count)
                print('Time: %.3f sec' % (end_sec - start_sec))
                break
