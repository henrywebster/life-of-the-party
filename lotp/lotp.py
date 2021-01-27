import random

# TODO: define a rule constant or config file?
class Rules:
	def __init__(self):
		self.guest_hand_size = 1

class Guest:
	def __init__(self, title, quotation, description):
		self.title = title
		self.quotation = quotation
		self.description = description

class Scenario:
	def __init__(self, title, quotation, description):
		self.title = title
		self.quotation = quotation
		self.description = description

class Player:
	def __init__(self, name):
		self.name = name
		self.active = True
		self.guests = []

	def add_guest(self, guest):
		self.guests.append(guest)

class Deck:
	def __init__(self, cards = [], seed = None):
		self.cards = cards
		random.seed(seed)

	def draw(self):
		if not self.cards:
			raise ValueError("Cannot draw from empty deck")
		return self.cards.pop()

	def place(self, card):
		self.cards.append(card)

	def size(self):
		return len(self.cards)

	# TODO how to unit test? -- use same seed value
	def shuffle(self):
		random.shuffle(self.cards)

class Game:
	def __init__(self, guests, scenarios, players, rules):
		self.scenario_deck_active = Deck(scenarios)
		self.scenario_deck_inactive = Deck()
		self.guest_deck = Deck(guests)
		self.players = players
		self.rules = rules

	def __deal_guests(self):
		# TODO: more natural to do cards then players?
		for player in self.players:
			for _ in range(self.rules.guest_hand_size):
				guest = self.guest_deck.draw()
				player.add_guest(guest)

	def setup(self):
		self.guest_deck.shuffle()
		self.scenario_deck_active.shuffle()
		self.__deal_guests()

	def round(self):
		for player in self.players:
			if not player.active:
				continue
			# have two implementations: computer and human player
			print(player.name)
			scenario = self.scenario_deck_active.draw()
			# scenario.effect

			# check if no one has cards left
			for _player in self.players:
				if not _player.guests:
					# player is taken out of game
					_player.active = False

			print(scenario.title)

		# TODO: clean up players after?
