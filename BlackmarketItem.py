import re

def strip_tags(s):
	return re.sub('<[^<]+?>', '', s)
def remove_commas(s):
	return re.sub(',', '', s)

class BlackmarketItem:

	def __init__(self, item):
		if item['action'] == "메소에 팔려!":
			self.type = 0
		if item['action'] == "메소에 매물로 나와!":
			self.type = 1
		if item['action'] == "판매 취소!":
			self.type = 2

		self.timestamp = item['time']
		self.time = item['HHmm'][1:-1]
		self.item_id = item['item_data']
		self.item_name = strip_tags(item['item_name'])
		self.price = -1
		if self.type in [0,1]:
			self.price = int(remove_commas(item['price']))

	def get_market_message(self):
		if self.type == 0:
			return "[{0}] {1} was sold for {2}".format(self.time, self.item_name, self.price)
		if self.type == 1:
			return "[{0}] {1} was listed for {2}".format(self.time, self.item_name, self.price)
		if self.type == 2:
			return "[{0}] {1} was cancelled".format(self.time, self.item_name)
