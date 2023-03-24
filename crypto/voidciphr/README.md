# voidciphr

## Type
crypto

## Difficulty
Easy

## Description
For obfuscation, I had a void suck away part of my 🔑

Flag format: bctf{KEYPHRASE}

## Provides
- `dist/cipher.txt`

## Structure
    .
    ├── src/SECRET
    │       ├── plain.txt   # Original plaintext
    │       ├── cipher.py   # Encodes/decodes plaintext 
    │       └── secret.pt   # Stores codebook/key mapping stuff
    ├── dist                
    │   └── cipher.txt      # Ciphertext
    ├── solve                
    │   ├── flag.txt        # The flag (for reference)
    │   └── sol.py          # Intended solution
    └── README.md
