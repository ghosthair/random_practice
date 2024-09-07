#!/bin/bash
cat $1 | awk -F',' '{ lines++; print "Line " NR " has " NF " columns"} END {print "Total lines: "lines }' 
