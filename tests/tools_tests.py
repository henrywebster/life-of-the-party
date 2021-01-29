import unittest
from lotp.tools import convert_csv, GameData

class TestConvertCsv(unittest.TestCase):

	def test_convert_csv(self):

		data = convert_csv("data.csv")
		guests = data.guests
		self.assertEqual(1, len(guests))
		self.assertEqual("Jay Gatsby", guests[0].title)