#!/usr/bin/env python3

import os

old_path = os.getcwd()
os.chdir(os.path.dirname(__file__))
with open('../../solve/flag.txt', 'rt') as f:
    FLAG = f.readline().strip()
os.chdir(old_path)

# The little seed awaited its day... On the eve of a truly momentous undertaking!'
# (oops, shouldn't have hidden your secrets in the poem too...)
SEED = b'03/17/2023'
