#!/bin/bash

if [[ $# < 2 || $# > 2 ]];then
	echo "Error: Only takes in two numbers"
	exit
fi

FIRST=$1
SEC=$2
THIRD=$(($FIRST*$SEC))
echo $THIRD
