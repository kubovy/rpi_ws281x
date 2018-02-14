# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time

from neopixel import *

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

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
	"""Movie theater light style chaser animation."""
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

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

def wipe(strip, color1, color2, wait_ms=50, sleep=0):
	"""Wipe color across display a pixel at a time."""
	half = (strip.numPixels() - 2) / 2
	for i in range(half):
		strip.setPixelColor(i, color1)
		strip.setPixelColor(i + half, color2)
		strip.show()
		time.sleep(wait_ms/1000.0)
	if sleep > 0:
		time.sleep(sleep/1000.0)
		wipe(strip, Color(0, 0, 0), Color(0, 0, 0), wait_ms, 0)

def light(strip, color1, color2):
	half = (strip.numPixels() - 2) / 2
	for i in range(half):
		strip.setPixelColor(i, color1)
		strip.setPixelColor(i + half, color2)
	strip.show()

def rotation(strip, color1, color2, width=3, fade=0, wait_ms=50):
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
			strip.setPixelColor(p, c1)
			strip.setPixelColor(p + half, c2)
		strip.show()
		time.sleep(wait_ms/1000.0)

def spin(strip, color1, color2):
	"""Spin"""
	for w in range(5):
		rotation(strip, color1, color2, 24, 4, 50 - (w * 10))
	rotation(strip, color1, color2, 24, 4, 50 - (w * 10))
	for w in range(3):
		lighthouse(strip, color1, color2, 12, 4, 30 - (w * 10))
		lighthouse(strip, color1, color2, 12, 4, 30 - (w * 10))
	light(strip, color1, color2)
	time.sleep(10)

def chaise(strip, color1, color2, width=3, fade=0, wait_ms=50):
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
		strip.show()
		time.sleep(wait_ms/1000.0)

			
def lighthouse(strip, color1, color2, width=3, fade=0, wait_ms=50):
	"""Lighthouse"""
	half = (strip.numPixels() - 2) / 2
	quarter = half / 2
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
			q = p + quarter if (p + quarter < half) else (p + quarter) - half
			strip.setPixelColor(p, c1)
			strip.setPixelColor(p + half, c1)
			strip.setPixelColor(q, c2)
			strip.setPixelColor(q + half, c2)
		strip.show()
		time.sleep(wait_ms/1000.0)
			
def fade(strip, color1, color2, wait_ms=50, min=0, max=100):
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
	
def fadeToggle(strip, color1, color2, wait_ms=50, min=0, max=100):
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

def blink(strip, color1, color2, wait_ms=50):
	"""Blink"""
	half = (strip.numPixels() - 2) / 2
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

pattern = ['fade']
color1 = [Color(16, 16, 16)]
color2 = [Color(16, 16, 16)]
wait_ms = [10]
width = [3]
fading = [0]
min = [50]
max = [80]
count = 1

first = True
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
	while True:
		change = os.path.getmtime(CONF_PATH + 'light.conf')
		if (change != lastChange or first):
			file = open(CONF_PATH + 'startup.conf', 'r') if first else open(CONF_PATH + 'light.conf', 'r')
			pattern = []
			color1 = []
			color2 = []
			wait_ms = []
			width = []
			fading = []
			min = []
			max = []
			i = 0
			for line in file:
				#print ('Line: ' + line)
				if not line.startswith('#'):
					values = line.replace("\t\t", "\t").replace("\t", " ").split(" ")
					#print (str(len(values)))
					if len(values) == 8:
						pattern.append(values[0])
						rgb = values[1].split(",")
						color1.append(Color(int(rgb[0]), int(rgb[1]), int(rgb[2])))
						rgb = values[2].split(",")
						color2.append(Color(int(rgb[0]), int(rgb[1]), int(rgb[2])))
						wait_ms.append(int(values[3]))
						width.append(int(values[4]))
						fading.append(int(values[5]))
						min.append(int(values[6]))
						max.append(int(values[7]))
						print ('Changed[' + str(i) + ']: ' + pattern[i] + ' color1=' + str(color1[i]) + ', color2=' + str(color2[i]) + ', wait=' + str(wait_ms[i]) + 'ms, width=' + str(wait_ms[i]) + ', fading=' + str(fading[i]) + ', min=' + str(min[i]) + ', max=' + str(max[i]))
						i = i + 1
			first = False
			count = i
			file.close()
			lastChange = change


		index = iteration % count
		if pattern[index] == 'clear':
			for i in range(index + 1):
				pattern.pop(0)
				color1.pop(0)
				color2.pop(0)
				wait_ms.pop(0)
				width.pop(0)
				fading.pop(0)
				min.pop(0)
				max.pop(0)
			count = count - index - 1
			#print ('Cleared ' + str(index) + ', ' + str(count) + ', ' + str(len(pattern)) + ' -> ' + pattern[0])
			index = iteration % count

		if pattern[index] == 'wipe':
			wipe(strip, color1[index], color2[index], wait_ms[index], fading[index])
		elif pattern[index] == 'light':
			light(strip, color1[index], color2[index])
		elif pattern[index] == 'rotation':
			rotation(strip, color1[index], color2[index], width[index], fading[index], wait_ms[index])
		elif pattern[index] == 'spin':
			spin(strip, color1[index], color2[index])
		elif pattern[index] == 'chaise':
			chaise(strip, color1[index], color2[index], width[index], fading[index], wait_ms[index])
		elif pattern[index] == 'lighthouse':
			lighthouse(strip, color1[index], color2[index], width[index], fading[index], wait_ms[index])
		elif pattern[index] == 'fade':
			fade(strip, color1[index], color2[index], wait_ms[index], min[index], max[index])
		elif pattern[index] == 'fadeToggle':
			fadeToggle(strip, color1[index], color2[index], wait_ms[index], min[index], max[index])
		elif pattern[index] == 'blink':
			blink(strip, color1[index], color2[index], wait_ms[index])
		else:
			fade(strip, Color(16, 16, 16), Color(16, 16, 16), 10, 50, 80)
			
		iteration = iteration + 1

