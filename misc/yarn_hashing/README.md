# yarn_hashing

## Author
enigcryptist

## Type
misc

## Difficulty
Easy

## Description
Maybe if I weave the flag into a tight enough space, you won't be able to find it...

Flag format: bctf{...}

## Provides
- `src/yarn_hash.py`
- `dist/hash.txt`

## Structure
    .
    ├── src/
    │   ├── yarn_hash.py    # (dist) Hashes flag onto a curve
    │   └── SECRET.py
    ├── dist/
    │   └── hash.txt        # Hash of flag
    ├── solve/
    │   ├── flag.txt        # The flag
    │   ├── solve.md        # Solution writeups (+ discussing unintended ones)
    │   └── sol.py          # Intended solution
    └── README.md
