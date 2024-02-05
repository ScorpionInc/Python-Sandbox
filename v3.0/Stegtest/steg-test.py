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

import argparse
import PIL

