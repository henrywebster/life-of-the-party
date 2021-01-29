import itertools
from objects import Guest, Scenario
import csv
import collections
GameData = collections.namedtuple("GameData", ["guests", "scenarios"])

# TODO: unit test these all

def skip_player(player, players):
	pass

def guest_exit(player, players):
	guest = player.choose(player.active_guests)
	# TODO: create ADT
	player.active_guests.remove(guest)
	player.add_guest(guest)

def target_murder(player, game):
	excluded_list = [x for x in game.players if x != player]
	other_guests = list(itertools.chain(*[y.active_guests for y in excluded_list]))
	if not other_guests:
		print("No other active guests!")
		return
	guest = player.choose(other_guests)

	if guest.killable:
		# search for guest in all players
		# TODO: could be better
		for p in excluded_list:
			if guest in p.active_guests:
				# TODO: need graveyard?
				p.active_guests.remove(guest)
				break
	else:
		guest.killable = True

def protect_guest(player, game):
	guest = player.choose(player.active_guests)
	guest.killable = False

actions = {
	"SKIP": skip_player,
	"EXIT": guest_exit,
	"TARGET_MURDER": target_murder,
	"PROTECT_GUEST": protect_guest
}

def convert_csv(path):

	guests = []
	scenarios = []

	with open(path, "r") as file:
		reader = csv.DictReader(file)
		# put conversion from dictionary to data into another function
		for row in reader:
			#print(row)
			# change to enum
			if row["type"] == "guest":
				guest = Guest(row["title"], row["description"], row["source"])
				guests.append(guest)
			elif row["type"] == "scenario":
				scenario = Scenario(row["title"], row["description"], row["effect"], actions[row["action"]])
				scenarios.append(scenario)
			else:
				assert False

	return GameData(guests, scenarios)