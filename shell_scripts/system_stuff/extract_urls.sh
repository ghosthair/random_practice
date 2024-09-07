#!/bin/bash
#while read line;do echo $line | python3 -m json.tool;done <<< $(head du.json) | grep 'url' | grep -v 'urlkey' | awk -F '"' '{ print $4 }'
while read line; do
	url=$(echo $line | python3 -m json.tool | grep 'url' | grep -v 'urlkey' | awk -F '"' '{ print $4 }')
	status=$(echo $line | python3 -m json.tool | grep 'status' | grep -v 'urlkey' | awk -F '"' '{ print $4 }') 
	#echo "The urs is $url, the status is 500"
	echo "The url is $url, the status is $status"
done

