import os

old_path = os.getcwd()
os.chdir(os.path.dirname(__file__))
with open('../solve/flag.txt', 'rt') as f:
    FLAG = f.readline().strip()
os.chdir(old_path)
