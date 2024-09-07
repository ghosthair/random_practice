#!/bin/bash

#Zip Code
cat $1 | sed -r "s/([0-9]{5,9})/Zip Code: \1/"
#Phone
cat $1 | sed -r "s/([0-9]{3}-[0-9]{3}-[0-9]{4})/Phone Number: \1/"
#Name
cat $1 | sed -r "s/(^[A-Z][a-z]+) ([A-Z \.)([A-Z][a-z]+)/Name: \1 \2/"
#IP
cat $1 | sed -r "s/([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)/IP: \1/g"
#Url, need review
cat $1 | sed -r "s/(http+)/Url: \1/g"
