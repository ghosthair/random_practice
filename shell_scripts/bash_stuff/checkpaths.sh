#!/bin/bash
for f in /etc/{skel, network , host{s,""}, resolv.conf,passwd, shadow}; do
	#echo "file $f";
	#echo $f
	if [[ -f $f ]]; then
		echo "$f is a file";
	elif [[ -d $f ]]; then
		echo "$f is a directory";
	elif [[ ! -e $f ]]; then
		echo "$f does not exist"
	else
		echo "It exists but is not a file or directory"
	fi
done


#Needs more work
