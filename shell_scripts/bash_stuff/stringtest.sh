#!/bin/bash

first_string=$1
second_string=$2


if [[ ! -n $first_string || ! -n $second_string ]]; then
	echo "One of the strings was empty"
	exit 2
elif [[ -n $first_string || -n $second_string ]]; then
	if [[ ! $# == 2 ]]; then
		echo "Not enough arguments"
		exit 1
	elif [[ $# == 2 ]]; then 
		if [[ $first_string < $second_string ]];then
			#echo "First was longer"
			echo "${#first_string}"
		elif [[ $first_string > $second_string ]];then
			#echo "Second string was longer"
			echo "${#second_string}"
		elif [[ $first_sting == $second_sting ]];then
			exit 0
			fi
	fi
fi
