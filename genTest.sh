#!/bin/bash

size1=$1
size2=$2
blockSize=$3

command_default="-R $size1 -C $size2 -B $blockSize --mode exclusive"

echo "skinny"
python3 ./util/gen_skinny.py $command_default

echo "long"
python3 ./util/gen_long.py $command_default

echo "stair"
python3 ./util/gen_stair.py -R $size1 -C $size2 -B $blockSize -P 3 --mode exclusive

echo "zigzag"
python3 ./util/gen_zigzag.py $command_default

echo "twoline_col"
python3 ./util/gen_twoline_col.py $command_default

echo "twoline_row"
python3 ./util/gen_twoline_row.py $command_default
