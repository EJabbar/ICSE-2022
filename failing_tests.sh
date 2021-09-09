#!/bin/bash

pname=$1
version=$2

cd ./projects/${pname}_${version}
defects4j export -p tests.trigger > ../../failing_tests/failing_${pname}_${version}.txt
cd ../..
