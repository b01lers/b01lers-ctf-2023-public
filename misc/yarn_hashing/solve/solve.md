# yarn_hashing

## Author
enigcryptist

## Difficulty
Easy

## Provides
- `src/yarn_hash.py`
- `dist/hash.txt`

## Intended Solution

0. Looking at the source code provided (`yarn_hash.py`), the flag text seems to be converted into an integer modulo `n_winds`, which is then hashed to some 2D point defined by some `Yarn` curve. The curve takes in `ply=112` as a parameter, which results in the input space $[0, 2^{2 \cdot 112}-1]$. The hash function is defined by the functions `fold`, `twist`, and `flip`.

1. **Attempt 1**: Consider pre-computing various hashes in an attempt to find the `FLAG` by brute-force, with the higher-order bits of the integer fixed to what the flag format`bctf{...}` might imply. However, the input space is much too large to reliably brute-force the flag. But if you try outputting all $H(i)$ in order, you might see that the points are very close together...

2. **Observation**: Since this code lets us input any curve parameter, start off simple by looking at what happens with smaller curves. If you took $H(0), H(1), \ldots, H(2^{2n}-1)$, you might notice something interesting: nearby inputs $i$ and $j$ result in nearby points $H(i) = (x_i, y_i)$ and $H(j) = (x_j, y_j)$! This is true with many distance metrics: $L_1$ (Manhattan), $L_2$ (Euclidean), Hamming...

3. **Observation**: The challenge's source code even provides a `render_fabric` function which appears to print a nice graph of the curve for you! For example, if we try `ply=1` `ply=2`, and `ply=5`, we get the following...

![`Yarn` curve with ply=1](fabric-ply1.png)
![`Yarn` curve with ply=2](fabric-ply2.png)
![`Yarn` curve with ply=5](fabric-ply5.png)

This hash not only preserves locality, but does so with a very regular pattern. It's a fractal that fills up an entire $2^{\textsf{ply}} \times 2^{\textsf{ply}}$ integer space!

4. **Attempt 2**: Either by recognizing the curve or reading up online or by recognizing the properties (locality-preserving hashes and/or space-filling curves), there's a very common curve that satisfies all the properties you've observed so far. The "upside down U" Hilbert curve looks exactly like this, and Wikipedia literally gives you the code for how to invert $(x,y)$ back to $d$. Find the code (or re-discover) that inverts the "hash", invert the point in `hash.txt`, convert the integer back into the string, and you have the flag!

Admittedly there's some leaps of logic in this challenge to solve it this way. But there's another way to solve it that doesn't expect you to necessarily know anything about locality-preserving hashing or Hilbert curves...

## Unintended Solutions

#### Divide and Conquer

An alternate approach which works (and, in retrospect, makes for a much better writeup) would be to perform divide and conquer, comparing the candidate hash-point with the flag's hash-point to see which quadrant/subcurve you need to consider next. The below is untested, but it looks something like the following for a 1D window `[a, b]` and quadrant size `quad = (b+1-a)//4` to consider at each step:

0. Initialize the first candidate as the middle dot `cdot = yarn.n_winds // 2` in the 1D window `[a, b] = [0, yarn.n_winds-1]`, which should be the first dot to the right of the middle "bridge" connecting the left-right subcurves. Smallest dot in lower-left, largest in lower-right.
1. Then compute `(cx, cy) = fold(cdot)` (i.e. `hash_to_curve` with an integer input) and recursively compare with the hash of the flag `(x, y)`:
2. **Base case**: If `(cx = x) and (cy = y)`, then convert `cdot` into a string for the flag. The fact that the integer representation of the flag was taken modulo `n_winds` turns out to not matter here since the flag is small: it was just there for general correctness.
3. **Upper-right**: Else if `(cx >= x) and (cy >= y)`,  reduce the 1D window to `[cdot, cdot + quad - 1]`. Set `cdot = += quad // 2`, and repeat.
4. **Upper-left**: Else if `(cx < x) and (cy >= y)`,  reduce the 1D window to `[cdot - quad, cdot - 1]`. Set `cdot = -= quad // 2`, and repeat.
5. **Lower-right**: Else if `(cx >= x) and (cy < y)`, reduce the 1D window to `[cdot + quad, b]` and set `cdot = (cdot + quad) + quad // 2`. Rotate clockwise $90^\circ$, flip symmetrically parallel to $y$-axis (i.e. 1D goes opposite direction), and repeat.
6. **Lower-left**: Else `(cx < x) and (cy < y)`, reduce the 1D window to `[a, cdot - quad - 1]` and set `cdot = (cdot - quad) - quad // 2`. Rotate counter-clockwise $90^\circ$, flip symmetrically parallel to $y$-axis, and repeat.

This is a moderately difficult divide-and-conquer problem which is at least as difficult as the boring "solution" I gave above of finding and implementing the curve's inversion; you need to instead determine this curve's rotate and flip operations (some of the functions are already given :). So, if someone wants to take the pure leetcode route to a solution, I respect that.

(Discovering purely algorithmic solutions like this which offered little-to-no crypto insight was part of the reason this wasn't an easy "bad hash" `crypto` challenge...)

#### Reverse Engineering

I tried to give as many hints as I could about the curve to work with (analogy of seeing where a dot ends up on a piece of yarn woven into a 2D space = space-filling, keyword drops of "space", "curve", "hash", "fold", and "flip", `render_fabric` visualizing the curve for you, etc.) so that people would have recognizable keywords and curve figures to search for online if they got lost. However, if you don't recognize the curve you can also just read the `Yarn` implementation super closely, deduce that it's invertible, then blindly reverse-engineer this function's inversion based on the code alone.

#### Hillclimb Algorithm?

I'm unsure whether it's possible to perform a clever hillclimb / nearest-neighbor / etc. algorithm. I wasn't able to figure out an objective function to "zero" in on what integer corresponding to `FLAG` hashed to the point in `hash.txt`. I feel like there's something you could try here that works, but I'm no expert with optimization techniques like this.

**Naive approach**: Perhaps you could start somewhere random in 1D, hash your candidate to a point on the curve, incorporate 2D distance somehow (since the point in `hash.txt` is the only "ground truth" you have to compare to) then iterate until you hopefully reach the integer for `FLAG` that exactly hashes to the point.

However, I suspect this won't work because, while hashes such as these are locality preserving from input to output (here, 1D to 2D), the inverse (i.e. 2D to 1D) won't always hold. For example, looking at the `ply=5` example above, suppose the hash is $H(\texttt{FLAG}) = (x^\ast, y^\ast) = (16, 0)$. After performing naive hillclimb (i.e. minimal 2D distance as objective function via gradient descent) an attacker might find a "good" input $\hat{d}$ such that e.g. $H(\hat{d}) = (15, 0)$ with $d_2((15, 0), (x^\ast, y^\ast)) = 1$. Despite this small distance between points, the 1D integers $\hat{d}$ and $\texttt{FLAG}$ are extremely far from each other. 

So, how do you also encode in the objective function that the candidate dot should also be close when you don't know the integer flag to begin with...? Could you penalize 1D solutions to avoid being nearby large "jumps" in 2D? Use Hamming distance on Gray codes of each point on the curve somehow?

## Additional Resources
- **Hilbert Curve** ([Wikipedia](https://en.wikipedia.org/wiki/Hilbert_curve)): Contains a lot of information about a very common **NON-cryptographic** space-filling curve, as well as the base C code I used as a reference implementation.
- **Locality-preserving hashing** (LPH; [Wikipedia](https://en.wikipedia.org/wiki/Locality-sensitive_hashing#Locality-preserving_hashing)): A **NON-cryptographic** hashing technique which ensures that relative distance between similar inputs is preserved after hashing. This Hilbert curve-based hash construction is one of many examples.
