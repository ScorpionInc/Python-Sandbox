#/usr/bin/env python
"""Module providing a write once, read-only const class."""

import sys

if sys.version_info.major != 3:
	print("[ERROR]: Script was designed for Python Major version >= 3.", file=sys.stderr)
	sys.exit(1)

if __name__ == "__main__":
	print("[ERROR]: si_const.py is not executable.", file=sys.stderr)
	sys.exit(1)

class const(object):
	"""Class representing constant values."""
	# Ensures singleton
	_instance = None
	# No dictionary usage
	__slots__ = ()
	# Values can be assigned only once.
	_consts = {}
	def __new__(cls, *_):
		if not isinstance(cls._instance, cls):
			cls._instance = super(const, cls).__new__(cls)
		return cls._instance
	def __setattr__(self, name, value):
		if name in self._consts:
			raise TypeError
		self._consts[name] = value
	def __getattr__(self, name):
		return self._consts[name]
