#!/usr/bin/python3

import os

old_path = os.getcwd()
os.chdir(os.path.dirname(__file__))

pt = ''
with open('plain.txt', 'rt') as f:
    lines = f.readlines()
    for line in lines:
        pt += line.strip()

# Plain: a b c d e f g h i j k l m n o p q r s t u v w x y z
# Ciphr: X O U T E B Y R M I S F L A G Z W V Q P N K J H D C
codebook = {
    'a':'X',
    'b':'O',
    'c':'U',
    'd':'T',
    'e':'E',
    'f':'B',
    'g':'Y',
    'h':'R',
    'i':'M',
    'j':'I',
    'k':'S',
    'l':'F',
    'm':'L',
    'n':'A',
    'o':'G',
    'p':'Z',
    'q':'W',
    'r':'V',
    's':'Q',
    't':'P',
    'u':'N',
    'v':'K',
    'w':'J',
    'x':'H',
    'y':'D',
    'z':'C',
    ' ':' '
}

os.chdir(old_path)
