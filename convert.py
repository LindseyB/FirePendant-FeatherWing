# Generates code for drawing images via command line presently hardcoded 
# to newframe*.png
# Invocation: python convert.py > code.ino
# Created from the convert.py file on the original FlamePendant project
# Requires Python3 and Python Imaging Library.

from PIL import Image
import sys
import fnmatch
import os

# --------------------------------------------------------------------------

cols     = 12 # Current column number in output (force indent on first one)
byteNum  = 0
numBytes = 0

def writeByte(n):
	global cols, byteNum, numBytes

	cols += 1                      # Increment column #
	if cols >= 12:                 # If max column exceeded...
		print                  # end current line
		sys.stdout.write("  ") # and start new one
		cols = 0               # Reset counter
	sys.stdout.write("{0:#0{1}X}".format(n, 4))
	byteNum += 1
	if byteNum < numBytes:
		sys.stdout.write(",")
		if cols < 11:
			sys.stdout.write(" ")

# --------------------------------------------------------------------------

prior    = None
bytes    = 0
numBytes = 0xFFFF

for file in os.listdir('.'):
	if fnmatch.fnmatch(file, 'newframe*.png'):
		image = Image.open(file)
		image.pixels = image.load()
		if image.mode != 'L': # Not grayscale? Convert it
			image = image.convert("L")
			image.pixels = image.load()
		# Gamma correction:
		for y in range(image.size[1]):
			for x in range(image.size[0]):
				image.pixels[x, y] = int(pow((image.pixels[x, y] / 255.0), 2.7) * 255.0 + 0.5)

		if prior:
			for y in range(image.size[1]):
				for x in range(image.size[0]):
					if image.pixels[x, y] != prior.pixels[x, y]:
						print("matrix.drawPixel("+str(x)+", "+str(y)+", " + str(image.pixels[x,y]) + ");")
		else:
			# first frame
			for y in range(image.size[1]):
				for x in range(image.size[0]):
					if image.pixels[x, y] != 0:
						print("matrix.drawPixel("+str(x)+", "+str(y)+", " + str(image.pixels[x,y]) + ");")
			
		prior = image
		