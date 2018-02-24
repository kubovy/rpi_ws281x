# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
import json
from collections import namedtuple

from neopixel import *
import subprocess

import argparse
import signal
import sys

import os
import platform

def signal_handler(signal, frame):
        colorWipe(strip, Color(0,0,0))
        sys.exit(0)

def opt_parse():
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', action='store_true', help='clear the display on exit')
        args = parser.parse_args()
        if args.c:
                signal.signal(signal.SIGINT, signal_handler)

def Color(red, green, blue, white = 0):
	"""Convert the provided red, green, blue color to a 24-bit color value.
	Each color component should be a value 0-255 where 0 is the lowest intensity
	and 255 is the highest intensity.
	"""
	return (white << 24) | (red << 8)| (green << 16) | blue

def Color2(color):
        """Color2"""
        return Color(color.red, color.green, color.blue)

# LED strip configuration:
LED_COUNT      = 50      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering
CONF_PATH      = '/etc/light-strip/'
#CONF_PATH      = '/mnt/mass-storage/light-strip/'
#REBOOT_PATH   = '/mnt/mass-storage/restart-light-strip'


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)

def theater(strip, color1, color2, color5, color6, wait_ms=50, iterations=10):
	"""Movie theater light style chaser animation."""
        half = (strip.numPixels() - 2) / 2
        strip.setPixelColor(strip.numPixels() - 1, color5)
        strip.setPixelColor(strip.numPixels() - 2, color6)
	for j in range(iterations):
		for q in range(3):
			for i in range(0, half, 3):
				strip.setPixelColor(i+q, color1)
				strip.setPixelColor(i+q+half, color2)
			strip.show()
			time.sleep(wait_ms/1000.0)
                        for i in range(0, half, 3):
				strip.setPixelColor(i+q, 0)
				strip.setPixelColor(i+q+half, 0)

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
	"""Draw rainbow that fades across all pixels at once."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
	"""Draw rainbow that uniformly distributes itself across all pixels."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
	"""Rainbow movie theater light style chaser animation."""
	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, wheel((i+j) % 255))
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)
# Mine

def wipe(strip, color1, color2, color5, color6, wait_ms=50, sleep=0):
	"""Wipe color across display a pixel at a time."""
	half = (strip.numPixels() - 2) / 2
        strip.setPixelColor(strip.numPixels() - 1, color5)
        strip.setPixelColor(strip.numPixels() - 2, color6)
	for i in range(half):
		strip.setPixelColor(i, color1)
		strip.setPixelColor(i + half, color2)
		strip.show()
		time.sleep(wait_ms/1000.0)
	if sleep > 0:
		time.sleep(sleep/1000.0)
		wipe(strip, Color(0, 0, 0), Color(0, 0, 0,), color5, color6, wait_ms, 0)

def light(strip, color1, color2, color5, color6, wait_ms=50):
	half = (strip.numPixels() - 2) / 2
        strip.setPixelColor(strip.numPixels() - 1, color5)
        strip.setPixelColor(strip.numPixels() - 2, color6)
	for i in range(half):
		strip.setPixelColor(i, color1)
		strip.setPixelColor(i + half, color2)
	strip.show()
        time.sleep(wait_ms/1000.0)

def rotation(strip, color1, color2, color5, color6, width=3, fade=0, wait_ms=50):
	"""Rotation"""
	half = (strip.numPixels() - 2) / 2
        strip.setPixelColor(strip.numPixels() - 1, color5)
        strip.setPixelColor(strip.numPixels() - 2, color6)
	for i in range(half):
		for j in range(half):
			strip.setPixelColor(j, Color(0, 0, 0))
			strip.setPixelColor(j + half, Color(0, 0, 0))
		for k in range(width):
		        white1 = (color1 & (255 << 24)) >> 24
			red1 = (color1 & (255 << 8)) >> 8
			green1 = (color1 & (255 << 16)) >> 16
			blue1 = (color1 & 255)
		        white2 = (color2 & (255 << 24)) >> 24
			red2 = (color2 & (255 << 8)) >> 8
			green2 = (color2 & (255 << 16)) >> 16
			blue2 = (color2 & 255)

			percent = 100.0 - float(width - k - 1) * float(fade)
			factor = percent / 100.0

			r1 = int(float(red1) * factor)
			g1 = int(float(green1) * factor)
			b1 = int(float(blue1) * factor)
			r2 = int(float(red2) * factor)
			g2 = int(float(green2) * factor)
			b2 = int(float(blue2) * factor)
			#print (str(percent) + ' -> ' + str(factor) + ': ' + str(r) + ', ' + str(g) + ', ' + str(b))

			c1 = Color(r1, g1, b1)
			c2 = Color(r2, g2, b2)

			p = i + k if (i + k < half) else (i + k) - half
			strip.setPixelColor(p, c1)
			strip.setPixelColor(p + half, c2)
		strip.show()
		time.sleep(wait_ms/1000.0)

def spin(strip, color1, color2, color5, color6):
	"""Spin"""
        strip.setPixelColor(strip.numPixels() - 1, color5)
        strip.setPixelColor(strip.numPixels() - 2, color6)
	for w in range(5):
		rotation(strip, color1, color2, 24, 4, 50 - (w * 10))
	rotation(strip, color1, color2, 24, 4, 50 - (w * 10))
	for w in range(3):
		lighthouse(strip, color1, color2, 12, 4, 30 - (w * 10))
		lighthouse(strip, color1, color2, 12, 4, 30 - (w * 10))
	light(strip, color1, color2)
	time.sleep(10)

def chaise(strip, color1, color2, color5, color6, width=3, fade=0, wait_ms=50):
	"""Rotation"""
	half = (strip.numPixels() - 2) / 2
	for i in range(half):
		for j in range(half):
			strip.setPixelColor(j, Color(0, 0, 0))
			strip.setPixelColor(j + half, Color(0, 0, 0))
		for k in range(width):
		        white1 = (color1 & (255 << 24)) >> 24
			red1 = (color1 & (255 << 8)) >> 8
			green1 = (color1 & (255 << 16)) >> 16
			blue1 = (color1 & 255)
		        white2 = (color2 & (255 << 24)) >> 24
			red2 = (color2 & (255 << 8)) >> 8
			green2 = (color2 & (255 << 16)) >> 16
			blue2 = (color2 & 255)

			percent = 100.0 - float(width - k - 1) * float(fade)
			factor = percent / 100.0

			r1 = int(float(red1) * factor)
			g1 = int(float(green1) * factor)
			b1 = int(float(blue1) * factor)
			r2 = int(float(red2) * factor)
			g2 = int(float(green2) * factor)
			b2 = int(float(blue2) * factor)
			#print (str(percent) + ' -> ' + str(factor) + ': ' + str(r) + ', ' + str(g) + ', ' + str(b))

			c1 = Color(r1, g1, b1)
			c2 = Color(r2, g2, b2)

			p = i + k if (i + k < half) else (i + k) - half
			q = half - (i + k) if (half - (i + k) >= 0) else (half - (i + k)) + half
			strip.setPixelColor(p, c1)
			strip.setPixelColor(q + half, c2)
                strip.setPixelColor(strip.numPixels() - 1, color5)
                strip.setPixelColor(strip.numPixels() - 2, color6)
		strip.show()
		time.sleep(wait_ms/1000.0)

			
def lighthouse(strip, color1, color2, color3, color4, color5, color6, width=3, fade=0, wait_ms=50):
	"""Lighthouse"""
	half = (strip.numPixels() - 2) / 2
	quarter = half / 2
        strip.setPixelColor(strip.numPixels() - 1, color5)
        strip.setPixelColor(strip.numPixels() - 2, color6)
	for i in range(half):
		for j in range(half):
			strip.setPixelColor(j, Color(0, 0, 0))
			strip.setPixelColor(j + half, Color(0, 0, 0))
		for k in range(width):
		        white1 = (color1 & (255 << 24)) >> 24
			red1 = (color1 & (255 << 8)) >> 8
			green1 = (color1 & (255 << 16)) >> 16
			blue1 = (color1 & 255)
		        white2 = (color2 & (255 << 24)) >> 24
			red2 = (color2 & (255 << 8)) >> 8
			green2 = (color2 & (255 << 16)) >> 16
			blue2 = (color2 & 255)
		        white3 = (color3 & (255 << 24)) >> 24
			red3 = (color3 & (255 << 8)) >> 8
			green3 = (color3 & (255 << 16)) >> 16
			blue3 = (color3 & 255)
		        white4 = (color4 & (255 << 24)) >> 24
			red4 = (color4 & (255 << 8)) >> 8
			green4 = (color4 & (255 << 16)) >> 16
			blue4 = (color4 & 255)

			percent = 100.0 - float(width - k - 1) * float(fade)
			factor = percent / 100.0

			r1 = int(float(red1) * factor)
			g1 = int(float(green1) * factor)
			b1 = int(float(blue1) * factor)
			r2 = int(float(red2) * factor)
			g2 = int(float(green2) * factor)
			b2 = int(float(blue2) * factor)
			r3 = int(float(red3) * factor)
			g3 = int(float(green3) * factor)
			b3 = int(float(blue3) * factor)
			r4 = int(float(red4) * factor)
			g4 = int(float(green4) * factor)
			b4 = int(float(blue4) * factor)
			#print (str(percent) + ' -> ' + str(factor) + ': ' + str(r) + ', ' + str(g) + ', ' + str(b))

			c1 = Color(r1, g1, b1)
			c2 = Color(r2, g2, b2)
			c3 = Color(r3, g3, b3)
			c4 = Color(r4, g4, b4)

			p = i + k if (i + k < half) else (i + k) - half
			q = p + quarter if (p + quarter < half) else (p + quarter) - half
			strip.setPixelColor(p, c1)
			strip.setPixelColor(p + half, c3)
			strip.setPixelColor(q, c2)
			strip.setPixelColor(q + half, c4)
		strip.show()
		time.sleep(wait_ms/1000.0)
			
def fade(strip, color1, color2, color5, color6, wait_ms=50, min=0, max=100):
	"""Fade"""
	half = (strip.numPixels() - 2) / 2

	white1 = (color1 & (255 << 24)) >> 24
	red1 = (color1 & (255 << 8)) >> 8
	green1 = (color1 & (255 << 16)) >> 16
	blue1 = (color1 & 255)
	white2 = (color2 & (255 << 24)) >> 24
	red2 = (color2 & (255 << 8)) >> 8
	green2 = (color2 & (255 << 16)) >> 16
	blue2 = (color2 & 255)
	#print ('Input: ' + str(red) + ', ' + str(green) + ', ' + str(blue))
        strip.setPixelColor(strip.numPixels() - 1, color5)
        strip.setPixelColor(strip.numPixels() - 2, color6)
	for pr in range((max - min + 1) * 2):
		percent = pr + min if ((pr + min) <= max) else max - (pr + min - max)
		factor = float(percent) / 100.0
		#print (str(pr) + ', ' + str(percent) + ', ' + str(factor))
		r1 = int(float(red1) * factor)
		g1 = int(float(green1) * factor)
		b1 = int(float(blue1) * factor)
		r2 = int(float(red2) * factor)
		g2 = int(float(green2) * factor)
		b2 = int(float(blue2) * factor)
		c1 = Color(r1, g1, b1)
		c2 = Color(r2, g2, b2)
		#print ('Color: ' + str(r) + ', ' + str(g) + ', ' + str(b))
		for i in range(half):
			strip.setPixelColor(i, c1)
			strip.setPixelColor(i + half, c2)
		strip.show()
		time.sleep(wait_ms/1000.0)
	
def fadeToggle(strip, color1, color2, color5, color6, wait_ms=50, min=0, max=100):
	"""Fade Toggle"""
	half = (strip.numPixels() - 2) / 2
	white1 = (color1 & (255 << 24)) >> 24
	red1 = (color1 & (255 << 8)) >> 8
	green1 = (color1 & (255 << 16)) >> 16
	blue1 = (color1 & 255)
	white2 = (color2 & (255 << 24)) >> 24
	red2 = (color2 & (255 << 8)) >> 8
	green2 = (color2 & (255 << 16)) >> 16
	blue2 = (color2 & 255)
	#print ('Input: ' + str(red) + ', ' + str(green) + ', ' + str(blue))
        strip.setPixelColor(strip.numPixels() - 1, color5)
        strip.setPixelColor(strip.numPixels() - 2, color6)
	for pr in range((max - min + 1) * 2):
		percent = pr + min if ((pr + min) <= max) else max - (pr + min - max)
		factor1 = float(percent) / 100.0
		factor2 = float(max - percent + min) / 100.0
		r1 = int(float(red1) * factor1)
		g1 = int(float(green1) * factor1)
		b1 = int(float(blue1) * factor1)
		c1 = Color(r1, g1, b1)
		r2 = int(float(red2) * factor2)
		g2 = int(float(green2) * factor2)
		b2 = int(float(blue2) * factor2)
		c2 = Color(r2, g2, b2)
		for i in range(half):
			strip.setPixelColor(i, c1)
			strip.setPixelColor(i + half, c2)
		strip.show()
		time.sleep(wait_ms/1000.0)

def blink(strip, color1, color2, color5, color6, wait_ms=50):
	"""Blink"""
	half = (strip.numPixels() - 2) / 2
        strip.setPixelColor(strip.numPixels() - 1, color5)
        strip.setPixelColor(strip.numPixels() - 2, color6)
	for i in range(half):
		strip.setPixelColor(i, color1)
		strip.setPixelColor(i + half, color2)
	strip.show()
	time.sleep(wait_ms/1000.0)
	for i in range(half):
		strip.setPixelColor(i, Color(0, 0, 0))
		strip.setPixelColor(i + half, Color(0, 0, 0))
	strip.show()
	time.sleep(wait_ms/1000.0)

data = json.loads(json.dumps([{'pattern': 'fade', 'color1': {'red': 16, 'green': 16, 'blue': 16}, 'color2': {'red': 16, 'green': 16, 'blue': 16}, 'color3': {'red': 16, 'green': 16, 'blue': 16}, 'color4': {'red': 16, 'green': 16, 'blue': 16}, 'color5': {'red': 16, 'green': 16, 'blue': 16}, 'color6': {'red': 16, 'green': 16, 'blue': 16}, 'wait': 10, 'width': 3, 'fading': 0, 'min': 50, 'max': 80}]), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

first = True
start = 0
iteration = 0
# Main program logic follows:
if __name__ == '__main__':
        # Process arguments
        opt_parse()

	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	# Intialize the library (must be called once before other functions).
	strip.begin()

	#print ('Press Ctrl-C to quit.')
	lastChange = os.path.getmtime(CONF_PATH + 'light.conf')
        #lastRestartChange = os.path.getmtime(REBOOT_PATH) if os.path.exists(REBOOT_PATH) else 0
        while True: #(os.path.getmtime(REBOOT_PATH) if os.path.exists(REBOOT_PATH) else 0) == lastRestartChange:
                #call(["/usr/local/bin/refresh"])
                #print ('Reboot: ' + str(os.path.getmtime(REBOOT_PATH) if os.path.exists(REBOOT_PATH) else 0) + ' <> ' + str(lastRestartChange))
		change = os.path.getmtime(CONF_PATH + 'light.conf')
                #os.spawnl(os.P_DETACH, '/usr/local/bin/refresh')
                #subprocess.Popen(['/usr/local/bin/refresh'], shell=True)
		if (change != lastChange or first):
                        try:
                                data = json.load(open(CONF_PATH + 'light.conf'), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
                                print ('Changed:')
                                for conf in data:
			                print ('    ' + conf.pattern + ' c1=' + str(conf.color1) + ', c2=' + str(conf.color2) + ', c3=' + str(conf.color3) + ', c4=' + str(conf.color4) + ', c5=' + str(conf.color5) + ', c6=' + str(conf.color6) + ', wait=' + str(conf.wait) + 'ms, width=' + str(conf.width) + ', fading=' + str(conf.fading) + ', min=' + str(conf.min) + ', max=' + str(conf.max))
			        #			i = i + 1
			        first = False
			        lastChange = change
                        except ValueError:
                                print ('Oops!  That was no valid JSON.  Try again...')


		index = start + (iteration % (len(data) - start))
                conf = data[index]
		if conf.pattern == 'clear':
                        start = index + 1
			print ('Cleared index=' + str(index) + ', length=' + str(len(data)) + ', start=' + str(start))
			index = start + (iteration % (len(data) - start))

                #print ('Index: ' + str(start) + ' + (' + str(iteration) + ' % (' + str(len(data)) + ' - ' + str(start) + ') = ' + str(index))
		if conf.pattern == 'wipe':
			wipe(strip, Color2(conf.color1), Color2(conf.color2), Color2(conf.color5), Color2(conf.color6), conf.wait, conf.fading)
		elif conf.pattern == 'light':
			light(strip, Color2(conf.color1), Color2(conf.color2), Color2(conf.color5), Color2(conf.color6), conf.wait)
		elif conf.pattern == 'rotation':
			rotation(strip, Color2(conf.color1), Color2(conf.color2), Color2(conf.color5), Color2(conf.color6), conf.width, conf.fading, conf.wait)
		elif conf.pattern == 'spin':
			spin(strip, Color2(conf.color1), Color2(conf.color2), Color2(conf.color5), Color2(conf.color6))
		elif conf.pattern == 'chaise':
			chaise(strip, Color2(conf.color1), Color2(conf.color2), Color2(conf.color5), Color2(conf.color6), conf.width, conf.fading, conf.wait)
		elif conf.pattern == 'lighthouse':
			lighthouse(strip, Color2(conf.color1), Color2(conf.color2), Color2(conf.color3), Color2(conf.color4), Color2(conf.color5), Color2(conf.color6), conf.width, conf.fading, conf.wait)
		elif conf.pattern == 'fade':
			fade(strip, Color2(conf.color1), Color2(conf.color2), Color2(conf.color5), Color2(conf.color6), conf.wait, conf.min, conf.max)
		elif conf.pattern == 'fadeToggle':
			fadeToggle(strip, Color2(conf.color1), Color2(conf.color2), Color2(conf.color5), Color2(conf.color6), conf.wait, conf.min, conf.max)
		elif conf.pattern == 'blink':
			blink(strip, Color2(conf.color1), Color2(conf.color2), Color2(conf.color5), Color2(conf.color6), conf.wait)
                elif conf.pattern == 'theater':
                        theater(strip, Color2(conf.color1), Color2(conf.color2), Color2(conf.color5), Color2(conf.color6), conf.wait, conf.fading)
                elif conf.pattern == 'rainbow':
                        rainbow(strip, conf.wait, conf.fading)
                elif conf.pattern == 'rainbowCycle':
                        rainbowCycle(strip, conf.wait, conf.fading)
                elif conf.pattern == 'wait':
                        time.sleep(conf.wait/1000.0)
		else:
			fade(strip, Color(16, 16, 16), Color(16, 16, 16), Color(0, 0, 0), Color(0, 0, 0), 10, 50, 80)
			
		iteration = iteration + 1

        light(strip, Color(0, 0, 0), Color(0, 0, 0))
