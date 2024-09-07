#!/bin/bash
#num=$1

if [[ $# != 1 ]]; then
	printf "Not enough arguments"
	exit 0
fi

for i in {1..100..3};do
	printf "%0"$1"d\n" $i
	#echo i
done
