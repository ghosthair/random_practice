#!/bin/bash

for i in {1..3}; do
	#parallel nc -p20-25 192.186.1.$1 ;
	echo nc -nvzw 1 192.168.1.$i 20-24
done | parallel 
