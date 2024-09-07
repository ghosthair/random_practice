#!/bin/bash

while read line; do
	url=$( echo $line | jq ".url" )
	status=$(echo $line | jq ".status" )
	#curl_status=$( curl -s -w "%{http_code}\n" -o /dev/null "$url")
	curl_status=$(curl -s -w "$url")
	#if [[ status -ne curl_status ]]; then
	#	echo "Here is the url $url and the new status $curl_status"
	#fi
	echo "URL: $url"
	echo "Status: $status"
	#echo "New Status: $curl_status"
done
