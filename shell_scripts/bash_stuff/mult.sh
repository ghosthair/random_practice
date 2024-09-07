#!/bin/bash

FIRST="2"
SEC="3"
THIRD=$(($FIRST * $SEC))
echo $THIRD

sleep 1

echo "Pick a number."
read FORTH
echo "Pick a second number"
read FIFTH
SIXTH=$((FORTH*FIFTH))
echo $SIXTH
