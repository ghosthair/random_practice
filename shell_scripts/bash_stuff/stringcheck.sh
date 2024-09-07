#!/bin/bash
first=$1
second=$2

if [[ $second =~ .*$first.* ]]; then
	echo "$first is a substring of $second"
fi
