#!/bin/bash
#Use mktemp -u, gives name and doesn't make file
arg1=$1
arg2=$2

for i in $(eval echo {1..$arg1}); 
do
	temp_dir=$(mktemp -u -d)
	echo $(ln "$arg2" "$temp_dir")

done
