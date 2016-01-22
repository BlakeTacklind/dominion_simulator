from B_card_classes import *
import random

#get list of cards and their costs in order
cardsByCost = [list() for i in range(9)]
for key in name_to_inst_dict:
	if key in all_cards_in_play_list:
		if key is not "Remodel" and key is not "Chapel":
			cardsByCost[name_to_inst_dict[key].cost].append(key)

cards=0

chances = 5
nonechance = 5
# for i in range(1,9):
# 	cardsByCost[i] = cardsByCost[i]*(chances**i) + cardsByCost[i-1]

def getPossibleList(bank, treasure):

	if treasure > 8:
		treasure = 8

	cards = cardsByCost[treasure]

	# for i in range(0,treasure+1):
	# 	cards+=cardsByCost[i]

	for key in cards:
		# if key is not "None":
		if bank[key] is 0:
			cards.remove(key)

	return cards

def getCardWithChances(gold, num, bank):
	# print gold
	if gold is 0:
		return random.choice(['None']*num + ["Copper"])


	if random.randint(0, chances) is 0:
		return getCardWithChances(gold - 1, num, bank)

	cards = getPossibleList(bank, gold)

	if not cards:
		return getCardWithChances(gold - 1, num, bank)
	# print "choice"
	return random.choice(cards)

# c = dict()
# for i in range(10000):
# 	card = getCardWithChances(8, 10)
# 	if card not in c:
# 		c[card] = 1
# 	else:
# 		c[card] += 1

# print c

# print cardsByCost

def buy_choice(player_info):
	if player_info.treasure > 8:
		treasure = 8
	else:
		treasure = player_info.treasure

	return getCardWithChances(treasure, nonechance, player_info.bank)

def execute_action_strategy(player_info, action):
	global choices
	if action.name == 'Remodel':
		hand = list(player_info.hand)
		hand.remove("Remodel")

		remodeling = random.choice(hand)

		print "remodel ", remodeling
		remodelFor = name_to_inst_dict[remodeling].cost + 2
		if remodelFor > 8:
			remodelFor = 8

		card = getCardWithChances(remodelFor, 0, player_info.bank)
		# print "gain ", card

		return [remodeling, card]

	elif action.name == 'Workshop':
		card = getCardWithChances(4, 0, player_info.bank)
		# print "workshop: ", card
		return card
	
	elif action.name == 'Feast':
		card = getCardWithChances(5, 0, player_info.bank)

		# print "Feast: ", card
		return card
	
	elif action.name == 'Chapel':
		# hand = list(player_info.hand)
		# hand.remove("Chapel")

		return []
	
	elif action.name == 'Money Lender':
		return 'Copper'

	else:
		return 'None'

biasExtraActions = 5
def addExtraToList(lst, action):
	for i in range(0, lst.count(action)):
		lst = lst + [action]*biasExtraActions

def action_choice(player_info):
	# for key in cardsByCost[8]:
	# 	if player_info.bank[key] is 0:
	# 		for i in range(name_to_inst_dict[key].cost, len(cardsByCost)):
	# 			cardsByCost[i].remove(key)

	# print player_info.hand
	possibleActions = [i.name for i in player_info.actions_available]
	if "Copper" not in player_info.hand:
		while "Money Lender" in possibleActions:
			possibleActions.remove("Money Lender")

	addExtraToList(possibleActions, "Laboratory")
	addExtraToList(possibleActions, "Market")
	addExtraToList(possibleActions, "Village")
	addExtraToList(possibleActions, "Festival")
	
	return random.choice(possibleActions + ['None'])
