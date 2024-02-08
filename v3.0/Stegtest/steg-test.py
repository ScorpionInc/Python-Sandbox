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

def handle_image_file(parser, arg):
	if not os.path.exists(arg):
		parser.error("The image file %s does not exist!" % arg)
	else:
		return PIL.Image.open(arg, mode='r', formats=None)

def handle_secret_file(parser, arg):
	if not os.path.exists(arg):
		parser.error("The secret file %s does not exist!" % arg)
	else:
		return open(arg, 'r')

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
	print("[ERROR]: Image path is required.")
	exit(-1)
elif(args.imagepath is None):
	print("[ERROR]: Image path is required.")
	exit(-2)
if(not hasattr(args, "secret")):
	print("[ERROR]: Secret file is required when embedding.")
	exit(-3)
elif(args.secret is None):
	print("[ERROR]: Secret file is required when embedding.")
	exit(-4)
sourceImage = args.imagepath[0]
print("Image Path: " + sourceImage.filename + "\t Dimensions: " + str(sourceImage.size))
print("Secret File Path: '" + args.secret[0] + "'.") # Debugging
if(args.dataratio[0] <= 0.0 or args.dataratio[0] >= 1.0):
	print("[DEBUG]: Invalid Data Retio detected. Auto selecting...")
	pixel_count = sourceImage.size[0] * sourceImage.size[1]
	print("[DEBUG]: Pixel Count: " + str(pixel_count) + "\t Current Image Mode: " + str(sourceImage.mode) + "\t Current Image Bands: " + str(sourceImage.getbands()) + "\t Current Image Info: " + str(sourceImage.info))
	
