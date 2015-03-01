#!/bin/bash

inputdir=$1
num=0
for file in ${inputdir}/*.txt
    do
    sed "s;FILENUM;$file;g" plt | sed "s/PLOTNUM/$num/" | gnuplot
    num=$((num+1))
    done
