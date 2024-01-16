#!/usr/bin/env python3

"""
File     : SiFileUtils.py
Author(s): ScorpionInc
Purpose  : Static class contains helper functions/methods to expand functionality of basic python file handles.
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

from typing import Final, IO, Tuple  # Python version 3.8+

import re

# https://github.com/The-Compiler/hypothesis/commit/66ca462ddc6426d35047508d95e660a77999197b
try:
	import re._constants as sre_constants
	import re._parser as sre_parse
except ImportError:  # Python < 3.11
	import sre_constants
	import sre_parse


class SiFileUtils:
	# Constant(s)
	DEFAULT_BUFFER_SIZE: Final[int] = 4096  # 4kb
	
	# Function(s)
	@classmethod
	def r_seek_until_count(cls, file_handle: IO, character: int, count: int,
	                       block_size: int = DEFAULT_BUFFER_SIZE) -> None:
		# TODO Validation
		counter = count
		if counter <= 0:
			return
		buffer = cls.r_read_some(file_handle=file_handle, amount=block_size)
		while buffer:
			i = buffer.split(chr(character))
			counter -= (len(i) - 1)
			if (len(buffer) != block_size) or (counter <= 0):
				break
			buffer = cls.r_read_some(file_handle=file_handle, amount=block_size)
	
	@classmethod
	def r_seek_until(cls, file_handle: IO, character: int, block_size: int = DEFAULT_BUFFER_SIZE) -> None:
		# Helper Function
		cls.r_seek_until_count(file_handle=file_handle, character=character, count=1, block_size=block_size)
	
	@staticmethod
	def r_read_some(file_handle: IO, amount: int = DEFAULT_BUFFER_SIZE) -> str:
		# Attempts to read amount of data from behind current position while moving pointer.
		# Returns value read (in normal order).
		file_handle.seek(-amount, 1)
		buffer = file_handle.read(amount)
		file_handle.seek(-amount, 1)
		return buffer  # , (len(buffer) == amount) # Value, Success
	
	@staticmethod
	def r_read_until(file_handle: IO, character: int, block_size: int = DEFAULT_BUFFER_SIZE) -> str:
		# TODO
		pass
	
	@staticmethod
	def r_peek_some(file_handle: IO, amount: int = DEFAULT_BUFFER_SIZE):
		# Attempts to read amount of data from behind current position without changing position.
		# Returns value read (in normal order).
		pos = file_handle.tell()
		file_handle.seek(-amount, 1)
		buffer = file_handle.read(amount)
		# We should already be back to where we started out but in the event of an error
		# causing an incomplete read, this will ensure our position is where we started at.
		file_handle.seek(pos, 0)
		return buffer  # , (len(buffer) == amount) # Value, Success
	
	@staticmethod
	def seek_until_count(file_handle: IO, character: int, count: int, block_size: int = DEFAULT_BUFFER_SIZE) -> None:
		# TODO Validation
		counter = count
		if counter <= 0:
			return
		buffer = file_handle.read(block_size)
		# TODO Doesnt decode properly?
		print("Buffer0: ", buffer, "", type(buffer))
		if type(buffer) is bytes:
			# Handle Binary Mode
			print("file_handle is reading bytes.")
			buffer = buffer.decode()
		print("Buffer1: ", buffer, "", type(buffer))
		while buffer:
			i = buffer.split(b"".join(chr(character)))
			counter -= (len(i) - 1)
			if counter <= 0:
				print("Neato! Counter: ", counter)
				position_offset = 0
				for l in range(0, len(i)):
					position_offset += len(i[l])
				print(file_handle.tell(), position_offset)
				# TODO Can't reverse seek with text mode file?
				file_handle.seek(-position_offset, 1)
			if (len(buffer) != block_size) or (counter <= 0):
				break
			buffer = file_handle.read(block_size)
	
	@classmethod
	def seek_until(cls, file_handle: IO, character: int, block_size: int = DEFAULT_BUFFER_SIZE) -> None:
		# Helper Function
		cls.seek_until_count(file_handle=file_handle, character=character, count=1, block_size=block_size)
	
	@staticmethod
	def peek_some(file_handle: IO, amount: int = DEFAULT_BUFFER_SIZE) -> str:
		# Returns peeked arbitrary amount of data then restores IO position via seek().
		pos = file_handle.tell()
		buffer = file_handle.read(amount)
		file_handle.seek(pos, 0)
		return buffer
	
	@staticmethod
	def peek_line(file_handle: IO) -> str:
		# Returns peeked line using included IO.readline() and IO.seek() functions.
		pos = file_handle.tell()
		line = file_handle.readline()
		file_handle.seek(pos, 0)
		return line
	
	@staticmethod
	def peek_until(file_handle: IO, character: int, block_size: int = DEFAULT_BUFFER_SIZE) -> tuple[str, bool]:
		# Peeks data from current position until EOF or character is found.
		# Returns read values and whether character was found.
		i = -1
		pos = file_handle.tell()
		buffer = ""
		while i == -1:
			next_block = file_handle.read(block_size)
			if not next_block:
				file_handle.seek(pos, 0)
				return buffer, False
			buffer += next_block
			i = buffer.find(chr(character))
		file_handle.seek(pos, 0)
		return buffer[:i:], True
	
	# Modified from source:
	# https://stackoverflow.com/questions/4063392/maximum-match-length-of-a-regular-expression
	@staticmethod
	def get_regex_max_match_len(regex):
		min_len, max_len = sre_parse.parse(regex).getwidth()
		if max_len >= sre_parse.MAXREPEAT:
			raise ValueError('Unbounded Regex.')
		return max_len
	
	@classmethod
	def find_first_regex_match_simple(cls, file_handle: IO, regex: str) -> int:
		# Unlike find_first_regex_match() this always checks regex matches line-by-line.
		# This will be fine in most use cases but may break if regex matches patterns across more than one line at a time.
		# Returns -1 otherwise.
		pos = file_handle.tell()
		rmp = -1
		file_handle.seek(0, 0)
		while True:
			next_line = file_handle.readline()
			if not next_line:
				break
			# re options: .match() .search() .findall() .fullmatch()
			fm = re.search(regex, next_line)
			if fm is not None:
				rmp = file_handle.tell() - len(next_line) + fm.span()[0]
				break
		file_handle.seek(pos, 0)
		return rmp
	
	@classmethod
	def find_first_regex_match(cls, file_handle: IO, regex: str) -> int:
		# TODO Validation
		# Returns the absolute position within a file of first match of regex.
		# Returns -1 or Exception otherwise.
		pos = file_handle.tell()
		file_handle.seek(0, 0)
		# First we test if the provided regex is bounded.
		# Bounded regex allows us to read in smaller chunks at a time test against.
		# For unbounded regex we will match against the entire file at once. (Memory intensive)
		try:
			min_len, max_len = sre_parse.parse(regex).getwidth()
		except ValueError:
			max_len = min_len = -1
		rmp = -1
		if (max_len < sre_parse.MAXREPEAT) and (max_len > 0):
			# Bounded Regex
			# Buffer of size max_len read min_length each loop.
			if min_len <= 0:
				return 0
			delta_range = (max_len - min_len)
			buffer = file_handle.read(max_len)
			while buffer:
				m = re.search(regex, buffer, re.MULTILINE)
				if m is not None:
					rmp = file_handle.tell() - max_len + m.span()[0]
					break
				next_read = file_handle.read(min_len)
				if not next_read:
					break
				buffer = buffer[min_len::] + next_read
		else:
			# Unbounded Regex
			buffer = file_handle.read()
			m = re.search(regex, buffer, re.MULTILINE)
			if m is not None:
				rmp = m.span()[0]
		file_handle.seek(pos, 0)
		return rmp
	
	# Method(s)
	# Constructor(s) / Destructor(s)
	def __init__(self):
		print("[WARN]: Static class SiFileUtils accessed in a non-static way.")  # !Debugging


if __name__ == "__main__":
	print("[WARN]: Script '", str(__file__), "' was designed to be used as a module but was run as __main__.",
	      " (are you missing an import somewhere?)", sep="")  # !Debugging
