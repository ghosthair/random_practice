#!/bin/bash

$(sleep 30) &
sleeppid=$!
echo "Sleeping pid is $sleeppid"
sleep 2
$( kill $sleeppid)
