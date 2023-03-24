#!/usr/bin/env python3

# Use these algorithms
from binascii import unhexlify, hexlify
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2

from Crypto.Random import get_random_bytes

# The obfuscated algorithm for deriving the key
def getKey(tree, salt):

    # Key stretching phase
    # 'For ten thousand days [iterations] the little sprout first grew'
    first_days = 10000
    # 'Nourished by the salt of the earth, it [key] stretched toward the sky!'
    prekey_material = PBKDF2(tree.seed, salt, dkLen=tree.key_len, count=first_days, hmac_hash_module=SHA256)

    # Key strengthening phase
    # 'While the salt had scattered [randomly] for a hundred days [iterations] after,'
    # Supposed to be random but, for determinism (and a chance for an additional lucky guess :), we choose the 16-bit secure salt to be 'dead':
    #secure_salt = get_random_bytes(tree.salt_len//8)
    days_no_salt = 100
    secure_salt = unhexlify('dead')
    print('PRIV_SALT\n', hexlify(secure_salt).decode('ascii'))
    # 'It had nevertheless [key] strengthened'
    key_material = PBKDF2(prekey_material, secure_salt, dkLen=tree.key_len, count=days_no_salt, hmac_hash_module=SHA256)

    # Manual salting phase
    # 'The humans... Split the poor tree in two...'
    # 'Half added right to the pyre [hr will be included], half left to rot in obscurity [hl unused]!'
    #kl = key_material[:tree.key_len//2]
    kr = key_material[tree.key_len//2:]
    # 'Oh, little seed, how you were hashed-then-burned with the ultimate aphorism [include the following after remains of the tree in the pyre (i.e H( kr || phrase )]:'
    # 'For dust you are and to dust you shall return!' [phrase]
    # Encryption with key is called burn(), so "pyre" here implies that the output of this hash is the key
    phrase = b'For dust you are and to dust you shall return!'
    ha = SHA256.new()
    ha.update(kr + phrase)
    key = unhexlify(ha.hexdigest())
    print('KEY\n', hexlify(key).decode('ascii'))
    return key
