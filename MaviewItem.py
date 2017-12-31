
class MaviewItem():
	def __init__(self, item):
		self.timestamp = item['time']
		self.time = item['HHmm'][1:-1]
