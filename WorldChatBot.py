import MaviewBot
import WorldChatMessage

class WorldChatBot(MaviewBot.MaviewBot):
	def __init__(self):
		super().__init__()
		self.url = 'http://maview.nexon.com/Now/GetMessage'

	def fetch_new_message(self):
		res_json = self.fetch_json()
		return [WorldChatMessage.WorldChatMessage(msg) for msg in res_json]
