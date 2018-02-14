#!/bin/bash

cat configs/examples.conf | while IFS='' read -r line || [[ -n "$line" ]]; do 
	if [[ ! $line =~ ^#.* && $line != "" ]]; then
		echo "Changing: $line"
		echo $line > light.conf
		sleep 10
	fi
done
