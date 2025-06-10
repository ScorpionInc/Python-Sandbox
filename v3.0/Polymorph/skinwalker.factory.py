#!/usr/bin/env python3

"""
File     : skinwalker.factory.py
Author(s): ScorpionInc
Purpose  : Generates simple self modifing python.
Version  : 1.0.0
Created  : 20250609
Updated  : 20250609
TODO     :
#1.) Make a TODO list...
"""

import sys

# versioninfo['major','minor','micro']
if sys.version_info[0] != 3:
	print("[WARN]: Script '", str(__file__), "' was designed to run in Python Major Version 3.", " Detected Major Version: '", str(sys.version_info[0]), "'.", sep="")

import random

if __name__ == "__main__":
	# Initialize variables
	xor_key = ord(chr(random.randint(1,127)))
	chunk_size = 1024
	input_file_path = ""
	output_file_path = "skinwalker.generated.py"
	argc = len(sys.argv)
	# Handle arguments
	if(argc <= 0):
		# How?
		sys.exit(1)
	if(argc == 1):
		print(f"Usage:\n{sys.argv[0]} source.py [output.py]")
		sys.exit(1)
	input_file_path = sys.argv[1]
	if(argc >= 3):
		output_file_path = sys.argv[2]
	# Start Generating
	with open(output_file_path, "w") as file:
		file.write("#!/usr/bin/env python3\n")
		file.write("i=(\'\'\'")
		with open(input_file_path, "r") as source:
			while True:
				chunk = source.read(chunk_size)
				if not chunk:
					break
				file.write(''.join(map(lambda c: chr(ord(c) ^ xor_key), chunk)).encode().hex())
		file.write("\'\'\')\n")
		file.write("import importlib as il\n")
		file.write("def o(p,n):\n\treturn il.util.spec_from_file_location(n,p)\n")
		file.write("def d(n):\n\treturn il.import_module(n)\n")
		file.write("def q(p,n='_'):\n\tm=il.util.module_from_spec(t:=o(p,n));t.loader.exec_module(m)\n")
		file.write("if __name__==\"__main__\":\n")
		file.write("\ta=(s:=d(''.join([chr(ord(__name__[3])+6*3),chr(ord(__name__[3])+6*4),chr(ord(__name__[3])+6*3)]))).argv[len(__name__)%2]\n")
		file.write("\twith open(a,chr(ord(__name__[5])+len(__name__)+1))as w:\n")
		file.write("\t\tw.write(''.join([chr(int(i[n:n+(len(__name__)%3)],16)^0x")
		file.write('{:02x}'.format(xor_key))
		file.write(")for n in range(len(__name__)%4,len(i),len(__name__)%3)]))\n")
		file.write("\tq(a);open(a,chr(ord(__name__[5])+len(__name__)+1)).close()\n");
