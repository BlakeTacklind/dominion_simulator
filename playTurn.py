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

def return_action_cards(hand):
	action_list = []
	for card in hand:
		if card.grouping == 'Action':
			if card is not monLen or copper in hand:
				action_list.append(card)
	return action_list

def printArray(arr):
	for card in arr:
		print card.name

def listToString(arr):
	return reduce(lambda x, y: x + ' ' + y.name, arr, "")

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
	# actionData = pd.DataFrame()

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
				actionsTaken.append(choose.name)
				actions -= 1

				hand.remove(choose)
				discard = discard + [choose]

				if choose is monLen:
					hand.remove(copper)
					treasure+=3
					discard.remove(choose)
					trash = trash + [copper]
					
				if choose.name is "Remodel":
					remod = choice(hand)
					aquire.append(remod.cost+2)
					actionsTaken.append("R - " + remod.name)
					trash = trash + [remod]
					hand.remove(remod)

				if choose.name is "Workshop":
					aquire.append(4)

				if choose.name is "Feast":
					aquire.append(5)
					discard.remove(choose)
					trash = trash + [choose]

				if choose.name is "Chapel":
					r = choice([1,2,3,4])
					
					if r > len(hand):
						r = len(hand)
					
					for i in range(r):
						c = choice(hand)
						actionsTaken.append("C - " + c.name)
						trash = trash + [c]
						hand.remove(c)

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

				hand = sorted(hand, key=lambda c: c.name)

				action_list = return_action_cards(hand)
			# End Else
		# End While
		# print "end of action "+str(treasure)+","+str(buys)+","+str(actions)+","+str(aquire)+","+str(len(hand))+","+str(actionsTaken)
		# printArray(hand)


		inHandTreasure = reduce(lambda x, y: x+y.treasure, hand, treasure)
		data.append({'taken':actionsTaken, 'treasure':inHandTreasure, 'buys':buys, 'aquire':aquire, 'actions':actions, 'startHand':listToString(Ohand), 'EndHand':listToString(hand), 'discarded':listToString(discard), 'trash':listToString(trash)})
		# print data
		# actionData.append(data, ignore_index=True)

	# print data
	return data

def playoutTurn(Odeck, rep=10):

	actionDataTurn = pd.DataFrame()
	buyDataTurn = pd.DataFrame()

	for i in range(rep):
		deck = list(Odeck)

		#shuffle deck
		shuffle(deck)

		#draw hand
		hand = deck[:5]
		deck = deck[5:]

		hand = sorted(hand, key=lambda c: c.name)

		#action phase
		newData = playoutActions(hand, deck)
		actionDataTurn = actionDataTurn.append(newData, ignore_index=True)

		#buy phase
		if newData is None:
			Bdata = [{'buys':1, 'treasure':reduce(lambda x, y: x+y.treasure, hand, 0), 'hand':listToString(hand)}]
		else:
			Bdata = map(ActionsToBuys, newData)
			# print Bdata

		buyDataTurn = buyDataTurn.append(Bdata, ignore_index=True)


	# print actionDataTurn
	# print buyDataTurn
	return buyDataTurn, actionDataTurn


# print allCardInst


copper = B_card_classes.name_to_inst_dict['Copper']
estate = B_card_classes.name_to_inst_dict['Estate']
duchy = B_card_classes.name_to_inst_dict['Duchy']
monLen = B_card_classes.name_to_inst_dict['Money Lender']
chapel = B_card_classes.name_to_inst_dict['Chapel']
remodel = B_card_classes.name_to_inst_dict['Remodel']

actionData = pd.DataFrame()
buyData = pd.DataFrame()
initialHand = [copper,copper,copper,copper,copper,copper,copper,estate,estate,estate]

# print possibleBuys(7, 2, 5)
for initBuys in possibleBuys(7, 2, 5):
	if copper not in initBuys and estate not in initBuys and duchy not in initBuys and initBuys:
		print initBuys
		bdT, adT = playoutTurn(initialHand + initBuys)
		actionData = actionData.append(adT, ignore_index=True)
		buyData = buyData.append(bdT, ignore_index=True)

actionData.to_csv('actionsData.csv')
buyData.to_csv('buysData.csv')
print actionData

# playoutTurn([copper,copper,copper,copper,copper,copper,copper,estate,estate,estate,smithy,lab])
# playoutTurn([copper,copper,estate,estate,estate,estate,estate,estate,estate,monLen])