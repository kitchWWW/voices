#!/bin/bash
mkdir out/$1
python go.py $1 $2 $3
rm out/$1/*.wav