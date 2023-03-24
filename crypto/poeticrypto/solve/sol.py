#!/usr/bin/env python3

# SUMMARY: The intended attack follows a very similar algorithm to how we derived the key in the first place (see `src/SECRET`), except we don't know the secure salt value used in the key strengthening phrase and must instead brute-force all 2^PRIV_SALT_BITS possible values. Because we hint at the seed in the poem and choose very weak parameters for PBKDF2, this KDF is almost trivial to crack by brute-force alone if you know what the algorithm is doing. See `solve.md` for more details.

# NOTE: AES.MODE_GCM being instantiated with a fixed nonce is a red herring, and isn't (shouldn't be) an attack vector in this scenario.

import os

# Use these algorithms
from binascii import unhexlify, hexlify
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2

from Crypto.Random import get_random_bytes

# Flag format is given
FLAG_PREFIX = 'bctf{'
# Ciphertext is provided
old_path = os.getcwd()
os.chdir(os.path.dirname(__file__))
ct = b''
with open('../dist/cipher.txt', 'rt') as fc:
    ct = unhexlify(fc.readline().strip())
    print('CIPHERTEXT:\n', hexlify(ct).decode('ascii'))
os.chdir(old_path)


# The "little seed" in the poem
SEED = b'03/17/2023'

from algo import TreeOfLife, PUB_SALT, KEY_SIZE, PRIV_SALT_BITS

# The deduced algorithm for deriving the key
def findKey(tree, salt):

    first_days = 10000
    days_no_salt = 100
    # Key stretching phase
    stretched_key = PBKDF2(tree.seed, salt, dkLen=tree.key_len, count=first_days, hmac_hash_module=SHA256)
    
    key = None
    phrase = b'For dust you are and to dust you shall return!'
    
    # (Crack by brute force) key strengthening phase
    print('%d possible secure salts. Testing the key derived with each...' % 2**tree.salt_len)
    for i in range(0, 2**tree.salt_len):
        # Just so we know it's running, report its progress...
        if i % 10000 == 0:
            print('i=%d' % i)

        secure_salt = i.to_bytes(tree.salt_len//8, 'little')
        key_material = PBKDF2(stretched_key, secure_salt, dkLen=tree.key_len, count=days_no_salt, hmac_hash_module=SHA256)
        
        # Manual salting phase: key = H( kr || phrase )
        #kl = key_material[:tree.key_len//2]
        kr = key_material[tree.key_len//2:]
        ha = SHA256.new()
        ha.update(kr + phrase)
        key = unhexlify(ha.hexdigest())
        
        # Test-decryption on this candicate key. We'll know we cracked the key derivation algorithm with the correct KDF seed and secure salt if we can find the flag prefix in the resulting plaintext:
        try:
            pt = AES.new(key, AES.MODE_GCM, nonce=b'00000000').decrypt(ct).decode('ascii')
            # pt must be valid text, also check that it's the flag we're looking for
            if pt.startswith(FLAG_PREFIX):
                print('i=%d' % i)
                print('PRIV_SALT\n', hexlify(secure_salt).decode('ascii'))
                print('KEY\n', hexlify(key).decode('ascii'))
                print('FLAG\n', pt)
                return key
        # Encryption fails because it's not valid text
        except UnicodeDecodeError:
            pass
        # Try new key...
    # Your seed didn't work with any salt... try again?
    return


if __name__ == "__main__":
 
    tree = TreeOfLife(SEED, PRIV_SALT_BITS, KEY_SIZE)
    key = findKey(tree, PUB_SALT)
    flag = AES.new(key, AES.MODE_GCM, nonce=b'00000000').decrypt(ct).decode('ascii')
