
#!/bin/bash
#The cut tool can assist with taking in the delimiter
<<<<<<< HEAD

if [[ $# != 3 ]]; then
	echo "Please have the 3 arguments, 'File', 'Delimiter', and the 'Column' number."
fi
infile=$1
delimiter=$2
column=$3
=======
infile=$1
delim=$2
column=$3

if [[ $# != 3 ]]; then
	echo "Please provide three arguments, the file name, the delimiter and the coulmn you would like to perfom the math on."
fi

>>>>>>> e62eac8 (Updating from Desktop)
declare -a filearray
readarray filearray <$infile
numlines=${#filearray[@]}
grad=0
count=0
high=0
low=100
lowest_grade=""
highest_grade=""

<<<<<<< HEAD

=======
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
>>>>>>> e62eac8 (Updating from Desktop)
