#!/bin/bash
#while read line;do echo $line | python3 -m json.tool;done <<< $(head du.json) | grep 'url' | grep -v 'urlkey' | awk -F '"' '{ print $4 }'
while read line; do
	url=$(echo $line | python3 -m json.tool | grep 'url' | grep -v 'urlkey' | awk -F '"' '{ print $4 }')
	status=$(echo $line | python3 -m json.tool | grep 'status' | grep -v 'urlkey' | awk -F '"' '{ print $4 }') 
	#curl_status=$(curl -s -w "%{http_code}\n" "$url" )
	curl_status=$(curl -s -w "%{http_code}\n" $url -o /dev/null)
	echo "The url is $url, the status is $status"
	#echo "The current status is $curl_status"
	if [[ $status -ne $curl_status ]]; then
		echo "The current status for $url is $curl_status";
	fi 
done

