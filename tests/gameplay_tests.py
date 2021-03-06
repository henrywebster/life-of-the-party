import random
import unittest
from lotp.gameplay import Guest, Scenario, Player, Deck, Game, Rules

def create_guest():
	return Guest("Example Guest", "An excerpt", "This guest is an example")

def create_scenario():
	return Scenario("Example Scenario", "An excerpt", "Description of excerpt", None)

class TestCard(unittest.TestCase):

	def test_constructor(self):
		guest = Guest("Example Guest", "An excerpt", "This guest is an example")
		self.assertEqual("Example Guest", guest.title)
		self.assertEqual("An excerpt", guest.quotation)
		self.assertEqual("This guest is an example", guest.description)

class TestScenario(unittest.TestCase):

	def test_constructor(self):
		action = lambda x,y,z: None
		scenario = Scenario("Example Scenario", "An excerpt", "This scenario is an example", action)
		self.assertEqual("Example Scenario", scenario.title)
		self.assertEqual("An excerpt", scenario.quotation)
		self.assertEqual("This scenario is an example", scenario.description)
		self.assertEqual(action, scenario.action)
	
class TestPlayer(unittest.TestCase):

	def test_constructor(self):
		player = Player("player1")
		self.assertEqual("player1", player.name)
		self.assertTrue(player.active)
		self.assertFalse(player.guests)

class TestDeck(unittest.TestCase):

	def test_default_constructor(self):
		deck = Deck()
		self.assertEqual(0, deck.size())

	def test_size(self):
		guest = create_guest()
		deck = Deck([guest])
		self.assertEqual(1, deck.size())

	def test_draw(self):
		guest = create_guest()
		deck = Deck([guest])
		self.assertEqual(guest, deck.draw())
		self.assertEqual(0, deck.size())
	
	def test_draw_empty_exception(self):
		deck = Deck()
		self.assertRaisesRegex(ValueError, "Cannot draw from empty deck", deck.draw)

	def test_shuffle(self):
		guest_1 = create_guest()
		guest_2 = create_guest()
		deck = Deck([], 100)		
		deck.place(guest_1)
		deck.place(guest_2)
		deck.shuffle()
		self.assertEqual(guest_1, deck.draw())
		self.assertEqual(guest_2, deck.draw())

	def test_place(self):
		guest = create_guest()
		deck = Deck()
		deck.place(guest)
		self.assertEqual(1, deck.size())
		self.assertEqual(guest, deck.draw())

#class TestGame(unittest.TestCase):
#
#	def test_setup(self):
#		guest_1 = create_guest()
#		guest_2 = create_guest()
#		scenario_1 = create_scenario()
#		scenario_2 = create_scenario()
#		player_1 = Player("player1")
#		player_2 = Player("player2")			
#		rules = Rules()
#
#		game = Game([guest_1, guest_2], [scenario_1, scenario_2], [player_1, player_2], rules)
#		game.setup()
#
#		players = game.players
#
#		self.assertEqual(2, len(players))
#		self.assertEqual(1, len(players[0].guests))
#		self.assertEqual(1, len(players[1].guests))

#	def test_round(self):
#		guest_1 = create_guest()
#		guest_2 = create_guest()
#		scenario_1 = create_scenario()
#		scenario_2 = create_scenario()
#		player_1 = Player("player1")
#		player_2 = Player("player2")			
#		rules = Rules()

#		game = Game([guest_1, guest_2], [scenario_1, scenario_2], [player_1, player_2], rules)
#		game.setup()
#		game.round()