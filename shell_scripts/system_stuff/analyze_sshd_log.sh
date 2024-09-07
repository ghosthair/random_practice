#!/bin/bash 

echo $(python3 analyze_sshd_python.py $1)

#All of this is generated from the python script as well, just added here
#	for convience as well.

#Question 1:  See output lists

#Question 2: 4038 failed with kex_exchange_identification phase
#		3976 errors were closed by remote host

#Question 3: 18674 errors were preauth
#	7189 were invalid user
#	4475 were auth fail

#Question 4: 4475 were username but not preauth error

#Question 5: 43 invalid protocol

#Question 6: 2937 successful logins.
#From the informaiton gathered here some attackers were able to get in
#This assumption is made from the successful IP address that were logged in also
#showing as a previous login attempt from a previous search on the regex logs.
