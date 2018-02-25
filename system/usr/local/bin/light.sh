#!/bin/bash

cp /etc/light-strip/startup.conf /etc/light-strip/light.conf

function loop() {
	cp /var/log/light.log /var/log/light.log.0
	python /home/pi/rpi_ws281x/python/examples/double-circle-50-24-2.py > /var/log/light.log
	echo $! > /tmp/light-strip.pid
	loop
}

loop
