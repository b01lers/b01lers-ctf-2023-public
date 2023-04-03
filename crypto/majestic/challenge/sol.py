# collects useful ciphertexts, stores those in file
#


from pwn import *
import sys
import math
import datetime
import numpy as np


cache = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 
107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 
233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 
373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 
509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 
659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 
823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 
983, 991, 997]

def makeStamp(t):  return int( "".join( str(t)[:-3].translate({45: ' ', 46: ' ', 58: ' '}).split()[::-1] ) )

def getWeights(t): 
   stamp = makeStamp(t)
   return sorted(cache, key = lambda v: abs(math.sin(math.pi * stamp / v)))

def solveForTime(t0, credits, pgoal, qgoal):
   i = 0
   dt = 0.
   good = []
   goal = None
   while i < 40000:   # search up to +- 40 secs
      t = t0 + datetime.timedelta(seconds = dt)
      weights = getWeights(t)
      p, q = weights[:2]
      if (p,q) == (pgoal, qgoal) and goal == None: goal = t
      c = sum(weights[-29:])
      if c == credits:  good.append(t)
      if dt > 0:   dt = -dt
      else:
        dt = i * 1e-3
        i += 1
   # return times
   return good, goal



def connect():
   #r = process(["python3", "chal.py"])
   r = remote("majestic.bctf23-codelab.kctf.cloud", 1337)
   in1 = r.recvuntil(b">").strip().split()
   #print(f"# {in1}")
   credits = int( in1[-3] )
   return r, credits


# get ctxts for p,q = 3,7 in one connection
def collectOneBatch(t0, pgoal, qgoal):

   results = []

   # connect
   r, credits = connect()

   # solve for possible timestamps and suitable timestamp for p,q = pgoal,qgoal
   times, goal = solveForTime(t0, credits, pgoal, qgoal)
   print(f"#TIMES: {[ str(t) for t in times]}")
   print(f"#GOAL: {goal}")

   if goal == None:
      print("#->NO GOAL")
      return results

   MINGAP = 2.0  # super conservative!
   if len(times) == 0 or (len(times) > 1 and abs( (times[0] - times[1]).total_seconds() ) < MINGAP):
      print("#->TIMES BAD/RISKY")
      return results

   # "buy time" to shift to suitable timestamp
   dt = (goal - times[0]).total_seconds()
   print(f"#dt={dt}")

   MAXSHIFT = 5.
   while dt != 0:
      shft = dt   if abs(dt) <= MAXSHIFT   else  math.copysign(MAXSHIFT, dt)
      print(f"#shft={shft}")
      r.send( f"3\n{shft}\n".encode() )
      r.recvuntil(b">")
      dt -= shft

   # generate flag encryptions until we run out of money
   Nbatch = 10
   try:
      while True:
         r.send( b"2\n" * Nbatch)
         for _ in range(Nbatch):
            c = r.recvuntil(b">").strip().split()[0]
            results.append(c.decode())
   except EOFError:
      r.close()

   return results


# get all ctxts we need through multiple connections
def collectAllCtxts(Ntot, pgoal, qgoal, fname):
   n, round = 0, 0
   ctxts = []
   f = open(fname, "w")   if fname   else   None
   while n < Ntot:
      round += 1
      t0 = datetime.datetime.utcnow()
      print(f"#ROUND {round}: {t0}")

      ctxtBatch = collectOneBatch(t0, pgoal, qgoal)
      if f: 
         for c in ctxtBatch:  f.write(c + "\n")
         f.flush()

      ctxts += ctxtBatch
      n += len(ctxtBatch)
      print(f"#TOTAL {n}/{Ntot}")
   #
   return ctxts



context.log_level = 'ERROR'

# read params

Ntot = int(sys.argv[1])    # if Ntot <= 0 then use the ctxt file as is, do no data collection
pgoal = int(sys.argv[2])
qgoal = int(sys.argv[3])
freqFile = sys.argv[4]
ctxtFile = sys.argv[5]  if len(sys.argv) > 5   else   None

#####
# get flag encryptions
#####

if Ntot > 0:  ctxts = collectAllCtxts(Ntot, pgoal, qgoal, ctxtFile)
else:  ctxts = open(ctxtFile, "r").read().strip().split("\n")

#####
# break ctxts
#####

Nflag = len(ctxts[0]) // 4

print(f"#{len(ctxts)} encryptions")
print(f"# flag has {Nflag} chars")

# byte frequencies in ctxts
#
# counts[n,i] gives freqs for flag byte i

countsLO, countsHI = np.zeros((256, Nflag)), np.zeros((256, Nflag))
for c in ctxts: 
   for i in range(Nflag):
      val = int(c[i*4:(i+1)*4], 16)
      countsLO[(val & 0xff), i] += 1
      countsHI[val >> 8, i] += 1

# read expected freqs, convert to log(P)
#
# logPs[k,n] gives ln P(k->n)   

data = open(freqFile, "r").read().strip().split("\n")
probs = [ [int(v)  for v in l.split()[1:]]   for l in data    if not "#" in l ]
for row in probs:
   norm = 1. / sum(row)
   for n in range(len(row)):  row[n] *= norm

p0 = 1e-6
logPs = np.array( [ [math.log(p + p0) for p in row] for row in probs ] )


# get flag via max likelihood
#
scLO = np.matmul(logPs, countsLO)     # logPs[k,n] * counts[n,i]  matrix product
scHI = np.matmul(logPs, countsHI)
flag = ""
for i in range(Nflag):
   scores = [  (k, scLO[k ^ 0xbc, i] + scHI[k, i])   for k in range(32, 128) ]
   scores.sort(key = lambda v: -v[1])
   #print(i, scores[:10])
   flag += chr(scores[0][0])
   print(flag)
