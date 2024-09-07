#!/bin/bash
for i in {1..254}; do
	echo 192.168.226.$i;
done | parallel check_ping.sh {}
