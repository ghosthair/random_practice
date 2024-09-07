#!/bin/bash

date_1=`date +%s`

# Using this block would add extra time for the script to run
#echo "How long do you want to sleep for (in seconds)? "
#read sleep_time

sleep_time=$1

sleep $sleep_time

date_2=`date +%s`

date3=$((date_2 - date_1))
echo "I'm awake after $date3 second(s)"

