#!/bin/bash
count=0

for dir in $(ls); do
#	echo "$dir"
	((count++))
#	echo $count
done
#echo "Total files: $count"

if [[ $count -lt 10 ]]; then
	echo "Less than ten files";
elif [[ $count -gt 10 ]]; then
	echo "More than ten files"
else
	echo "Corrent number of files"
fi
