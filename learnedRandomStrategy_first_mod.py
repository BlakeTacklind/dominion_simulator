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

olsPercentDone=[0.014954465,-0.011014872,0.149544654,0.003494926,-0.026260187,-0.016535603,0.149544654,-0.005303709,-0.013212782,-0.007973532,-0.017445924,-0.003796381,-0.018908398,-0.029986546,-0.000302217,0.016660336,-0.061304149]
def getPercentDone(bank):
	curPiles = [1,bank["Village"],bank["Chapel"],bank["Workshop"],bank["Smithy"],bank["Money Lender"],bank["Remodel"],bank["Feast"],bank["Market"],bank["Festival"],bank["Laboratory"],bank["Copper"],bank["Silver"],bank["Gold"],bank["Estate"],bank["Duchy"],bank["Province"]]
	return sum([a*b for a,b in zip(olsPercentDone,curPiles)])


Village_vec=[0.02159609,-0.012302108,0.000266109,0.000199315,0.004566928,0.040418813,0.001069097,0.024369423,-0.001435959,0.010370676,0.024554479,-0.020397249,0.000972323,0.030966404,0.001183019,0.083522901,-0.009615827]
Chapel_vec=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Workshop_vec=[-0.013487231,-0.008814494,0.000176529,0.000635239,0.002751283,0.037771369,0.009193879,0.017632922,0.002527202,-0.014392777,-0.019604298,0.047867533,-0.001914662,0.008772677,0.00497348,0.068405522,0.009050578]
Smithy_vec=[0.228757351,-0.014494523,-4.81E-05,0.003970354,-0.025598707,-0.029124959,0.017148978,-0.509905097,-0.029595125,0.138883628,0.038958296,-0.084290418,-0.001183448,-0.017746808,-0.008235696,0.073939739,-0.115547263]
Money_Lender_vec=[0.091493926,-0.010871768,6.27E-05,0.002865538,-0.010152033,0.005575017,-0.015562451,-0.120058261,-0.005373387,0.016385015,0.036336394,-0.06601825,0.009593367,-0.040517768,0.002036728,0.026598045,-0.045968195]
Remodel_vec=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Feast_vec=[0.021121857,-0.009519634,0.000208192,0.001807505,0.000885247,0.030042898,-0.007434371,-0.002831252,3.80E-06,-0.023421299,0.019440463,-0.038594905,0.010043151,-0.018879555,0.010904352,0.026329146,-0.013000368]
Market_vec=[-0.000373207,-0.003944707,-5.74E-05,0.000240402,0.004483945,0.037685667,0.01653364,-0.026375324,0.019242458,-0.066050731,-0.102708067,0.36767639,-0.007601634,0.039031968,0.009834508,-0.004070669,-0.004578732]
Festival_vec=[-0.003203168,-0.00404167,1.76E-05,0.000139412,0.00427229,0.036933958,0.018659986,-0.031587534,-0.018863297,0.042603438,-0.045041314,0.217667417,0.000177194,0.014131196,0.015269854,0.010504576,-0.004821275]
Laboratory_vec=[0.007328703,-0.003986744,-2.67E-05,0.00017444,0.005456728,0.037480704,0.001101108,0.001168353,-0.015352453,0.056830266,0.034846498,-0.118586637,-0.001989775,0.034732008,0.021190164,-0.031300175,-0.008528514]
Copper_vec=[-0.004594993,-0.004714172,0.000113262,4.23E-05,0.000703652,0.016348013,-0.004964008,0.053714887,-0.001973131,0.003987854,0.001336294,-0.020612353,0.000650558,-0.000835105,-0.001654878,0.044733876,0.004315015]
Silver_vec=[0.517356817,-0.030744564,0.000322319,0.001645843,-0.03302616,-0.147688382,-0.091089428,-0.086303835,0.054648697,-0.208438096,-0.017718548,0.081426506,-0.025669488,0.037446235,-0.183204793,0.429123776,-0.244939858]
Gold_vec=[0.307230817,0.045162353,-0.006351182,-0.007397775,0.066723131,0.022251511,0.188125154,-0.214174779,-0.046056544,-0.002716126,0.057967249,-0.096710942,0.029452877,0.19873776,0.240788472,-0.618728042,-0.204929356]
Estate_vec=[-0.044735714,-0.032276294,0.000783331,0.001280041,0.004984815,0.125228657,0.012914739,0.128719976,0.00808842,0.000792295,-0.00583849,0.038545956,-0.004221674,0.047516977,0.00755803,0.288697665,0.032056061]
Duchy_vec=[-0.051677483,-0.007125328,0.000471322,0.001219417,0.002869469,0.06201241,0.017246346,-0.015140451,-0.005531094,0.0063898,0.016809065,0.007922803,-0.004513708,0.041452935,0.00935464,0.099685569,0.012513981]
Province_vec=[-0.593664752,0.122350708,0.002298998,-0.00187818,-0.029975192,-0.035021535,-0.098970857,-0.355104221,0.040516081,-0.113211252,-0.02252601,0.115342032,-0.004672924,0.03475834,-0.104707181,0.430808562,0.343356258]
None_vec=[-0.021147967,-0.025119078,0.000624844,-0.000367267,0.004698235,0.095538714,-0.021757423,0.225630182,-0.002574016,0.033886027,0.005629907,-0.025739999,-0.001406398,0.013636215,-0.012260456,0.243412811,0.020901531]
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
