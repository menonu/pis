#!/bin/bash

a=`/bin/date '+%F-%R'`
mkdir $a 
for i in `seq 10` 
do
    python cdf_rand.py ../data/positionfixed-USRP-20150212/forDatabase_20150212-100516.csv '2015/2/12 10:5:28' '2015/2/12 12:7:55' 5 > $a/${i}.csv
done
