#!/bin/bash

pname=$1
version=$2

cd ./projects/${pname}_${version}
defects4j coverage -r
cp all_tests ../../relevant_tests/relevant_${pname}_${version}.txt
cd ../..