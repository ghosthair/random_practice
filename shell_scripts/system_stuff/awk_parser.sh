#!/bin/bash
echo 'flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST>mtu 1500' | awk -F'<' '{ print $2 }' | awk -F'>' '{ print $1 }'
