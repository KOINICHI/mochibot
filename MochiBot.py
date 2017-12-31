import discord
from discord.ext import commands

import random, os, re, itertools, time, datetime, math
import asyncio

from utils import unquote
import CardBot, EnchantBot, BlackmarketBot

class MochiBot(commands.Bot):
	def __init__(self, token):
		super().__init__(self)
		self.command_prefix = "!!"
		self.description    = "Hello :D"

		# IDs
		self.my_server        = '220988375946100736'
		self.my_blackmarket   = '221750533755633675'

		# Log fp
		self.log_file = open('log.txt', 'a', encoding='utf-8')

		# Login token
		self.token = token

		# Sub-bots
		self.blackmarket_bot = BlackmarketBot.BlackmarketBot()
		self.enchant_bot = EnchantBot.EnchantBot()
		self.card_bot = CardBot.CardBot()

		self.remove_command('help')

		# Add commands
		@self.command(pass_context=True)
		async def help(ctx):
			await self._help(ctx)
		@self.command(pass_context=True)
		async def whoami(ctx):
			await self._whoami(ctx)
		@self.command(pass_context=True)
		async def enchant(ctx):
			await self._enchant(ctx)
		@self.command(pass_context=True)
		async def inventory(ctx):
			await self._inventory(ctx)
		@self.command(pass_context=True)
		async def draw(ctx):
			await self._draw(ctx)
		@self.command(pass_context=True)
		async def shuffle(ctx):
			await self._shuffle(ctx)
		@self.command(pass_context=True)
		async def watch(ctx):
			await self._watch(ctx)
		@self.command(pass_context=True)
		async def unwatch(ctx):
			await self._unwatch(ctx)
		@self.command(pass_context=True)
		async def watchlist(ctx):
			await self._watchlist(ctx)


	def log(self, msg):
		msg = "{0} : {1}".format(datetime.datetime.now(), msg)
		print (msg)
		#self.log_file.write(msg + '\n')

	async def blackmarket_notification_task(self):
		def group_by(lst, members=10):
			ret = []
			for i in range(math.ceil(len(lst) / members)):
				ret.append(lst[i * members : (i + 1) * members])
			return ret

		await self.wait_until_ready()
		self.log("Blackmarket bot started")

		server = self.get_server(self.my_server)
		channel = server.get_channel(self.my_blackmarket)
		while True:
			new_items = self.blackmarket_bot.fetch_new_items()
			self.log("{0} new items fetched from blackmarket".format(len(new_items)))
			for items in group_by(new_items, members=10):
				while True:
					try:
						await self.send_message(channel, '\n'.join([item.get_market_message() for item in items]))
						break
					except:
						continue

				players_items = self.blackmarket_bot.get_players_to_notify(new_items)
				for user_id in players_items:
					items = players_items[user_id]
					user = await self.get_user_info(user_id)
					await self.send_message(user, '\n'.join([item.get_market_message() for item in items]))

			await asyncio.sleep(1)

	def start_mochi_bot(self):
		self.loop.create_task(self.blackmarket_notification_task())
		self.run(self.token)

	###########################
	## Event handling begins ##
	###########################
	async def on_error(self, event, *args, **kwargs):
		msg = "error occured during event {0}...\n".format(event)
		self.log(msg)

	## Special case for commands
	async def on_message(self, msg):
		# Don't do anything if I said it
		if msg.author == self.user:
			return

		# Unflip the table!!
		if '(╯°□°）╯︵ ┻━┻' in msg.content:
			await self.send_message(msg.channel, random.choice([
				'┬─┬ ノ( ゜-゜ノ)',
				'┬─┬ ノ(  \'   -  \'ノ)',
				]));

		# Any message containing 'mochi' & 'bot' & ('die' | 'death'), react to it
		if 'mochi' in msg.content and 'bot' in msg.content and ('die' in msg.content or 'death' in msg.content):
			await self.send_message(msg.channel, ':cry: :dizzy_face:')

		# Fallback for other possible commands
		await self.process_commands(msg)

	async def on_ready(self):
		self.log("Logged in as {0} ({1})".format(self.user.name, self.user.id))

		self.card_bot.reshuffle()



	################################
	## Blacmkarket commands begin ##
	################################
	async def _watch(self, ctx):
		message = ctx.message
		author = message.author

		regex_pat = '^\\!\\!watch\\s\\"([^"\\\\]|\\\\.)*\\"\\s\\d+\\-\\d+$'
		if not re.match(regex_pat, message.content):
			await self.say("{0} Make sure you have the correct format : `!!watch \"<item name>\" <low>-<high>`".format(author.mention))
			return

		params = message.content.split(' ', 1)[1].rsplit(' ', 1)
		item_name = unquote(params[0])
		low, high = map(int, params[1].split('-'))
		self.blackmarket_bot.add_watch(author.id, item_name, (low, high))
		self.log("{0} watched \"{1}\" {2}-{3}".format(author.mention, item_name, low, high))

		await self.say("{0} watching \"{1}\" with price range {2}-{3}".format(author.mention, item_name, low, high))

	async def _unwatch(self, ctx):
		message = ctx.message
		author = message.author

		params = message.content.split(' ', 1)[1]
		item_name = unquote(params)
		if not self.blackmarket_bot.remove_watch(author.id, item_name):
			self.say("{0} you weren't watching \"{1}\" but sure".format(author.mention, item_name))
			return
		self.log("{0} stopped watching {1}".format(author.mention, item_name))

		await self.say("{0} not watching \"{1}\" anymore".format(author.mention, item_name))

	async def _watchlist(self, ctx):
		message = ctx.message
		author = message.author

		watchlist = self.blackmarket_bot.get_watchlist(author.id)

		if len(watchlist) == 0:
			await self.say("{0} you are not watching anything".format(author.mention))
			return

		await self.send_message(author, "you are not watching:")
		reply = []
		for item in watchlist:
			low = watchlist[item]['low']
			high = watchlist[item]['high']
			reply.append("{0} : {1}-{2}".format(item, low, high))
			# Do not spam
			if len(reply) > 10:
				await self.send_message(author, '\n'.join(reply))
				reply = []
		if len(reply) > 0:
			await self.send_message(author, '\n'.join(reply))


	############################
	## Enchant commands begin ##
	############################
	async def _enchant(self, ctx):
		message = ctx.message
		author = message.author

		result, lv = self.enchant_bot.enchant(author.id)

		reply = "Sorry I can't enchant that"
		if result == 'error':
			reply = "You have a +15??? What?? It's a bug. No worries, it's been reported and handled. Try it again"
		if result == 'fail':
			reply = random.choice([
					"Sorry, it's still **+{0}**".format(lv),
					"Sorry, Failed",
					"Oh no, it failed",
					"You failed but it didn't cost anything :wink:"])
			if random.random() < 0.0001:
				reply = ":poop: Blame Aya :poop: :poop: Aya debuff :poop: \n" \
						"Aside, you made through 0.01%; be proud!!"
		if result == 'unstable':
			reply = "Sorry, your weapon is now unstable, can't enchant that anymore"
		if result == 'success':
			reply = random.choice([
					"Nice, you got a **+{0}** weapon!",
					"**+{0}**!",
					"**+{0}**, that was easy!",
					"Congratulations on successfully enchanting a **+{0}** weapon!"]).format(lv)
			if lv == 10:
				reply = "**+10**, The beginning of everything, good job :smiley:"
			if lv == 11:
				reply = "**+11**! Congratulations!!:"
			if lv == 12:
				reply = "**+12**!!, Don't be sad because it's not a real weapon :sob:"
			if lv == 13:
				reply = "**+13**?!? Please don't yolo your real one"
			if lv == 14:
				reply = "**+14**??? Is this a glitch or something"
			if lv == 15:
				reply = "**+15**? RIGGED BANNED RIGGED BANNED BANNED RIGGED BANNED BANNED BANNED RIGGED RIGGED"
		await self.say(author.mention + ' ' + reply)

	async def _inventory(self, ctx):
		message = ctx.message
		author = message.author

		inven = self.enchant_bot.inventory(author.id)
		trials = abs(inven['trials'])
		best = inven['best']
		current = inven['cur']
		unstables = {lv: cnt for lv, cnt in inven.items() if cnt > 0 and lv.isdigit()}

		reply = "Your current weapon is **+{0}**\n".format(current)
		reply += "You have tried enchanting **{0}** weapons\n".format(trials)
		if len(unstables) > 0:
			reply += "You have the following unstable weapons:\n"
			for lv, cnt in sorted(unstables.items(), key = lambda x:int(x[0])):
				reply += "    **{0}** × **+{1}**\n".format(cnt, lv)
		reply += "Your best weapon is **+{0}**\n".format(best)

		await self.say(author.mention + ' ' + reply)


	#########################
	## Card commands begin ##
	#########################
	async def _draw(self, ctx):
		message = ctx.message
		author = message.author
		if len(self.card_bot.cards) < 5:
			await self.say("Not enough cards, will reshuffle and draw")
			self.card_bot.reshuffle()

		params = message.content.split(' ')
		draw_count = 1000
		while draw_count > 0:
			draws = self.card_bot.draw(5)
			hand = self.card_bot.getHand(draws)
			if hand == "High Card" and random.random() < 0.001:
				break
			if hand == "One Pair" and random.random() < 0.01:
				break
			if hand == "Two Pair" and random.random() < 0.1:
				break
			if hand not in ["High Card", "One Pair", "Two Pair"] and random.random() < 0.25:
				break
			for card in draws:
				self.card_bot.addCardToDeck(card)
			draw_count -= 1
		self.log("{0} drew {1} ({2})\n".format(author.name, ', '.join(draws), hand))

		image_file = self.card_bot.compileImage(draws)
		await self.send_file(message.channel, image_file)
		os.remove(image_file)
		await self.say("{0} {1}".format(author.mention, hand))

	async def _shuffle(self, ctx):
		message = ctx.message
		author = message.author

		self.card_bot.reshuffle()
		self.log("{0} reshuffled\n".format(author.name))

		await self.say("{0} deck shuffled".format(author.mention))


	##########################
	## Other commands begin ##
	##########################
	async def _help(self, ctx):
		message = ctx.message
		author = message.author

		reply = ""
		reply += "`!!draw` to draw card\n"
		reply += "`!!shuffle` to reset and shuffle the deck\n"
		reply += "`!!enchant` to simulate enchanting weapons\n"
		reply += "`!!inventory` to view your enchant history\n"
		reply += "`!!watch \"<item name>\" <low>-<high>` to watch item with the price range\n"
		reply += "`!!unwatch \"<item name>\"` to stop watching the item\n"
		reply += "`!!watchlist` to view your watchlist"

		await self.send_message(author, reply)

	async def _whoami(self, ctx):
		message = ctx.message
		author = message.author

		reply = ""
		reply += "Hi, {0}\n".format(author.mention)
		reply += "You are {0}#{1} (id: {2})\n".format(author.display_name, author.discriminator, author.id)
		if author.bot:
			reply += "Huh? you are a bot too? why are you querying this?"
		reply += "Your avater url is {0}\n".format(author.avatar_url)
		reply += "You created your account at {0} UTC".format(author.created_at)

		await self.say(reply)
