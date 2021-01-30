import itertools
from gameplay import Guest, Scenario
import csv
import collections
GameData = collections.namedtuple("GameData", ["guests", "scenarios"])

def reverse_order(player, scenario, game):
	game.players.reverse()
	game.scenario_deck_inactive.place(scenario)

def skip_player(player, scenario, game):
	game.scenario_deck_inactive.place(scenario)

def guest_exit(player, scenario, game):
	guest = player.choose(player.active_guests)
	# TODO: create ADT
	player.active_guests.remove(guest)
	if guest.scenario:
		scenario = guest.scenario
		guest.scenario = None
		game.scenario_deck_inactive.place(scenario)

	player.guests.append(guest)
	game.scenario_deck_inactive.place(scenario)

def target_murder(player, scenario, game):
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
		game.scenario_deck_inactive.place(guest.scenario)
		guest.scenario = None
		
	game.scenario_deck_inactive.place(scenario)

# New rule: cannot stack multiple buffs
# must filter out players with existing scenario card
def protect_guest(player, scenario, game):
	
	filtered = [g for g in player.active_guests if not g.scenario]
	if not filtered:
		print("All your guests already have active scenarios!")
		game.scenario_deck_inactive.place(scenario)
	else:
		guest = player.choose(filtered)
		guest.killable = False
		guest.scenario = scenario

actions = {
	"SKIP": skip_player,
	"EXIT": guest_exit,
	"TARGET_MURDER": target_murder,
	"PROTECT_GUEST": protect_guest,
	"REVERSE": reverse_order
}

def convert_csv(path):

	guests = []
	scenarios = []

	with open(path, "r") as file:
		reader = csv.DictReader(file)
		# put conversion from dictionary to data into another function
		for row in reader:
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