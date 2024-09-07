#!/bin/bash

function pingHostQuiet {
	ping -c 1 -q -W1 $1 1>/dev/null 2>/dev/null
	if [[ $? == 0 ]]; then
		printf "$1 is ALIVE\n"
	fi
}

host=$1

for i in {0..255}; do
	pingHostQuiet $host.$i &
done
wait 

