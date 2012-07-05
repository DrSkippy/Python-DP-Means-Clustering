#!/usr/bin/env bash

cd /Users/scotthendrickson/IdeaProjects/Python-DP-Means-Clustering

for i in 2 3 4 5 8 10 12 15 18 20; do
 echo "calculating min errors in $i iterations..."
 cmd="./test.py -i$i | tee ./output/test.$i.csv | grep -v Inter > ./output/test.csv"
 eval $cmd
 ./plotTest.r
 mv ./img/test_times-error.png ./img/test_times-error_$i.png
done
