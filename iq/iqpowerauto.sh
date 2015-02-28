#!/bin/bash
binary_path=`dirname $0`
inputdir=$1
outputdir=$2
for file in ${inputdir}/*.dat
    do
        ${binary_path}/powervstime.py ${file} ${outputdir}
    done
