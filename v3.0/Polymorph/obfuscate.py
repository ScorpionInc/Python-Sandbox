#!/usr/bin/env python3
import random
import re
import string

class ObfToken:
	"""
	Docstring: Represents a single unobfuscated character
	"""
	def __init__(self, clear: str, obfuscations: list):
		self.clear = clear
		self.obfuscations = obfuscations

	def select_obfuscation(self, max_len: int = -1):
		if(0 == len(self.obfuscations)):
			return self.clear
		if(max_len >= 0):
			capped = [o for o in self.obfuscations if len(o) <= max_len]
		else:
			capped = [o for o in self.obfuscations]
		# Allows for clear token as an option
		capped.append(self.clear)
		return random.choice(capped)

class Obfuscator:
	"""
	Docstring: Initializes mappings and generates obfuscated python code.
	"""
	DEFAULT_MAX_DEPTH:int = 2
	def __init__(self):
		self.max_token_depth = self.DEFAULT_MAX_DEPTH
		self.max_token_len = -1
		self.mapping = {}

		# Objects
		self.mapping["None"] = ObfToken("None", [
			"__doc__",
			"__spec__"
		])
		self.mapping["True"] = ObfToken("True", [
			"__debug__",
			"(\\2\\==\\2\\)",
			"(not \\False\\)"
		])
		self.mapping["False"] = ObfToken("False", [
			"(not \\1\\)",
			"(not \\5\\)",
			"(not \\8\\)",
			"(\\2\\!=\\2\\)",
			"(not \\True\\)"
		])
		# Numbers
		self.mapping["-2"] = ObfToken("-2", [
			"(~\\True\\)"
		])
		self.mapping["\"-2\""] = ObfToken("\"-2\"", [
			"str(\\-2\\)"
		])
		self.mapping["1"] = ObfToken("1", [
			"(\\5\\-\\4\\)",
			"(\\5\\//\\4\\)",
			"(\\5\\%\\4\\)"
		])
		self.mapping["\"1\""] = ObfToken("\"1\"", [
			"str(\\1\\)"
		])
		self.mapping["2"] = ObfToken("2", [
			"(\\True\\<<\\1\\)",
			"(\\4\\//\\2\\)",
			"(\\5\\//\\2\\)",
			"int(\\4\\/\\2\\)",
			"int(\\5\\/\\2\\)",
			"len(str(\\-2\\))"
		])
		self.mapping["\"2\""] = ObfToken("\"2\"", [
			"str(\\2\\)"
		])
		self.mapping["3"] = ObfToken("3", [
			"(\\5\\+\\-2\\)"
		])
		self.mapping["\"3\""] = ObfToken("\"3\"", [
			"str(\\3\\)"
		])
		self.mapping["4"] = ObfToken("4", [
			"len(\\\"True\"\\)"
		])
		self.mapping["\"4\""] = ObfToken("\"4\"", [
			"str(\\4\\)"
		])
		self.mapping["5"] = ObfToken("5", [
			"len(\\\"False\"\\)"
		])
		self.mapping["\"5\""] = ObfToken("\"5\"", [
			"str(\\5\\)"
		])
		self.mapping["7"] = ObfToken("7", [
			"(\\5\\+\\2\\)",
			"(\\8\\-\\1\\)"
		])
		self.mapping["\"7\""] = ObfToken("\"7\"", [
			"str(\\7\\)"
		])
		self.mapping["6"] = ObfToken("6", [
			"(\\4\\+\\2\\)",
			"(\\3\\*\\2\\)"
		])
		self.mapping["\"6\""] = ObfToken("\"6\"", [
			"str(\\6\\)"
		])
		self.mapping["8"] = ObfToken("8", [
			"(\\4\\*\\2\\)",
			"len(\\\"__main__\"\\)"
		])
		self.mapping["\"8\""] = ObfToken("\"8\"", [
			"str(\\8\\)"
		])
		self.mapping["9"] = ObfToken("9", [
			"(\\8\\+\\1\\)",
			"(\\3\\*\\3\\)",
			"(\\3\\**\\2\\)"
		])
		self.mapping["\"9\""] = ObfToken("\"9\"", [
			"str(\\9\\)"
		])
		# Strings
		self.mapping["\"True\""] = ObfToken("\"True\"", [
			"str(\\True\\)"
		])
		self.mapping["\"False\""] = ObfToken("\"False\"", [
			"str(\\False\\)"
		])
		self.mapping["\"None\""] = ObfToken("\"None\"", [
			"str(\\None\\)"
		])
		self.mapping["\"__main__\""] = ObfToken("\"__main__\"", [
			"__name__"
		])
		# Lowercase
		self.mapping["\"a\""] = ObfToken("\"a\"", [
			"(\\\"__main__\"\\[\\3\\])"
		])
		self.mapping["\"c\""] = ObfToken("\"c\"", [
			"chr(ord(\\\"a\"\\)+\\2\\)"
		])
		self.mapping["\"d\""] = ObfToken("\"d\"", [
			"chr(ord(\\\"a\"\\)+\\3\\)"
		])
		self.mapping["\"e\""] = ObfToken("\"e\"", [
			"(\\\"None\"\\[\\3\\])"
		])
		self.mapping["\"f\""] = ObfToken("\"f\"", [
			"chr(ord(\\\"e\"\\)+\\1\\)"
		])
		self.mapping["\"i\""] = ObfToken("\"i\"", [
			"(\\\"__main__\"\\[\\4\\])"
		])
		self.mapping["\"k\""] = ObfToken("\"k\"", [
			"chr(ord(\\\"i\"\\)+\\2\\)"
		])
		self.mapping["\"l\""] = ObfToken("\"l\"", [
			"(\\\"False\"\\[\\2\\])"
		])
		self.mapping["\"m\""] = ObfToken("\"m\"", [
			"(\\\"__main__\"\\[\\2\\])"
		])
		self.mapping["\"n\""] = ObfToken("\"n\"", [
			"(\\\"None\"\\[\\2\\])",
			"(\\\"__main__\"\\[\\5\\])"
		])
		self.mapping["\"o\""] = ObfToken("\"o\"", [
			"(\\\"None\"\\[\\1\\])"
		])
		self.mapping["\"r\""] = ObfToken("\"r\"", [
			"(\\\"True\"\\[\\1\\])",
			"chr(ord(\\\"o\"\\)+\\3\\)"
		])
		self.mapping["\"s\""] = ObfToken("\"s\"", [
			"chr(ord(\\\"o\"\\)+\\4\\)"
		])
		self.mapping["\"t\""] = ObfToken("\"t\"", [
			"chr(ord(\\\"o\"\\)+\\5\\)"
		])
		self.mapping["\"u\""] = ObfToken("\"u\"", [
			"(\\\"True\"\\[\\2\\])",
			"chr(ord(\\\"o\"\\)+\\6\\)"
		])
		# Uppercase
		self.mapping["\"F\""] = ObfToken("\"F\"", [
			"(\\\"False\"\\[\\0\\])"
		])
		self.mapping["\"I\""] = ObfToken("\"I\"", [
			"\\\"i\"\\.upper()"
		])
		self.mapping["\"N\""] = ObfToken("\"N\"", [
			"(\\\"None\"\\[\\0\\])"
		])
		self.mapping["\"T\""] = ObfToken("\"T\"", [
			"(\\\"True\"\\[\\0\\])"
		])
		# Symbols
		self.mapping["\"_\""] = ObfToken("\"_\"", [
			"(\\\"__main__\"\\[\\0\\])",
			"(\\\"__main__\"\\[\\1\\])",
			"(\\\"__main__\"\\[\\6\\])",
			"(\\\"__main__\"\\[\\7\\])"
		])
		# Number to/from character mappings
		self._add_ord_mappings()
		#self._add_chr_mappings()

	def _add_ord_mappings(self):
		for c in (string.ascii_lowercase + string.ascii_uppercase):
			key = str(ord(c))
			value = "ord(\\\"" + c + "\"\\)"
			if not key in self.mapping:
				self.mapping[key] = ObfToken(key, [])
			if not value in self.mapping[key].obfuscations:
				self.mapping[key].obfuscations.append(value)

	def _add_chr_mappings(self):
		for c in (string.ascii_lowercase + string.ascii_uppercase):
			key = "\"" + c + "\""
			value = "chr(\\" + str(ord(c)) + "\\)"
			if not key in self.mapping:
				self.mapping[key] = ObfToken(key, [])
			if not value in self.mapping[key].obfuscations:
				self.mapping[key].obfuscations.append(value)

	def expand_obfuscation(self, obfuscated:str, depth:int = 0, max_depth:int = -1):
		buffer: str = ""
		key: str = ""
		start_key: bool = False
		for i in range(len(obfuscated)):
			if(obfuscated[i] == "\\"):
				if(start_key == False):
					start_key = True
				else:
					start_key = False
					if("" == key):
						buffer += "\\"
						continue
					# Do key expansion
					if not key in self.mapping:
						buffer += key
						key = ""
						continue
					token = self.mapping[key]
					key = ""
					new_value = token.select_obfuscation(self.max_token_len)
					# Limit expansion depth
					if(max_depth >= 0 and depth >= max_depth):
						new_value = re.sub(r'(\\){1,1}([^\\])', r'\2', new_value, 0, 0)
						new_value = re.sub(r'([^\\])(\\){1,1}', r'\1', new_value, 0, 0)
					else:
						new_value = self.expand_obfuscation(new_value, depth + 1, max_depth)
					buffer += new_value
			elif(start_key == False):
				buffer += obfuscated[i]
			else:
				key += obfuscated[i]
		return buffer

	def explode_strings(self, source: str):
		buffer = ""
		start_str:bool = False
		for i in range(len(source)):
			if(source[i] == "\"" or source[i] == "\'"):
				start_str = not start_str
				if(not start_str):
					buffer = buffer[:-1]
			elif(start_str == False):
				buffer += source[i]
			else:
				buffer += ("\"" + source[i] + "\"+")
		return buffer

	def unexplode_strings(self, source: str):
		return re.sub(r'["\']\w?[+]\w?["\']', r'', source, 0, 0)

	def obfuscate(self, source: str):
		# TODO
		buffer = self.explode_strings(source)
		longest_key = max(self.mapping, key=len)
		longest_key_len = len(longest_key)
		for i in range(longest_key_len, 0, -1):
			filtered_map = {key: value for key, value in self.mapping.items() if len(key) == i}
			start_at:int = 0
			while True:
				found_match:bool = False
				buffer_len = len(buffer)
				for ii in range(start_at, buffer_len - i + 1):
					test_token = buffer[ii:(ii + i)]
					print("Testing:", test_token) # Debugging
					if(test_token in filtered_map):
						obfuscated = filtered_map[test_token]
						obfuscated = obfuscated.select_obfuscation(self.max_token_len)
						obfuscated = self.expand_obfuscation(obfuscated, 0, self.max_token_depth)
						start_at = (ii + len(obfuscated))
						found_match = True
						print(test_token, "->", obfuscated) # Debugging
						buffer = buffer[:ii] + obfuscated + buffer[ii+i:]
						print("Buffer:", buffer, "start_at:", start_at) # Debugging
						break
				if not found_match:
					break
		buffer = self.unexplode_strings(buffer)
		return buffer

	def pretty(self, source: str):
		# TODO
		pass

o = Obfuscator()
with open("sample.py", "r") as file:
	print(o.obfuscate(file.read()))
