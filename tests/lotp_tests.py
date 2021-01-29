import random
import unittest
from lotp.objects import Guest, Scenario, Player, Deck, Game, Rules, ScenarioEvent

class TestCard(unittest.TestCase):

	def test_constructor(self):
		guest = Guest("Example Guest", "An excerpt", "This guest is an example")
		self.assertEqual("Example Guest", guest.title)
		self.assertEqual("An excerpt", guest.quotation)
		self.assertEqual("This guest is an example", guest.description)

class TestScenario(unittest.TestCase):

	def test_constructor(self):
		scenario = Scenario("Example Scenario", "An excerpt", "This scenario is an example")
		self.assertEqual("Example Scenario", scenario.title)
		self.assertEqual("An excerpt", scenario.quotation)
		self.assertEqual("This scenario is an example", scenario.description)
	
class TestPlayer(unittest.TestCase):

	def test_constructor(self):
		player = Player("player1")
		self.assertEqual("player1", player.name)
		self.assertTrue(player.active)
		self.assertFalse(player.guests)

	def test_add_guest(self):
		guest = Guest("Example Guest", "An excerpt", "This guest is an example")
		self.assertEqual("Example Guest", guest.title)
		player = Player("player1")
		self.assertFalse(player.guests)
		player.add_guest(guest)
		self.assertTrue(player.guests)
		self.assertEqual(guest, player.guests[0])

class TestDeck(unittest.TestCase):

	def test_default_constructor(self):
		deck = Deck()
		self.assertEqual(0, deck.size())

	def test_size(self):
		guest = Guest("Example Guest", "An excerpt", "This guest is an example")
		deck = Deck([guest])
		self.assertEqual(1, deck.size())

	def test_draw(self):
		guest = Guest("Example Guest", "An excerpt", "This guest is an example")
		deck = Deck([guest])
		self.assertEqual(guest, deck.draw())
		self.assertEqual(0, deck.size())
	
	def test_draw_empty_exception(self):
		deck = Deck()
		self.assertRaisesRegex(ValueError, "Cannot draw from empty deck", deck.draw)

	def test_shuffle(self):
		guest_1 = Guest("Example Guest", "An excerpt", "This guest is an example")
		guest_2 = Guest("Example Guest", "An excerpt", "This guest is an example")
		deck = Deck([], 100)		
		deck.place(guest_1)
		deck.place(guest_2)
		deck.shuffle()
		self.assertEqual(guest_1, deck.draw())
		self.assertEqual(guest_2, deck.draw())

	def test_place(self):
		guest = Guest("Example Guest", "An excerpt", "This guest is an example")
		deck = Deck()
		deck.place(guest)
		self.assertEqual(1, deck.size())
		self.assertEqual(guest, deck.draw())

class TestScenarioEvent(unittest.TestCase):
	def test_scenario_event(self):
		guest_1 = Guest("Example Guest", "An excerpt", "This guest is an example")
		guest_2 = Guest("Example Guest", "An excerpt", "This guest is an example")
		guests = [guest_1, guest_2]
		remove_guest_func = lambda guests: guests.pop()
		remove_guest_event = ScenarioEvent(remove_guest_func)
		remove_guest_event.run(guests)
		self.assertEqual(1, len(guests))

class TestGame(unittest.TestCase):

	def test_setup(self):
		guest_1 = Guest("Example Guest", "An excerpt", "This guest is an example")
		guest_2 = Guest("Example Guest", "An excerpt", "This guest is an example")
		scenario_1 = Scenario("Example Scenario", "An excerpt", "This scenario is an example")	
		scenario_2 = Scenario("Example Scenario", "An excerpt", "This scenario is an example")		
		player_1 = Player("player1")
		player_2 = Player("player2")			
		rules = Rules()

		game = Game([guest_1, guest_2], [scenario_1, scenario_2], [player_1, player_2], rules)
		game.setup()

		players = game.players

		self.assertEqual(2, len(players))
		self.assertEqual(1, len(players[0].guests))
		self.assertEqual(1, len(players[1].guests))

	def test_round(self):
		guest_1 = Guest("Example Guest", "An excerpt", "This guest is an example")
		guest_2 = Guest("Example Guest", "An excerpt", "This guest is an example")
		scenario_1 = Scenario("Example Scenario", "An excerpt", "This scenario is an example")	
		scenario_2 = Scenario("Example Scenario", "An excerpt", "This scenario is an example")		
		player_1 = Player("player1")
		player_2 = Player("player2")			
		rules = Rules()

		game = Game([guest_1, guest_2], [scenario_1, scenario_2], [player_1, player_2], rules)
		game.setup()
		game.round()