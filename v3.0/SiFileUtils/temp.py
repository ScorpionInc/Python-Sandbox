# Python Version Validation
import sys

# versioninfo['major','minor','micro']
if sys.version_info[0] != 3:
	print("[WARN]: Script '", str(__file__), "' was designed to run in Python Major Version 3.",
		  " Detected Major Version: '", str(sys.version_info[0]), "'.", sep="")

import io
from typing import Final, IO, Tuple  # Python version 3.8+

#https://stackoverflow.com/a/36974338
def get_char():
	# figure out which function to use once, and store it in _func
	if "_func" not in get_char.__dict__:
		try:
			# for Windows-based systems
			import msvcrt # If successful, we are on Windows
			get_char._func=msvcrt.getch
		except ImportError:
			# for POSIX-based systems (with termios & tty support)
			import tty, sys, termios # raises ImportError if unsupported
			def _ttyRead():
				fd = sys.stdin.fileno()
				oldSettings = termios.tcgetattr(fd)
				try:
					tty.setcbreak(fd)
					answer = sys.stdin.read(1)
				finally:
					termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)
				return answer
			get_char._func=_ttyRead
	return get_char._func()
def pause(prompt: str = "Press any key to continue..."):
	print(prompt)
	return get_char()

# Returns true when file_handle was opened in binary mode.
# Returns false otherwise.
def is_binary(file_handle: IO):
    return isinstance(file_handle, (io.RawIOBase, io.BufferedIOBase))

# Seeks file stream file_handle by amount from mode.
# Handles relative mode for text mode and wraps on EOF/SOF.
# Returns new position.
def stream_seek(file_handle: IO, amount, mode: int = 1):
	# Validate Parameters
	# 0 - Start, 1 - Relative, 2 - EOF
	if(mode < 0 or mode > 2):
		print("[ERROR]: stream_seek() called with invalid parameter value: ", mode, ".")#!Debugging
		return
	current_position = file_handle.tell()
	target_position = (current_position + amount)
	# Handle reverse seek from file start.
	if(mode == 0 and amount < 0):
		mode = 2
	if(mode == 1 and target_position < 0):
		mode = 2
		amount = target_position
	# Can't relative(+/-) seek with file opened in text mode.
	if(is_binary(file_handle) or mode != 1):
		#print("[DEBUG]: Safe to relative seek(if needed/requested).")#!Debugging
		file_handle.seek(amount, mode)
	else:
		#print("[DEBUG]: Relative-mode seek requested on text-mode file handle.")#!Debugging
		#print("[DEBUG]: Current: ", current_position, "\tAmount: ", amount, "\tTarget: ", target_position)
		stream_seek(file_handle, target_position, 0)
	return file_handle.tell()

DEFAULT_BUFFER_SIZE: Final[int] = 4096 # 4kb
def seek_until_count(file_handle: IO, pattern: bytes, count: int, block_size: int = DEFAULT_BUFFER_SIZE) -> None:
	counter = count
	buffer = file_handle.read(block_size)

try:
	handle = open("challenges.html", "rb+")
	handle.close()
except IOError:
	ex_type, ex_value, traceback = sys.exc_info()
	print("[ERROR]: Encountered IOError: '" + str(ex_value) + "'.")  # !Debugging

print("temp.py has ended.") # !Debugging
pause()
