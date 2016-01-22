from __future__ import division
from B_card_classes import *
import random

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

	# print [name_to_inst_dict[i].treasure for i in player_info.hand]

	ds=deckSize
	dsf=deckSizeFull
	gpcd=goldInDeckFull/deckSizeFull
	apcd=actionsCardsInDeckFull/deckSizeFull
	ead=extraActionsInDeckFull/deckSizeFull
	ebd=extraBuysInDeckFull/deckSizeFull
	dpcd=drawInDeckFull/deckSizeFull
	vcd=victoryCardsInDeckFull/deckSizeFull

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

	return [ds,dsf,gpc,gpcd,apc,apcd,ea,ead,eb,ebd,dpc,dpcd,vc,vcd]

olsPercentDone=[0.006171295825915867,-0.03929716609354948,0.06171295825915912,0.06171295825915911,-0.04043105829468707,0.06171295825915908,0.06171295825915912,0.0617129582591593,-0.01151536461513331,-0.01593498126166915,-0.01682325262599091,-0.008103989465298566,-0.02143234307974589,-0.02958797640972152,0.04937036660732755,0.01166761765558321,-0.04872408575542178]
def getPercentDone(bank):
	curPiles = [1,bank["Village"],bank["Chapel"],bank["Workshop"],bank["Smithy"],bank["Money Lender"],bank["Remodel"],bank["Feast"],bank["Market"],bank["Festival"],bank["Laboratory"],bank["Copper"],bank["Silver"],bank["Gold"],bank["Estate"],bank["Duchy"],bank["Province"]]
	return sum([a*b for a,b in zip(olsPercentDone,curPiles)])

Village_vec=[-0.00462864,-0.00462864,-7.57E-05,-1.90E-05,-0.000103213,0.000240295,0.003503267,0.000418382,0.003651085,-0.000405327,-0.002805443,0.00268339,0.004403525,-0.001022919,0.009355174,0.000826424,0.011913609,-0.000927066]
Chapel_vec=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Workshop_vec=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Smithy_vec=[-0.003476165,-0.003476165,-2.95E-06,-4.16E-06,-5.86E-05,-0.000454439,0.002630236,-0.000166213,0.001514784,-0.00149134,0.007720424,0.001472128,-0.006389958,-0.000479427,0.003213886,-0.000939072,0.00994907,-0.000672728]
Money_Lender_vec=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Remodel_vec=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Feast_vec=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Market_vec=[-0.13138774,-0.13138774,-0.005615601,-0.000208495,0.000719908,0.017892239,0.104066304,0.004413006,0.033805746,0.021578819,0.097571454,-0.009961871,-0.042643053,0.00162207,0.046488835,0.026747473,0.288000675,-0.058988606]
Festival_vec=[-0.047682508,-0.047682508,-0.005590683,0.000166174,0.001881526,0.009062912,0.068161086,0.004877475,0.023351405,-0.014786992,0.023836515,0.026333011,0.006462463,0.003086406,0.039755236,0.019547207,0.042665061,-0.056249357]
Laboratory_vec=[-0.083945768,-0.083945768,-0.006724205,0.000219861,0.001072162,0.013135799,0.097537095,0.007158349,0.031399088,0.012857182,0.084254775,0.022039427,-0.066401751,-0.013421561,0.076344238,0.022320349,0.15903665,-0.065146693]
Copper_vec=[0.15867881,0.15867881,-0.022331991,0.000429507,-0.000559905,-0.010562193,0.011090894,-0.013655853,0.045523267,-0.073450452,0.053157048,0.015241698,0.123535822,0.017241196,-0.040123069,0.01593247,-0.270092325,0.101557056]
Silver_vec=[0.357446867,0.357446867,-0.088282469,-8.07E-05,0.005546505,-0.038685125,0.101401353,-0.027272818,0.013965902,0.081160589,-0.100552741,-0.160304481,-0.010330399,-0.002674563,0.152780846,-0.153286134,2.136998152,-0.368451958]
Gold_vec=[-0.192594153,-0.192594153,0.032133842,-0.002956079,0.00485695,0.040613608,0.418155309,0.051277168,0.026170773,-0.052792959,0.462605905,0.181580213,-0.551420917,0.025044251,0.16732733,0.248098766,-0.526408874,-0.54924721]
Estate_vec=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Duchy_vec=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Province_vec=[-0.967732657,-0.967732657,0.135021668,0.001323735,-0.010270028,-0.021142913,0.074320993,-0.032730792,0.012486369,-0.022769876,0.292971428,-0.020195762,-0.394774861,-0.055226738,0.13926254,-0.156100492,1.66923623,0.357379079]
None_vec=[-0.110049113,-0.110049113,-0.02745425,0.000920758,0.000470386,0.010431164,0.142703544,-0.002089906,0.055752693,0.024952005,0.105190414,0.009509931,-0.092536233,-0.040731655,0.154603898,-0.044458062,0.634072414,-0.035766431]
vec_dict={"Village":Village_vec, "Chapel":Chapel_vec, "Workshop":Workshop_vec, "Smithy":Smithy_vec, "Money Lender":Money_Lender_vec, "Remodel":Remodel_vec, "Feast":Feast_vec, "Market":Market_vec, "Festival":Festival_vec, "Laboratory":Laboratory_vec, "Copper":Copper_vec, "Silver":Silver_vec, "Gold":Gold_vec, "Estate":Estate_vec, "Duchy":Duchy_vec, "Province":Province_vec, "None":None_vec}

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

	# print str([(name, n) for name, n in zip(names, numbers)])
	#normilize num
	# if min(numbers) < 0:
	# 	m = min(numbers)
	# 	print m
	# 	numbers = [i-m for i in numbers]
	
	# if max(numbers) < 0:
	# 	print numbers
	# 	numbers = [-1/i for i in numbers]

	# adjusted = numbers

	adjusted = []
	for n in numbers:
		if n < 0:
			adjusted.append(0)
		else:
			adjusted.append(n)

	# print str(amount)
	# print str([(name, n) for name, n in zip(names, adjusted)])

	# got = max([(name, n) for name, n in zip(names, adjusted)],key=lambda item:item[1])[0]
	# print got
	# return got

	r = random.random() * sum(adjusted)
	# print r
	for i in range(0, len(names)):
		if adjusted[i] > r:
			# print "bought ", names[i]
			return names[i]
		else:
			r-=adjusted[i]

	print "-----------------Oops"
	return "None"

def buy_choice(player_info):
	# print
	# print player_info.hand
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

biasExtraActions = 5
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
	
	return random.choice(possibleActions + ['None'])
