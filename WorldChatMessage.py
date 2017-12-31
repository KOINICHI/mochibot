from utils import strip_tags, remove_commas

import MaviewItem

class WorldChatMessage(MaviewItem.MaviewItem):
	def __init__(self, item):
		super().__init__(item)

		self.message = item['message']
		self.char_name = item['ch_name']
		self.type = strip_tags(item['type'])[1:-1]

	def get_worldchat_message(self):
		return "[{0}] [{1}] {2} : {3}".format(self.time, self.type, self.char_name, self.message)
