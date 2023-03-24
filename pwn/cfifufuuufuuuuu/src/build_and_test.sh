#!/bin/bash

rm ../solve/flag.txt
cp flag.txt ../solve/flag.txt

rm input_exploit
rm input_exploitfail
rm ../solve/input_exploit
python3 ./build_inputs.py
cp input_exploit ../solve/input_exploit
cp input_exploitfail ../solve/input_exploitfail

rm ../dist/s
rm ../deploy/s
gcc -O1 -no-pie -nostdlib s.c -o s
strip -s s

rm ../dist/loader.pyc
rm ../deploy/loader.pyc
python3 -c 'import py_compile; py_compile.compile("loader.py")'
cp __pycache__/loader.cpython-36.pyc loader.pyc
rm -r __pycache__

if python3 ./test_benign.py; then
    true #
else
    echo "ERROR test_benign"
    exit 1
fi


cat input_exploitfail | python3 ./loader.pyc | grep -A 3 -B 3 -a "Stack"
if [[ $(cat input_exploitfail | python3 ./loader.pyc | grep -a "Stack") ]]; then
    true #echo "SUCCESS"
else
    echo "ERROR exploitfail"
    exit 1
fi

cat input_exploit | python3 ./loader.pyc | grep -a "bctf{"
if [[ $(cat input_exploit | python3 ./loader.pyc | grep -a "bctf{") ]]; then
    echo "SUCCESS"
else
    echo "ERROR exploit"
    exit 1
fi


cp loader.pyc ../dist/loader.pyc
cp loader.pyc ../deploy/loader.pyc
cp s ../dist/s
cp s ../deploy/s


