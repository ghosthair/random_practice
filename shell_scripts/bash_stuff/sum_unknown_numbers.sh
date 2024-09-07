#!/bin/bash

num=0

while [[ $# -gt 0 ]]; do
	num=$(echo "$num + $1" | bc -l)
	shift
done

echo "The sum of all the args:$num"

