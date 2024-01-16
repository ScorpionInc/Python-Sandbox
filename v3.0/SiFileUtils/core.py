#!/usr/bin/env python3

"""
File     : core.py
Author(s): ScorpionInc
Purpose  : Sandbox main.
Version  : 1.0.0
Created  : 20231206
Updated  : 20231206
TODO     :
#1.) Make a TODO list...
"""

# Python Version Validation
import sys

# versioninfo['major','minor','micro']
if sys.version_info[0] != 3:
	print("[WARN]: Script '", str(__file__), "' was designed to run in Python Major Version 3.",
	      " Detected Major Version: '", str(sys.version_info[0]), "'.", sep="")

from SiFileUtils import *

if __name__ != "__main__":
	print("[WARN]: Script '", str(__file__), "' was designed to be used as an entry point but was not run as __main__.",
	      " (are you running from the wrong script?)", sep="")  # !Debugging

try:
	handle = open("challenges.html", "rb+")
	SiFileUtils.seek_until_count(file_handle=handle, character=ord("\n"), count=5, block_size=100)
	#print("Peeked line: '", SiFileUtils.peek_until(file_handle=handle, character=ord("\n"), block_size=1)[0], "'.", sep="")
	handle.close()
except IOError:
	ex_type, ex_value, traceback = sys.exc_info()
	print("[ERROR]: Encountered IOError: '" + str(ex_value) + "'.")  # !Debugging
