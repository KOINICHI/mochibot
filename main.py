import MochiBot

def main():
	token = None
	with open('keys') as f:
		token = f.readline().strip()
	if token is not None:
		mochi_bot = MochiBot.MochiBot(token)
		mochi_bot.start_mochi_bot()
	else:
		print ("Invalid Token")

if __name__ == '__main__':
	while True:
		main()
