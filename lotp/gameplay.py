import random
import collections

DeckPair = collections.namedtuple("DeckPair", ["active", "discard"])

# TODO: define a rule constant or config file?
class Rules:
	def __init__(self, guest_hand_size = 1):
		self.guest_hand_size = guest_hand_size

class Guest:
	def __init__(self, title, quotation, description):
		self.title = title
		self.quotation = quotation
		self.description = description
		self.killable = True
		self.scenario = None
	
	def __str__(self):
		return "\t{} ({}) - {}".format(self.title, self.description, self.quotation)

class Scenario:
	def __init__(self, title, quotation, description, action):
		self.title = title
		self.quotation = quotation
		self.description = description
		self.action = action
	
	def act(self, player, game):
		self.action(player, self, game)

	def __str__(self):
		return "\t{} - {}\n\t{}".format(self.title, self.quotation, self.description)

class Player:
	def __init__(self, name):
		self.name = name
		self.active = True
		self.skip = False
		self.guests = []
		self.active_guests = []

class ComputerPlayer(Player):
	def __init__(self, name):
		super().__init__(name)

	def turn(self):
		pass

	def choose(self, guests):
		return random.choice(guests)

class HumanPlayer(Player):
	def __init__(self, name):
		super().__init__(name)

	def turn(self):
		while True:
			print("(d) draw, (h) see hand, (a) see active guests")
			choice = input("{}: ".format(self.name))
			if choice == "d":
				break
			elif choice == "h":
				for guest in self.guests:
					# TODO: custom print function
					print(guest)
			elif choice == "a":
				for guest in self.active_guests:
					print(guest)
			else:
				assert False

	def choose(self, guests):
		print("Choose guest")
		for i in range(len(guests)):
			print("\t{}:\t{}".format(i + 1, guests[i].title))
		# what if guest is outside range?
		choice = int(input("{}: ".format(self.name)))
		return guests[choice - 1]

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
				player.guests.append(guest)

	def setup(self):
		self.guest_deck.shuffle()
		self.scenario_deck_active.shuffle()
		self.__deal_guests()

		# initial card placement
		for player in self.players:
			guest = player.choose(player.guests)
			player.guests.remove(guest)
			player.active_guests.append(guest)


	def round(self):
		
		player = self.players.pop(0)

		if not player.active_guests:
			print("{} has no active guests and must play one".format(player.name))
			guest = player.choose(player.guests)
			player.guests.remove(guest)
			player.active_guests.append(guest)
		else:
			# change to status?
			player.turn()
			scenario = self.scenario_deck_active.draw()
			print(scenario)
			scenario.act(player, self)

			if self.scenario_deck_active.size() == 0:
				self.scenario_deck_active, self.scenario_deck_inactive = self.scenario_deck_inactive, self.scenario_deck_active
				self.scenario_deck_active.shuffle()

		self.players.append(player)
		# check if no one has cards left
		print("TURN ORDER")
		removals = []
		for _player in self.players:
			print(_player.name)
			if not _player.guests and not _player.active_guests:
				removals.append(_player)

		for _player in removals:
			print("{} has been eliminated!".format(_player.name))
			self.players.remove(_player)

#		for player in self.players:
#			if not player.active:
#				continue
#
#			if not player.active_guests:
#				print("{} has no active guests and must play one".format(player.name))
#				guest = player.choose(player.guests)
#				player.guests.remove(guest)
#				player.active_guests.append(guest)
#			else:
#				# change to status?
#				player.turn()
#				scenario = self.scenario_deck_active.draw()
#				print(scenario)
#				scenario.act(player, self)
#
#				# possible this is not done
#				#self.scenario_deck_inactive.place(scenario)
#
#				# Have deck group object, with swap, active, inactive
#
#				# TODO: unit test this
#				if self.scenario_deck_active.size() == 0:
#					self.scenario_deck_active, self.scenario_deck_inactive = self.scenario_deck_inactive, self.scenario_deck_active
#					self.scenario_deck_active.shuffle()
#
#			# check if no one has cards left
#			for _player in self.players:
#				if not _player.guests and not _player.active_guests:
#					# player is taken out of game
#					_player.active = False
#
#
#		# TODO: clean up players after?




	def run(self):
		while self.players:
			self.round()