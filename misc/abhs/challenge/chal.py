import os

def filter(w):
   return "".join([ c   for c in w  if ord(c) < 0x80 ])


print("== A Bonkers Homemade Shell ==")

while True:
   l = input("$ ")

   if "(" in l or ")" in l: 
      print("don't be naughty!")
      continue

   words = l.strip().split()
   cmd = " ".join( [ "".join(sorted(filter(w)))  for w in words] )
   os.system(cmd)
