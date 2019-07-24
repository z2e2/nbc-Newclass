#!/bin/bash

EXEC_ROOT=/lustre/scratch/zz374/nbc_new_class_detection/NB.run
GEN_SRC=$1
GEN_TEST=$2
FOLD=$3
KMERSIZE=$4
NTHREADS=$5
YEAR=$6
MEMLIM=$(($NTHREADS * 5000000)) # 160GB for 16 cores: 10 GB/core - 5 GB/class
echo "Classifying on fold $FOLD."

$EXEC_ROOT classify $GEN_TEST/fold$FOLD -s $GEN_SRC/$YEAR/save_$FOLD -t $NTHREADS -k $KMERSIZE -p 1 -r $YEAR-$FOLD.csv
