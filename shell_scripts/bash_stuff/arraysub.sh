#!/bin/bash

MYARRAY=("You cannot shake hands with a
clenched fist." "Whoever is happy will make others happy too." "Let
us be grateful to people who make us happy." "Very little is needed to
make a happy life." "Be happy for this moment. This moment is your
life.")

for i in {0..4}
do
	echo ${MYARRAY[$i]//happy/sloppy}
	#echo ${MYARRAY[1]//happy/sloppy}
done
