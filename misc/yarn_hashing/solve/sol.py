#!/usr/bin/env python3

# SUMMARY: You can't just choose any ol' curve and hashing algorithm even if it's mildly-resistant to brute-force attacks to invert or find a direct collision. Turns out, if the curve lets you invert the operations you used to hash (oops!), or even if you know similar inputs give similar outputs in a predictable way (i.e. locality-preserving hash), it's easy to get back the flag.

from Crypto.Util.number import bytes_to_long, long_to_bytes

import os
import random
from yarn_hash import Yarn

old_path = os.getcwd()
os.chdir(os.path.dirname(__file__))
with open('./flag.txt', 'rt') as f:
    FLAG_PREFIX = f.readline().strip().rsplit('{',1)[0] + '{'
with open('../dist/hash.txt', 'rt') as f:
    hx = int(f.readline().strip()[2:], 10)
    hy = int(f.readline().strip()[2:], 10)
os.chdir(old_path)


# Attempt 1: brute force -- this is way too slow
def try_brute_force(yarn, x, y):
    minDist = float('inf')
    for d in range(bytes_to_long(bytes(FLAG_PREFIX, 'ascii')) % yarn.n_winds, yarn.n_winds):
        cand_flag = long_to_bytes(d).decode()
        xp, yp = yarn.fold(dot=d)
        l1_dist = abs(x - xp) + abs(y - yp)
        if l1_dist < minDist:
            minDist = l1_dist
            print('Dist from flag with d=%s:' % cand_flag, minDist)
            if l1_dist == 0:
                print('FLAG:', cand_flag)
                return cand_flag

# Try out some small curves to see what it looks like and how it hashes.
def try_small_curve(yarn, dot=None):
    # hard to graph with large (x,y) space \in [0,2^(2*ply))^2, so to prevent it plotting forever...
    assert(yarn.ply <= 5)
    yarn.render_fabric(dot)

# Through either finding out what curve this is online or reverse engineering the code provided, invert the `fold` operation (in essense, inverting hash_to_curve)
def unravel(yarn, x, y):
    dot = 0
    skein = 1 << (yarn.ply-1)
    while skein > 0:
        
        # 0 or 1
        block_x = (x & skein) > 0
        block_y = (y & skein) > 0

        dot += skein * skein * ((3 * block_x) ^ block_y)
        x, y = yarn.twist(x, y, block_x, block_y, 1 << (yarn.ply))
        skein = skein // 2

    return dot

# Same as above, but only works for hashes of valid strings
def invert_hash(yarn, x, y):
    return long_to_bytes(unravel(yarn, x, y)).decode()

if __name__ == "__main__":
    # I made sure this ply=112 parameter was large enough to make it so modulus above didn't affect anything (it's only for correctness' sake on large strings). You could make it smaller and force people to find the flag by looking at "wrap-around" values, but that would bury the lede too far IMO
    curve = Yarn(ply=112)

    # Attempt 0: Brute-force
    #print(try_brute_force(curve, x, y))
    # Attempt 1: Plot d -> (x,y) -- looks like a Hilbert curve!
    short_yarn1 = Yarn(ply=1)
    short_yarn2 = Yarn(ply=2)
    short_yarn3 = Yarn(ply=5)
    try_small_curve(short_yarn1, 2)
    try_small_curve(short_yarn2, 2)
    try_small_curve(short_yarn3, 2)
    # Attempt 2: Invert Hilbert curve
    flag = invert_hash(curve, hx, hy)
    print(flag)

    # Aside: sanity check that unravel works correctly
    dot = random.randint(0, curve.n_winds-1)
    assert(dot == unravel(curve, *curve.fold(dot)))
