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

Village_vec=[-0.007193986,-8.97E-05,-2.05E-05,-0.000152307,0.000290872,0.005254131,0.000597279,0.005622346,-0.000683355,-0.004173564,0.004053161,0.006737224,-0.00157797,0.014303378,0.000820026,0.018533341,-0.001459205]
Chapel_vec=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Workshop_vec=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Smithy_vec=[-0.005298224,-4.49E-06,-6.34E-06,-8.94E-05,-0.000692636,0.004008895,-0.000253335,0.00230877,-0.002273038,0.011767145,0.002243755,-0.009739305,-0.000730723,0.004898469,-0.001431294,0.015163953,-0.001025344]
Money_Lender_vec=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Remodel_vec=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Feast_vec=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Market_vec=[-0.075177128,-0.006705461,-5.24E-05,0.000431867,0.015562319,0.085737201,0.002515206,0.029366942,0.032171067,0.062648521,-0.020726798,-0.016090937,-0.003898649,0.041543241,0.035707005,0.168793561,-0.04196938]
Festival_vec=[-0.002968596,-0.006505286,0.000232768,0.001626059,0.007850262,0.04992384,0.003586621,0.012325771,0.000573589,-0.004840408,0.004280606,0.028863043,0.005905667,0.012954677,0.025410726,-0.038309425,-0.035310029]
Laboratory_vec=[0.002853389,-0.006966911,0.000409829,0.001471037,0.009987959,0.056890049,0.0082832,0.028520489,0.016297113,-0.044892541,0.015624199,0.105045076,-0.007071712,0.025408931,0.022797215,-0.048217386,-0.048895342]
Copper_vec=[0.211399313,-0.024783666,0.000310313,-0.00081841,-0.010626262,-0.005766935,-0.01428697,0.043917031,-0.085066768,0.073476411,0.022423073,0.134236355,0.019782786,-0.075961672,0.016218865,-0.363560963,0.122578695]
Silver_vec=[0.736519341,-0.093279387,0.000146771,0.003712894,-0.034326271,-0.095530648,-0.015442136,-0.037025886,0.056482628,-0.186723713,-0.115148012,0.040845978,0.012338975,0.034800075,-0.159619297,1.530000155,-0.239376575]
Gold_vec=[0.322674871,0.032363935,-0.003307261,0.00340199,0.040962307,0.145065772,0.048784434,-0.020577852,-0.047009899,0.15058884,0.134971745,-0.192221875,0.058391454,-0.02010052,0.253734624,-1.618069504,-0.357927125]
Estate_vec=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Duchy_vec=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Province_vec=[-0.158139114,0.134509374,0.001752678,-0.009856287,-0.038945197,-0.337872604,-0.031704089,-0.116357521,-0.008962947,-0.150925523,-0.04560287,-0.017410787,-0.040546449,-0.180736253,-0.145692232,-0.182582998,0.607344971]
None_vec=[-0.024669866,-0.028538427,0.000534154,0.000272526,0.009936647,0.092290298,-0.00208021,0.051899911,0.038471611,0.093074832,-0.00211886,-0.080264773,-0.04259338,0.142889674,-0.047945639,0.518249265,-0.003960665]
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

	adjusted = numbers
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
