#!/bin/bash

id=$1
tid=$2
name=$3
pname=$4

cd ./projects/${pname}_${id}

defects4j coverage -t ${name} > coverage.txt
cp coverage.xml ../../coverage_files/coverage_${pname}_${id}_${tid}.xml
cp coverage.txt ../../coverage_files/coverage_${pname}_${id}_${tid}.txt
cd ..