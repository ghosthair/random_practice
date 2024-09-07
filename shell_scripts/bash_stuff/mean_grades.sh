#!/bin/bash

if [[ $# != 3 ]]; then
	echo "Please provide three arguments, the file name, the delimiter and the coulmn you would like to perfom the math on."
fi

infile=$1
delim=$2
column=$3

declare -a filearray
readarray filearray <$infile
numlines=${#filearray[@]}
grad=0
count=0
high=0
low=100
lowest_grade=""
highest_grade=""

while [[ "$count" -lt "$numlines" ]]; do
	line="${filearray[$count]}"

	grades=$(echo "$line" | cut -d "$delim" -f "$column")

	grad=$(($grad + $grades))

	if [[ $grades -gt $high ]]; then
		high=$grades
		highest_grade="$line"
	fi

	if [[ $grades -lt $low ]]; then
		low=$grades
		lowest_grade="$line"
	fi
	count=$(($count + 1))
done

mean=$(echo "scale=2; $grad/$numlines" | bc)
echo "Mean: $mean"
echo "Highest grade: $highest_grade"
echo "Lowest grade: $lowest_grade"
