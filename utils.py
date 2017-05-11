import re


def unquote(s):
	while s.startswith('"') or s.startswith("'"):
		s = s[1:]
	while s.endswith('"') or s.endswith("'"):
		s = s[:-1]
	return s

def strip_tags(s):
	return re.sub('<[^<]+?>', '', s)

def remove_commas(s):
	return re.sub(',', '', s)
