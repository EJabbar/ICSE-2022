#!/bin/bash

pname=$1
version=$2

defects4j checkout -p $pname -v ${version}b -w ./projects/${pname}_${version}
