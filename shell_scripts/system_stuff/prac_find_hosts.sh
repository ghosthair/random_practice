#!/bin/bash

#host/subnet discovery
#Assume a /24 network

function pingHostQuiet {
	ping -c 1 -q -W1 $1 1>/dev/null 2>/dev/null
	echo $?
}

host=$1
interval=$2
count=0
alive=0

while true;do
	echo "Ping $host $count"
	((count++))
	ret=$(pingHostQuiet $host)
	if [[ ! $ret -eq 0 ]]; then
		echo "Host $host failed to respond to ping ($alive/$count) successful"
	else
		((alive++))
	echo "Host $host responded to ping ($alive/$count) successful"
	fi
	sleep $interval
done


