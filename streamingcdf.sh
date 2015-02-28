#!/bin/bash
binary_path=`dirname $0`
for i in `seq 1 100`
    do
        ${binary_path}/coopsplit.py $1 $(($i*5))
        if [ $? -eq 1 ]; then
            echo "End"
            break
        fi
        ${binary_path}/coopread.py > $2/$(($i*5)).csv
        #echo "$(($i*5))"
    done
