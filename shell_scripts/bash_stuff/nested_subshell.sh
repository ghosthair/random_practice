#!/bin/bash

echo "My first level is here $BASH_SUBSHELL"

	(echo "Hello this is the next level for the subshell:$BASH_SUBSHELL" 
		(echo "This is the second level:$BASH_SUBSHELL"
			(echo "This is the third level:$BASH_SUBSHELL")
	)
)
