# poeticrypto

## Type
crypto

## Difficulty
Easy/Intermediate (?)

## Description
I thought I'd write a poem to commemorate the day this CTF went live :)

## Provides
- `dist/cipher.txt`
- `dist/poem.txt`
- `src/algo.py`

## Structure
    .
    ├── src/
    │   ├── algo.py         # (dist) Encrypts flag with key obtained from seed + algorithm in `src/SECRET`
    │   └── SECRET/
    │       ├── keygen.py   # The algorithm to generate the key
    │       └── priv_vals.py# Seed and flag
    ├── dist/
    │   ├── poem.txt        # A helpful poem... :)
    │   └── cipher.txt      # Ciphertext of flag
    ├── solve/
    │   ├── flag.txt        # The flag
    │   └── sol.py          # Intended solution + writeup
    └── README.md
