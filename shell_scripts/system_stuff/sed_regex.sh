#!/bin/bash 
#Syslog break down, username between timestamp and from
#Need to print the IP, Port and Username

cat $1 | sed -r 's/([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{9}) (Invalid user) ([A-Za-z0-9_]+) (from) ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+) (port) ([0-9]+)/Username: \3, IP: \5 Port: \7/'
