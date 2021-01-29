from objects import Game, Rules, Player
from tools import convert_csv

# TODO: read rules file
rules = Rules(2)

# TODO: generate players
#player_1 = Player("Ada")
#player_2 = Player("Ben")



# ask how many players
player_count = input("How many players? ")

# handle when user does not input number
# handle when number is more than 4
players = []
for i in range(int(player_count)):
	name = input("Player {} name: ".format(i + 1))
	player = Player(name)
	players.append(player)

game_data = convert_csv("data.csv")

game = Game(game_data.guests, game_data.scenarios, players, rules)

game.setup()
game.run()
