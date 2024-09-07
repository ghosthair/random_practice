#!/bin/bash

if [[ $# != 2 ]]; then
	echo "Please only use two arguments"
	exit
fi

function add {
	math=$(($1 + $2))
	echo $math
}


function multiply {
	math=$(($1 * $2))
	echo $math
}

function factorial {
	num=$1
	math=1
	while [[ $num -gt 1 ]]; do
		math=$((math * num))
		num=$((num - 1))
	done
	echo $math
}

retval_add=$(add $1 $2)
retval_mult=$(multiply $1 $2)
retval_fact=$(factorial $1)
echo $retval_add
echo $retval_mult
echo $retval_fact
