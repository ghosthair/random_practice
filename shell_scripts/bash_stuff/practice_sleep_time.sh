#!/bin/bash

START=$(date +%s)
echo "Started at $START"

sleep 1 &
sleep 10
sleep 2
sleep 5 &

END=$(date +%s)
DELAY=$(($END - $START))

wait
echo "Sleep slept for $DELAY seconds"
