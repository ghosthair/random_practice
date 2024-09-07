#!/bin/bash
#Taking in a file as a command line argument
#infile=$1
infile=alice.txt
declare -a filearray
readarray filearray <$infile
numlines=${#filearray[@]}
count=0
thes=0

while [[ "$count" -lt "$numlines" ]]; do
	line="${filearray[$count]}"
	result=$(echo "$line" | grep -o 'the' | wc -l)

	if [[ $result -gt 0 ]]; then
		echo "The number of 'the's in this line: $result. $line"
	fi

	thes=$(($thes + result))
	count=$((count + 1))
done
echo "The total number of the's: $thes"
