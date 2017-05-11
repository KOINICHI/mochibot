import os
import random

from PIL import Image

class CardBot:
	def __init__(self):
		self.cards = []

	def reshuffle(self):
		self.cards = set([s+n for s in 'shcd' for n in 'a234567890jqk'])

	def draw(self, n):
		draws = random.sample(self.cards, n)
		set(map(self.cards.remove, draws))
		return draws

	def getCardFilename(self, card):
		n,s = card
		return os.path.join('cards', n + s + '.png')

	def compileImage(self, cards):
		ret = Image.new('RGB', (500, 145), 'White')
		x = 0
		for i in map(Image.open, map(self.getCardFilename, cards)):
			ret.paste(i, (x, 0))
			x += 100
		filename = ''.join(cards) + '.png'
		ret.save(filename)
		return filename

	def addCardToDeck(self, card):
		self.cards.add(card)

	def isRoyalFlush(self, cards):
		if not self.isStraightFlush(cards):
			return False
		return cards[0][0] == 10
	def isStraightFlush(self, cards):
		return self.isStraight(cards) and self.isFlush(cards)
	def isFourOfAKind(self, cards):
		return (cards[1][0] == cards[2][0] == cards[3][0]) and (cards[0][0] == cards[1][0] or cards[3][0] == cards[4][0])
	def isFullHouse(self, cards):
		return cards[0][0] == cards[1][0] == cards[2][0] and cards[3][0] == cards[4][0] or \
				cards[0][0] == cards[1][0] and cards[2][0] == cards[3][0] == cards[4][0]
	def isFlush(self, cards):
		suit = cards[0][1]
		for card in cards:
			if card[1] != suit:
				return False
		return True
	def isStraight(self, cards):
		first = cards[0][0]
		for card in cards:
			if first != card[0]:
				return False
			first += 1
		return True
	def isThreeOfAKind(self, cards):
		return cards[0][0] == cards[1][0] == cards[2][0] or \
				cards[1][0] == cards[2][0] == cards[3][0] or \
				cards[2][0] == cards[3][0] == cards[4][0]
	def isTwoPair(self, cards):
		return cards[0][0] == cards[1][0] and cards[2][0] == cards[3][0] or \
				cards[1][0] == cards[2][0] and cards[3][0] == cards[4][0] or \
				cards[0][0] == cards[1][0] and cards[3][0] == cards[4][0]
	def isOnePair(self, cards):
		return cards[0][0] == cards[1][0] or \
				cards[1][0] == cards[2][0] or \
				cards[2][0] == cards[3][0] or \
				cards[3][0] == cards[4][0]

	def getHand(self, cards):
		toN = {'0': 10, 'j': 11, 'q': 12, 'k': 13, 'a': 14}
		for i in range(2, 11):
			toN[str(i)] = i
		cards = list(map((lambda x: (toN[x[1]], x[0])), cards))
		cards.sort()
		if self.isRoyalFlush(cards):
			return "Royal Flush"
		if self.isStraightFlush(cards):
			return "Straight Flush"
		if self.isFourOfAKind(cards):
			return "4 of A Kind"
		if self.isFullHouse(cards):
			return "Full House"
		if self.isFlush(cards):
			return "Flush"
		if self.isStraight(cards):
			return "Straight"
		if self.isThreeOfAKind(cards):
			return "Three Of A Kind"
		if self.isTwoPair(cards):
			return "Two Pair"
		if self.isOnePair(cards):
			return "One Pair"
		return "High Card"
