from threading import Lock
import discord
import requests, asyncio
import re, json

import MaviewBot
import BlackmarketItem

class BlackmarketBot(MaviewBot.MaviewBot):
	def __init__(self):
		super().__init__()
		self.watchlist_filename = "watchlist.json"
		with open(self.watchlist_filename, 'r') as f:
			self.watchlist = json.load(f)
		self.url = 'http://maview.nexon.com/Now/GetMessageMarket'

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
		res_json = self.fetch_json()
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
