#!/bin/bash

inputdir=$1
num=0
for file in ${inputdir}/*.txt
    do
        string='pic'${file##*/}
        sed "s;FILENUM;$file;g" $2 | sed "s/PLOTNUM/${string%.*}/" | gnuplot
    num=$((num+1))
    done
