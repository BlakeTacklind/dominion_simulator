import B_card_classes
import player_one_turn
from random import shuffle
from random import choice

import numpy as np
import pandas as pd


# actionData = pd.DataFrame(columns=['taken', 'treasure', 'buys', 'aquire', 'actions', 'startHand', 'EndHand'])

allCardInst = [B_card_classes.name_to_inst_dict[name] for name in B_card_classes.all_cards_in_play_list]

allCardInst = sorted(allCardInst, key=lambda c: c.cost)
for i in range(len(allCardInst)):
	allCardInst[i].key = i

# for i in allCardInst:
# 	print i.name, i.key


copper = B_card_classes.name_to_inst_dict['Copper']
estate = B_card_classes.name_to_inst_dict['Estate']
duchy = B_card_classes.name_to_inst_dict['Duchy']
monLen = B_card_classes.name_to_inst_dict['Money Lender']
chapel = B_card_classes.name_to_inst_dict['Chapel']
remodel = B_card_classes.name_to_inst_dict['Remodel']
workshop = B_card_classes.name_to_inst_dict['Workshop']
feast = B_card_classes.name_to_inst_dict['Feast']

actionData = pd.DataFrame()
buyData = pd.DataFrame()
stagedDecks = dict()

def return_action_cards(hand):
	action_list = []
	for card in hand:
		if card.grouping == 'Action':
			if (card is not monLen or copper in hand) and (((card is not remodel) and (card is not chapel)) or (len(hand) != 1)):
				action_list.append(card)
	return action_list

def printArray(arr):
	for card in arr:
		print card.name

def listToString(arr):
	return reduce(lambda x, y: x + ' ' + y.name, arr, "")[1:]

def listToStortString(arr):
	return reduce(lambda x, y: x + ' ' + str(y.key), arr, "")[1:]

def ActionsToBuys(row):
	return {'buys':row['buys'], 'treasure':row['treasure'], 'ohand':row['startHand'], 'hand':row['EndHand']}

def possibleBuys(treasure,buys=1,cap=8,keyCap=100):
	if buys == 0:
		return

	buysList = reduce(lambda x, y: x+[y] if y.cost <= treasure and y.cost <= cap and y.key <= keyCap else x, allCardInst, [])
	
	if buys == 1:
		return [[]]+ [[i] for i in (buysList)]

	moreBuys = [possibleBuys(treasure-i.cost, buys-1, i.cost, i.key) for i in buysList]

	# print moreBuys
	# print len(buysList)
	out = []

	for i in range(len(buysList)):
		out = out + [[buysList[i]] + j for j in moreBuys[i]]

	return [[]] + out

# import time
# start_time = time.time()
# # for i in range(1000):
# for i in possibleBuys(7, 2, 5):
# 	print i
# print str(time.time() - start_time)

def playoutActions(Ohand, Odeck, rep=10):

	Oactions = return_action_cards(Ohand)
	
	if not Oactions:
		return None

	if chapel in (Ohand + Odeck):
		rep *= 10
	elif remodel in (Ohand + Odeck):
		rep *= 4

	data = []

	for i in range(rep):
		deck = list(Odeck)
		shuffle(deck)
		hand = list(Ohand)
		action_list = list(Oactions+Oactions)
		action_list.append(None)

		another = True

		actionsTaken = []
		actions = 1
		treasure = 0
		buys = 1
		aquire = []
		discard = []
		trash = []

		while another and actions > 0 and action_list:
			choose = choice(action_list)
			# print action_list
			# print choose
			if choose is None:
				another = False
			else:
				actions -= 1

				hand.remove(choose)
				discard = discard + [choose]

				if choose is monLen:
					hand.remove(copper)
					treasure+=3
					trash = trash + [copper]
					actionsTaken.append((choose,[copper]))
					
				elif choose is remodel:
					remod = choice(hand)
					aquire.append(remod.cost+2)
					# actionsTaken.append("R - " + remod.name)
					trash = trash + [remod]
					hand.remove(remod)
					actionsTaken.append((choose,[remod]))

				elif choose.name is workshop:
					aquire.append(4)
					actionsTaken.append((choose,None))

				elif choose is feast:
					aquire.append(5)
					discard.remove(choose)
					trash = trash + [choose]
					actionsTaken.append((choose,None))

				elif choose is chapel:
					r = choice([1,2,3,4])
					
					if r > len(hand):
						r = len(hand)
					
					actionsTaken.append((choose,[]))

					for i in range(r):
						c = choice(hand)
						a,b = actionsTaken[len(actionsTaken)-1]
						b.append(c)
						trash = trash + [c]
						hand.remove(c)



				else:
					actionsTaken.append((choose,None))


				treasure += choose.gain_treasure
				actions += choose.gain_actions
				buys += choose.gain_buys

				draw = choose.draw_cards
				if (len(deck) > draw):
					hand = hand + deck[:draw]
					deck = deck[draw:]
				else:
					hand = hand + deck
					deck = []

				hand = sorted(hand, key=lambda c: c.key)

				action_list = return_action_cards(hand)
			# End Else
		# End While
		# print "end of action "+str(treasure)+","+str(buys)+","+str(actions)+","+str(aquire)+","+str(len(hand))+","+str(actionsTaken)
		# printArray(hand)


		inHandTreasure = reduce(lambda x, y: x+y.treasure, hand, treasure)
		data.append({'taken':actionsTaken, 'treasure':inHandTreasure, 'buys':buys, 'aquire':aquire, 'actions':actions, 'startHand':Ohand, 'EndHand':hand, 'discarded':discard, 'trash':trash, 'deck':deck})
		# print data
		# actionData.append(data, ignore_index=True)

	# print data
	return data

def stringifyTaken(taken):
	return reduce(lambda x, (a,b): x+' '+a.name+('' if b is None else '(' + listToString(b) + ')'), taken, '')

def stringifyActions(row):
	return {'taken':stringifyTaken(row['taken']), 'treasure':row['treasure'], 'buys':row['buys'], 'aquire':row['aquire'], 'actions':row['actions'], 'startHand':listToString(row['startHand']), 'EndHand':listToString(row['EndHand']), 'discarded':listToString(row['discarded']), 'trash':listToString(row['trash']), 'deck':listToString(row['deck'])}

def playoutTurn(Odeck, rep=10):

	if allDecks[listToStortString(Odeck)]['done']:
		return None, None

	allDecks[listToStortString(Odeck)]['done'] = True

	actionDataTurn = pd.DataFrame()
	buyDataTurn = pd.DataFrame()

	for i in range(rep):
		deck = list(Odeck)

		#shuffle deck
		shuffle(deck)

		#draw hand
		hand = deck[:5]
		deck = deck[5:]

		hand = sorted(hand, key=lambda c: c.key)

		#action phase
		newData = playoutActions(hand, deck)

		if newData:
			actstr = map(stringifyActions, newData)
			actionDataTurn = actionDataTurn.append(actstr, ignore_index=True)
		#buy phase

			Bdata = map(ActionsToBuys, actstr)

			nextTurnDecks = []
			for i in newData:
				for k in [sorted(j+i['deck']+i['EndHand']+i['discarded'], key=lambda c: c.key) for j in possibleBuys(i['treasure'], i['buys'])]:
					key = listToStortString(k)
					if key not in allDecks:
						if key in stagedDecks:
							stagedDecks[key]['origin'].append(Odeck)
						else:
							stagedDecks[key]={'done':False, 'origin':[Odeck], 'deck':k}
							# print key
					else:
						allDecks[key]['origin'].append(Odeck)
			# print nextTurnDecks
			# print set(nextTurnDecks)

		else:
			Bdata = [{'buys':1, 'treasure':reduce(lambda x, y: x+y.treasure, hand, 0), 'hand':listToString(hand)}]
			deck = hand + deck
			for k in [sorted(deck + i, key= lambda c: c.key) for i in possibleBuys(Bdata[0]['treasure'])]:
				key = listToStortString(k)
				if key not in allDecks:
					if key in stagedDecks:
						stagedDecks[key]['origin'].append(Odeck)
					else:
						stagedDecks[key]={'done':False, 'origin':[Odeck], 'deck':k}
				else:
					allDecks[key]['origin'].append(Odeck)

			# print nextTurnDecks

		buyDataTurn = buyDataTurn.append(Bdata, ignore_index=True)



	# print actionDataTurn
	# print buyDataTurn
	return buyDataTurn, actionDataTurn


# print allCardInst

# initialHand = [chapel]
initialHand = [copper,copper,copper,copper,copper,copper,copper,estate,estate,estate]

allDecks = dict({listToStortString(initialHand):{'done':True, 'origin':[], 'deck':initialHand}})

# bdT, adT = playoutTurn(initialHand)
# actionData = actionData.append(adT, ignore_index=True)
# buyData = buyData.append(bdT, ignore_index=True)

# for key in allDecks:
# 	print listToString(allDecks[key]['deck'])
# print possibleBuys(7, 2, 5)

for initBuys in possibleBuys(7, 2, 5):
	if copper not in initBuys and estate not in initBuys and duchy not in initBuys and initBuys:
		# print initBuys
		rundeck = sorted(initialHand + initBuys, key=lambda x: x.key)
		allDecks[listToStortString(rundeck)] = {'done':False, 'origin':[initialHand], 'deck':rundeck}
		bdT, adT = playoutTurn(rundeck)
		actionData = actionData.append(adT, ignore_index=True)
		buyData = buyData.append(bdT, ignore_index=True)


# for i in range(0):

# 	for key in allDecks:
# 		if not allDecks[key]['done']:
# 			bdT, adT = playoutTurn(allDecks[key]['deck'])
# 			actionData = actionData.append(adT, ignore_index=True)
# 			buyData = buyData.append(bdT, ignore_index=True)

# 	for key in stagedDecks:
# 		allDecks[key] = stagedDecks[key]

# 	stagedDecks = dict()

actionData.to_csv('actionsData.csv')
buyData.to_csv('buysData.csv')
# print buyData
print actionData

# playoutTurn([copper,copper,copper,copper,copper,copper,copper,estate,estate,estate,smithy,lab])
# playoutTurn([copper,copper,estate,estate,estate,estate,estate,estate,estate,monLen])