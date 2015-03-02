#!/bin/bash
binary_path=`dirname $0`
inputdir=$1
outputdir='.'
outputdir=$2
for file in ${inputdir}/*.dat
    do
        ${binary_path}/head1sec.py ${file} ${outputdir}
    done
