#!/usr/bin/env python3

"""
File     : steg-test.py
Author(s): ScorpionInc
Purpose  : Sandbox testing out simple stegenography in python.
Version  : 1.0.0
Created  : 20240202
Updated  : 20240202
TODO     :
#1.) Make a TODO list...
"""

# Python Version Validation
import sys

# versioninfo['major','minor','micro']
if sys.version_info[0] != 3:
	print("[WARN]: Script '", str(__file__), "' was designed to run in Python Major Version 3.",
	      " Detected Major Version: '", str(sys.version_info[0]), "'.", sep="")

import os
import argparse
import PIL.Image

def PIL_Image_has_Alpha(img):
	if(not hasattr(img, mode)):
		return False;
	return(img.mode.contains('A'))

def PIL_Band_to_BitCount(band):
	if(";" in band):
		tmp = band[(band.find(";") + 1):]
		return int(''.join(c for c in tmp if c not in "ABGLNPRabglnpr"));
	elif(band in "LPRGBACMYKHSV"):
		return 8
	elif(band == "Cb" or band == "Cr"):
		return 8
	elif(band == "I" or band == "F"):
		return 32
	return 0

def PIL_Bands_to_TotalBitCount(bands):
	if not hasattr(bands, "__iter__") or isinstance(bands, str):
		return 0
	band_count = len(bands)
	bit_accumulator = 0
	for band in bands:
		bit_accumulator += PIL_Band_to_BitCount(band)
	return bit_accumulator

def handle_image_file(parser, arg):
	if not os.path.exists(arg):
		parser.error("[ERROR]: The specified image file %s does not exist!" % arg)
	else:
		return PIL.Image.open(arg, mode='r', formats=None)

def handle_secret_file(parser, arg):
	if not os.path.exists(arg):
		parser.error("[ERROR]: The specified secret file %s does not exist!" % arg)
	else:
		return open(arg, 'rb')

def handle_target_file(parser, arg):
	if os.path.exists(arg):
		print("[WARN]: Target file already exists and will be overwritten.")
	return arg

parser = argparse.ArgumentParser(description='Python script for image stegenography.', epilog='~Created by: ScorpionInc')
parser.add_argument('-i', '--imagepath', dest='imagepath', nargs=1, metavar='FILE', help='Path to image file.', type=lambda x: handle_image_file(parser, x)) # required=True,
parser.add_argument('-s', '--secret', dest='secret', nargs=1, help='Filepath to file of data to be stored/hidden.', type=lambda x: handle_secret_file(parser, x))
parser.add_argument('-o', '--output', dest='output', nargs=1, default="", help='Filepath to save result image/extracted data to/as. (Default: <SOURCE FILE>_steg<.img/.bin>)', type=lambda x: handle_target_file(parser, x))
parser.add_argument('-d', '--dataratio', dest='dataratio', nargs=1, default=0.13, help='How much data is stored per pixel as a percentage. (Default: 13%%)', type=float)
parser.add_argument('-a', '--alphaweight', dest='alphaweight', nargs=1, default=1, help='Priority of the data being stored in the alpha channel. (Default: 1)', type=int)
parser.add_argument('-r', '--redweight', dest='redweight', nargs=1, default=1, help='Priority of the data being stored in the red channel. (Default: 1)', type=int)
parser.add_argument('-g', '--greenweight', dest='greenweight', nargs=1, default=1, help='Priority of the data being stored in the green channel. (Default: 1)', type=int)
parser.add_argument('-b', '--blueweight', dest='blueweight', nargs=1, default=1, help='Priority of the data being stored in the blue channel. (Default: 1)', type=int)

args = parser.parse_args()
if(not hasattr(args, "imagepath")):
	print("[ERROR]: Image path is required.", file=sys.stderr)
	exit(-1)
elif(args.imagepath is None):
	print("[ERROR]: Image path is required.", file=sys.stderr)
	exit(-2)
if(not hasattr(args, "secret")):
	print("[ERROR]: A Secret file is required when embedding.", file=sys.stderr)
	exit(-3)
elif(args.secret is None):
	print("[ERROR]: A Secret file is required when embedding.", file=sys.stderr)
	exit(-4)
BITS_PER_BYTE = 8
sourceImage = args.imagepath[0]
pixel_count = sourceImage.size[0] * sourceImage.size[1]
pixel_bit_count = PIL_Bands_to_TotalBitCount(sourceImage.getbands())
total_bit_count = (pixel_count * pixel_bit_count)
secretFile = args.secret[0] if (type(args.secret) is list) else args.secret
secretPath = str(secretFile.name)
secretStats = os.stat(secretPath)
dataRatio = args.dataratio[0] if (type(args.dataratio) is list) else args.dataratio
print("[DEBUG]: Image Path: " + sourceImage.filename + "\t Dimensions: " + str(sourceImage.size)) # Debugging
print("[DEBUG]: Pixel Count: " + str(pixel_count) + " \t Pixel Bit Depth: " + str(pixel_bit_count) + ".") # Debugging
print("[DEBUG]: Secret File Path: '" + secretPath + "' \tByte Size: " + str(secretStats.st_size) + " \tBit Size: " + str(secretStats.st_size * 8) + ".") # Debugging
print("[DEBUG]: Initial Data Ratio: '" + str(dataRatio) + "'.") # Debugging
if(dataRatio <= 0.0 or dataRatio >= 1.0):
	print("[DEBUG]: Invalid Data Ratio detected. Auto selecting a new Data Ratio...")
	dataRatio = 0.13
print("[DEBUG]: Final Data Ratio: '" + str(dataRatio) + "'.") # Debugging

for y in range(0, sourceImage.size[1], 1):
	for x in range(0, sourceImage.size[0], 1):
		currentXY = (x, y)
		currentPixel = sourceImage.getpixel(currentXY)
		newRed = currentPixel[0]
		newGreen = currentPixel[1]
		newBlue = currentPixel[2]
		next_data = secretFile.read(3)
		data_len = len(next_data)
		if(data_len >= 1):
			newRed = (next_data[0])
		if(data_len >= 2):
			newGreen = (next_data[1])
		if(data_len >= 3):
			newBlue = (next_data[2])
		sourceImage.putpixel(currentXY, (newRed, newGreen, newBlue))
sourceImage.save(sourceImage.filename + "_stg.bmp")