from threading import Lock
import discord
import requests, asyncio
import re, json

import BlackmarketItem

class BlackmarketBot:
	def __init__(self):
		self.watchlist_filename = "watchlist.json"
		with open(self.watchlist_filename, 'r') as f:
			self.watchlist = json.load(f)
		self.last_updated = 0
		self.url = 'http://maview.nexon.com/Now/GetMessageMarket'
		self.request_headers = {
			'Accept' : 'application/json',
			'Accept-Encoding' : 'gzip, deflate, sdch',
			'Accept-Language' : 'ko',
			'Connection' : 'keep-alive',
			'DNT' : '1',
			'Host' : 'maview.nexon.com',
			'Referer' : 'http://maview.nexon.com/',
			'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
			'X-Requested-With' : 'XMLHttpRequest'
			'Cookie' 'PCID=14944728485621834338678; A2SK=act02:15960043732999717153; A2SR=http%253A%252F%252Fmaview.nexon.com%252F%3A1494472911435%3A0; _ga=GA1.2.285890743.1494472850; _gid=GA1.2.73831708.1494472912; IsMobile=; TweetsSearchTime=; _gat=1; NXGID=9C0187ACD1D497880B395933E97A01CB; NXLW=SID=D47E9EEE9CA83EF02DA4377C5C5AA334&PTC=http:&DOM=maview.nexon.com&ID=&CP=; NXPID=9FE7C248108465868BA58C1045406103; HENC='
		}


	# Save the current watchlist
	def save_watchlist(self):
		with open(self.watchlist_filename, 'w') as f:
			f.write(json.dumps(self.watchlist))

	# Add to watchlist
	def add_watch(self, user_id, item_name, price_range):
		if user_id not in self.watchlist:
			self.watchlist[user_id] = {}
		if item_name not in self.watchlist[user_id]:
			self.watchlist[user_id][item_name] = {}
		self.watchlist[user_id][item_name]['low'] = price_range[0]
		self.watchlist[user_id][item_name]['high'] = price_range[1]
		self.save_watchlist()
		return True

	# Remove from watchlist
	def remove_watch(self, user_id, item_name):
		if user_id not in self.watchlist:
			return False
		if item_name not in self.watchlist[user_id]:
			return False
		del self.watchlist[user_id][item_name]
		if len(self.watchlist[user_id]) == 0:
			del self.watchlist[user_id]
		self.save_watchlist()
		return True

	# Get watchlist of user
	def get_watchlist(self, user_id):
		if user_id in self.watchlist:
			return self.watchlist[user_id]
		return {}

	def check_user_watch(self, user_id, item):
		if user_id not in self.watchlist:
			return False
		if item.item_name not in self.watchlist[user_id]:
			return False
		low = self.watchlist[user_id][item.item_name]['low']
		high = self.watchlist[user_id][item.item_name]['high']
		return low <= item.price and item.price <= high

	# Fetch the new items from maview API
	def fetch_new_items(self):
		try:
			res = requests.get(self.url, headers = self.request_headers)
			res_json = json.loads(res.content.decode('utf-8'))
			res_json = list(filter(lambda item: int(item['time']) > self.last_updated, res_json))
		except:
			print ("Failed to fetch new items")
			return []

		if len(res_json) > 0:
			self.last_updated = int(res_json[-1]['time'])

		return [BlackmarketItem.BlackmarketItem(item) for item in res_json]

	# Get dictionary of player to list of items to notify given the list of items
	# i.e. {user: [items, ...], ...}
	def get_players_to_notify(self, new_items):
		ret = {}
		for user_id in self.watchlist:
			for item in new_items:
				if self.check_user_watch(user_id, item):
					if user_id not in ret:
						ret[user_id] = []
					ret[user_id].append(item)
		return ret
