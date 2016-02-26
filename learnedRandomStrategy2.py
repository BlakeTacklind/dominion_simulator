from __future__ import division
from B_card_classes import *
import random
from sklearn import svm, linear_model
from sklearn.externals import joblib
import pandas as pd

classifier = joblib.load('model.pkl')
percentDone = joblib.load('ridge.pkl')

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

	return [apc,apcf,dpc,dpcf,ds,dsf,ea,eaf,eb,ebf,gpc,gpcf,0,0,vc,vcf,victoryPoints,0]

def getPercentDone(bank):
	curPiles = [bank['Chapel'],bank['Copper'],bank['Duchy'],bank['Estate'],bank['Feast'],bank['Festival'],bank['Gold'],bank['Laboratory'],bank['Market'],bank['Money Lender'],bank['Province'],bank['Remodel'],bank['Silver'],bank['Smithy'],bank['Village'],bank['Workshop']]
	return percentDone.predict(pd.Series(curPiles).reshape(1, -1))
	# return sum([a*b for a,b in zip(olsPercentDone,curPiles)])

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

	info = getDeckData(player_info)
	info[12] = player_info.treasure
	info[13] = player_info.turn
	info[17] = getPercentDone(player_info.bank)
	# print info



	res = classifier.predict(pd.Series(info).reshape(1, -1))

	if res == 0:
		return "None"
	elif res == 1:
		return "Copper"
	elif res == 2:
		return "Silver"
	elif res == 3:
		return "Gold"
	elif res == 4:
		return "Estate"
	elif res == 5:
		return "Duchy"
	elif res == 6:
		return "Province"
	elif res == 7:
		return "Village"
	elif res == 8:
		return "Chapel"
	elif res == 9:
		return "Workshop"
	elif res == 10:
		return "Smithy"
	elif res == 11:
		return "Money Lender"
	elif res == 12:
		return "Remodel"
	elif res == 13:
		return "Feast"
	elif res == 14:
		return "Market"
	elif res == 15:
		return "Festival"
	elif res == 16:
		return "Laboratory"

	# l = getPossibleList(player_info.bank, amount)

	# if not Nones:
	# 	l.remove("None")

	# numbers = list()
	# names = list()
	
	# for key in l:
	# 	numbers.append(sum([a*b for a,b in zip(vec_dict[key],info)]))
	# 	names.append(key)

	# return names[numbers.index(max(numbers))]

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

	if "Workshop" in possibleActions:
		if getCardByValues(player_info, 4, None) is "None":
			while "Workshop" in possibleActions:
				possibleActions.remove("Workshop")

	if "Feast" in possibleActions:
		if getCardByValues(player_info, 5, None) is "None":
			while "Feast" in possibleActions:
				possibleActions.remove("Feast")

	addExtraToList(possibleActions, "Laboratory")
	addExtraToList(possibleActions, "Market")
	addExtraToList(possibleActions, "Village")
	addExtraToList(possibleActions, "Festival")
	
	if not possibleActions:
		return "None"

	return random.choice(possibleActions)
