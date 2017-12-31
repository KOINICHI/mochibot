import math
import re

def group_by(lst, members=10):
	""" Turn a list into a list of list where each item in the outer list contains
		`members` members. Last list of the outer list can contain less than
		`members` members."""
	ret = []
	for i in range(math.ceil(len(lst) / members)):
		ret.append(lst[i * members : (i + 1) * members])
	return ret

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
