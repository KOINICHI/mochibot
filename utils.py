def unquote(s):
	while s.startswith('"') or s.startswith("'"):
		s = s[1:]
	while s.endswith('"') or s.endswith("'"):
		s = s[:-1]
	return s
