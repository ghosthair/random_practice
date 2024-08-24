#!/bin/bash 

echo $(python3 analyze_sshd_python.py $1)

#The partner script in python will join this one in the bash dir since it calls it, there will be a copy in the py as well.
