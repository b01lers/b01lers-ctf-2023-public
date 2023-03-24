#!/bin/bash

echo "Select challenge:"
echo "1) Noah"
echo "2) Noah-golf"
echo -n "> "

./readint
choice=$?

case $choice in
        "1")
            NROWS=20
            FLAGFILE=flag.txt 
            ;;
        "2")
            NROWS=10
            FLAGFILE=golf_flag.txt
            ;;
        *) echo "quitting"
           exit 0
esac

./noah $NROWS $FLAGFILE

