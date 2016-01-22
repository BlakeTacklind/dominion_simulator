from __future__ import division
from B_card_classes import *
import random
from lRSn_bestTry import olsPercentDone, vec_dict

#get list of cards and their costs in order
cardsByCost = [list() for i in range(9)]
for key in name_to_inst_dict:
	if key in all_cards_in_play_list:
		if key is not "Remodel" and key is not "Chapel":
			cardsByCost[name_to_inst_dict[key].cost].append(key)


def getDeckData(player_info):
	goldInDeck = sum([name_to_inst_dict[i].treasure for i in player_info.deck])
	goldInDeckFull = sum([name_to_inst_dict[i].treasure for i in player_info.hand+player_info.discard]) + goldInDeck
	
	extraActionsInDeck = sum([name_to_inst_dict[i].gain_actions for i in player_info.deck])
	extraActionsInDeckFull = sum([name_to_inst_dict[i].gain_actions for i in player_info.hand+player_info.discard]) + extraActionsInDeck
	#need to add existance check of gain_buy
	extraBuysInDeck = sum([name_to_inst_dict[i].gain_buys for i in player_info.deck])
	extraBuysInDeckFull = sum([name_to_inst_dict[i].gain_buys for i in player_info.hand+player_info.discard]) + extraBuysInDeck

	drawInDeck = sum([name_to_inst_dict[i].draw_cards for i in player_info.deck])
	drawInDeckFull = sum([name_to_inst_dict[i].draw_cards for i in player_info.hand+player_info.discard]) + drawInDeck

	victoryCardsInDeck = sum([name_to_inst_dict[i].grouping is 'Victory' for i in player_info.deck])
	victoryCardsInDeckFull = sum([name_to_inst_dict[i].grouping is 'Victory' for i in player_info.hand+player_info.discard])+victoryCardsInDeck

	actionsCardsInDeck = sum([name_to_inst_dict[i].grouping is 'Action' for i in player_info.deck])
	actionsCardsInDeckFull = sum([name_to_inst_dict[i].grouping is 'Action' for i in player_info.hand+player_info.discard])+actionsCardsInDeck
	
	victoryPoints = sum([name_to_inst_dict[i].victory for i in player_info.hand+player_info.discard+player_info.deck])

	deckSize = len(player_info.deck)
	deckSizeFull = deckSize+len(player_info.hand)+len(player_info.discard)

	ds=deckSize
	dsf=deckSizeFull
	gpcf=goldInDeckFull/deckSizeFull
	apcf=actionsCardsInDeckFull/deckSizeFull
	eaf=extraActionsInDeckFull/deckSizeFull
	ebf=extraBuysInDeckFull/deckSizeFull
	dpcf=drawInDeckFull/deckSizeFull
	vcf=victoryCardsInDeckFull/deckSizeFull

	if deckSize is 0:
		gpc=0
		apc=0
		ea=0
		eb=0
		dpc=0
		vc=0
	else:
		gpc=goldInDeck/deckSize
		apc=actionsCardsInDeck/deckSize
		ea=extraActionsInDeck/deckSize
		eb=extraBuysInDeck/deckSize
		dpc=drawInDeck/deckSize
		vc=victoryCardsInDeck/deckSize

	return [ds,dsf,gpc,gpcf,apc,apcf,ea,eaf,eb,ebf,dpc,dpcf,vc,vcf]

def getPercentDone(bank):
	curPiles = [1,bank["Village"],bank["Chapel"],bank["Workshop"],bank["Smithy"],bank["Money Lender"],bank["Remodel"],bank["Feast"],bank["Market"],bank["Festival"],bank["Laboratory"],bank["Copper"],bank["Silver"],bank["Gold"],bank["Estate"],bank["Duchy"],bank["Province"]]
	return sum([a*b for a,b in zip(olsPercentDone,curPiles)])

def getPossibleList(bank, treasure):
	cards = ["None"]

	if treasure > 8:
		treasure = 8

	for i in range(0,treasure+1):
		cards+=cardsByCost[i]

	for key in cards:
		if key is not "None":
			if bank[key] is 0:
				cards.remove(key)

	return cards

def getCardByValues(player_info, amount, Nones):

	info = [1, amount]+getDeckData(player_info)+[getPercentDone(player_info.bank)]
	# print info

	l = getPossibleList(player_info.bank, amount)

	if not Nones:
		l.remove("None")

	numbers = list()
	names = list()
	
	for key in l:
		numbers.append(sum([a*b for a,b in zip(vec_dict[key],info)]))
		names.append(key)

	adjusted = numbers
	adjusted = []
	for n in numbers:
		if n < 0:
			adjusted.append(0)
		else:
			adjusted.append(n)

	r = random.random() * sum(adjusted)

	for i in range(0, len(names)):
		if adjusted[i] > r:
			return names[i]
		else:
			r-=adjusted[i]

	print "-----------------Oops"
	return "None"

def buy_choice(player_info):
	return getCardByValues(player_info, player_info.treasure, True)

def execute_action_strategy(player_info, action):
	if action.name == 'Remodel':
		return

	elif action.name == 'Workshop':
		card = getCardByValues(player_info, 4, False)
		return card
	
	elif action.name == 'Feast':
		card = getCardByValues(player_info, 5, False)

		return card
	
	elif action.name == 'Chapel':
		return []
	
	elif action.name == 'Money Lender':
		return 'Copper'

	else:
		return 'None'

biasExtraActions = 10
def addExtraToList(lst, action):
	for i in range(0, lst.count(action)):
		lst = lst + [action]*biasExtraActions

def action_choice(player_info):

	possibleActions = [i.name for i in player_info.actions_available]
	if "Copper" not in player_info.hand:
		while "Money Lender" in possibleActions:
			possibleActions.remove("Money Lender")

	addExtraToList(possibleActions, "Laboratory")
	addExtraToList(possibleActions, "Market")
	addExtraToList(possibleActions, "Village")
	addExtraToList(possibleActions, "Festival")
	
	if not possibleActions:
		return "None"

	return random.choice(possibleActions)
