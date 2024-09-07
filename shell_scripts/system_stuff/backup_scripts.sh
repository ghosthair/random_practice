#!/bin/bash

find $1 -name '*.sh' | xargs tar -cJf backup_scripts.tar.xz 
