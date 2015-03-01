#!/bin/bash
binary_path=`dirname $0`
duration=3
for i in `seq 1 100`
    do
        ${binary_path}/coopsplit.py $1 $(($i*$duration)) $duration
        if [ $? -eq 1 ]; then
            echo "End"
            break
        fi
        ${binary_path}/coopread.py $duration > $(($i*duration)).csv
        #echo "$(($i*5))"
    done
