import unittest
from lotp.tools import convert_csv, GameData, reverse_order
from lotp.gameplay import Player, Rules, Game

class TestConvertCsv(unittest.TestCase):

	def test_convert_csv(self):

		data = convert_csv("data.csv")
		guests = data.guests
		#self.assertEqual(1, len(guests))
		self.assertEqual("Jay Gatsby", guests[0].title)

class TestScenarioActions(unittest.TestCase):

	def test_reverse_order(self):
		player_0 = Player("player")
		player_1 = Player("player")
		player_2 = Player("player")
		players = [player_0, player_1, player_2]

		game = Game([], [], players, Rules())
		current_player = players.pop(0)
		self.assertEqual(player_0, current_player)
		self.assertEqual(player_1, players[0])
		self.assertEqual(player_2, players[1])

		reverse_order(current_player, None, game)
		players.append(current_player)
		self.assertEqual(player_2, players[0])
		self.assertEqual(player_1, players[1])
		self.assertEqual(player_0, players[2])
		
