import B_card_classes
import player_one_turn
from random import shuffle
from random import choice

import itertools

import numpy as np
import pandas as pd



copper = B_card_classes.name_to_inst_dict['Copper']
estate = B_card_classes.name_to_inst_dict['Estate']
duchy = B_card_classes.name_to_inst_dict['Duchy']
monLen = B_card_classes.name_to_inst_dict['Money Lender']
chapel = B_card_classes.name_to_inst_dict['Chapel']
remodel = B_card_classes.name_to_inst_dict['Remodel']
workshop = B_card_classes.name_to_inst_dict['Workshop']
feast = B_card_classes.name_to_inst_dict['Feast']


# actionData = pd.DataFrame(columns=['taken', 'treasure', 'buys', 'acquire', 'actions', 'startHand', 'EndHand'])



allCardInst = [B_card_classes.name_to_inst_dict[name] for name in B_card_classes.all_cards_in_play_list]

allCardInst = sorted(allCardInst, key=lambda c: c.cost)
for i in range(len(allCardInst)):
	allCardInst[i].key = i

allCardsConsidered = reduce(lambda x,y: x+[y] if y is not estate and y is not duchy and y is not copper else x, allCardInst, [])
allCardsConsidered2 = reduce(lambda x,y: x+[y] if y is not copper else x, allCardInst, [])

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

def listToString(arr):
	return reduce(lambda x, y: x + ' ' + y.name, arr, "")[1:]

def listToStortString(arr):
	return reduce(lambda x, y: x + ' ' + str(y.key), arr, "")[1:]

def ActionsToBuys(row):
	return {'buys':row['buys'], 'treasure':row['treasure'], 'ohand':row['startHand'], 'hand':row['EndHand']}


def possibleBuysGen(treasure,buys=1,cap=8,keyCap=100):
	if buys == 0:
		return


	buysList = reduce(lambda x, y: x+[y] if y.cost <= treasure and y.cost <= cap and y.key <= keyCap else x, allCardsConsidered, [])
	
	if buys == 1:
		return [[]]+ [[i] for i in (buysList)]

	moreBuys = (possibleBuysGen(treasure-i.cost, buys-1, i.cost, i.key) for i in buysList)

	# print moreBuys
	# print len(buysList)
	out = []

	i = 0
	for ele in moreBuys:
		out = out + [[buysList[i]] + j for j in ele]
		i+=1

	return [[]] + out

limitMon = 17
limitBuys = 4

pBuysList = list()
for i in range(limitBuys):
	pBuysList.append(list(range(limitMon)))
	for j in range(limitMon):
		pBuysList[i][j] = possibleBuysGen(j,i)

used = 0
def possibleBuys(treasure,buys=1):
	if treasure < limitMon and buys < limitBuys:
		global pBuysList
		return pBuysList[buys][treasure]

	global used
	used += 1

	return possibleBuysGen(treasure, buys)

def getPossibleAcquires(value):
	return reduce(lambda x,y: [y]+x if y.cost <= value else x, allCardsConsidered2, [])

def getPossibleAcquires2(arr):
	arr = sorted(arr, reverse=True)
	gen = itertools.product(*map(getPossibleAcquires, arr))

	for i in gen:
		keyCap = 100
		good = True
		for j in i:
			if j.key > keyCap:
				good = False
				break
			else:
				keyCap = j.key

		if good:
			yield list(i)


	# print arr



# for i in getPossibleAcquires2([2,4]):
# 	print i

# print 

# a = getPossibleAcquires2([2])
# print a
# for i in a:
# 	print i

# print
# b = possibleBuys(4, 2)

# for i in b:
# 	print i

# print

# c = map(lambda (x,y): x+y,itertools.product(getPossibleAcquires2([2]),b))
# print c
# for i in c:
# 	print listToString(i)
# c = map(lambda (x,y): x+y,itertools.product(map(list, itertools.product(map(getPossibleAcquires, [2]))), possibleBuys(4,2)))
# print c
# for i in c:
# 	print i

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
		acquire = []
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
					acquire.append(remod.cost+2)
					# actionsTaken.append("R - " + remod.name)
					trash = trash + [remod]
					hand.remove(remod)
					actionsTaken.append((choose,[remod]))

				elif choose.name is workshop:
					acquire.append(4)
					actionsTaken.append((choose,None))

				elif choose is feast:
					acquire.append(5)
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


		inHandTreasure = reduce(lambda x, y: x+y.treasure, hand, treasure)
		data.append({'taken':actionsTaken, 'treasure':inHandTreasure, 'buys':buys, 'acquire':acquire, 'actions':actions, 'startHand':Ohand, 'EndHand':hand, 'discarded':discard, 'trash':trash, 'deck':deck})

	return data

def stringifyTaken(taken):
	return reduce(lambda x, (a,b): x+' '+a.name+('' if b is None else '(' + listToString(b) + ')'), taken, '')

def stringifyActions(row):
	return {'taken':stringifyTaken(row['taken']), 'treasure':row['treasure'], 'buys':row['buys'], 'acquire':row['acquire'], 'actions':row['actions'], 'startHand':listToString(row['startHand']), 'EndHand':listToString(row['EndHand']), 'discarded':listToString(row['discarded']), 'trash':listToString(row['trash']), 'deck':listToString(row['deck'])}

def playoutTurn(Odeck, rep=10):

	if allDecks[listToStortString(Odeck)]['done']:
		return None, None

	allDecks[listToStortString(Odeck)]['done'] = True

	global actionColumns
	global buyColumns
	actionDataTurn = pd.DataFrame(columns=actionColumns)
	buyDataTurn = pd.DataFrame(columns=buyColumns)

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

		#buy phase
		if newData:
			actstr = map(stringifyActions, newData)
			actionDataTurn = actionDataTurn.append(actstr, ignore_index=True)

			Bdata = map(ActionsToBuys, actstr)

			nextTurnDecks = []


			for i in newData:

				buys = possibleBuys(i['treasure'], i['buys'])

				#Generates buys and gains list (possible copies created)
				#could use more generators
				# buysAndGains = map(lambda (x,y): x+y,itertools.product(*([map(list, itertools.product(*map(getPossibleAcquires, i['acquire'])))]+[buys])))

				buysAndGains = map(lambda (x,y): x+y,itertools.product(getPossibleAcquires2(i['acquire']),buys))

				for k in (sorted(j+i['deck']+i['EndHand']+i['discarded'], key=lambda c: c.key) for j in buysAndGains):
					key = listToStortString(k)

					if key not in allDecks:
						if key not in stagedDecks:
						# 	stagedDecks[key]['origin'].append(Odeck)
						# else:
							stagedDecks[key]={'done':False, 'deck':k}
							# print key
					# else:
					# 	allDecks[key]['origin'].append(Odeck)
			# print nextTurnDecks
			# print set(nextTurnDecks)

		else:
			Bdata = [{'buys':1, 'treasure':reduce(lambda x, y: x+y.treasure, hand, 0), 'hand':listToString(hand)}]
			deck = hand + deck
			for k in [sorted(deck + i, key= lambda c: c.key) for i in possibleBuys(Bdata[0]['treasure'])]:
				key = listToStortString(k)
				if key not in allDecks:
					if key not in stagedDecks:
					# 	stagedDecks[key]['origin'].append(Odeck)
					# else:
						stagedDecks[key]={'done':False, 'deck':k}
				# else:
				# 	allDecks[key]['origin'].append(Odeck)

			# print nextTurnDecks

		buyDataTurn = buyDataTurn.append(Bdata, ignore_index=True)

	# print actionDataTurn
	# print buyDataTurn
	with open('buysData.csv', 'a') as f:
		buyDataTurn.to_csv(f, header=False, index=False)

	with open('actionsData.csv', 'a') as f:
		actionDataTurn.to_csv(f, header=False, index=False)

	del buyDataTurn
	del actionDataTurn
	# return buyDataTurn, actionDataTurn


# exit()

actionColumns = ['taken', 'treasure', 'buys', 'acquire', 'actions', 'startHand', 'EndHand', 'discarded', 'trash', 'deck']
buyColumns = ['buys', 'treasure', 'ohand', 'hand']

holder = pd.DataFrame(columns=actionColumns)

with open('actionsData.csv', 'w') as f:
	holder.to_csv(f, index=False)

holder = pd.DataFrame(columns=buyColumns)

with open('buysData.csv', 'w') as f:
	holder.to_csv(f, index=False)

del holder

# stagedDecks = dict()
# bdT, adT = playoutTurn(initialHand)
# actionData = actionData.append(adT, ignore_index=True)
# buyData = buyData.append(bdT, ignore_index=True)

# print stagedDecks
# for key in allDecks:
# 	print listToString(allDecks[key]['deck'])
# print possibleBuys(7, 2, 5)

initialHand = [copper,copper,copper,copper,copper,copper,copper,estate,estate,estate]

allDecks = dict({listToStortString(initialHand):{'done':True, 'deck':initialHand}})


print 'turn ', str(3)
for initBuys in possibleBuysGen(7, 2, 5):
	if copper not in initBuys and estate not in initBuys and duchy not in initBuys and initBuys:
		# print initBuys
		rundeck = sorted(initialHand + initBuys, key=lambda x: x.key)
		allDecks[listToStortString(rundeck)] = {'done':False, 'deck':rundeck}
		playoutTurn(rundeck)
		# actionData = actionData.append(adT, ignore_index=True)
		# buyData = buyData.append(bdT, ignore_index=True)

for key in stagedDecks:
	allDecks[key] = stagedDecks[key]
print 'number of decks created:', len(stagedDecks)


numberMoreTurns = 0

for i in range(numberMoreTurns):
	print 'turn', str(i+4)
	stagedDecks = dict()

	for key in allDecks:
		if not allDecks[key]['done']:
			playoutTurn(allDecks[key]['deck'])
			# actionData = actionData.append(adT, ignore_index=True)
			# buyData = buyData.append(bdT, ignore_index=True)

	for key in stagedDecks:
		allDecks[key] = stagedDecks[key]
	print 'number of decks created:', len(stagedDecks)

	# actionData.to_csv('actionsData.csv')
	# buyData.to_csv('buysData.csv')

print "Generated",used,"more buys"
# for key in allDecks:
# 	print listToString(allDecks[key]['deck']), len(allDecks[key]['origin'])

# actionData.to_csv('actionsData.csv')
# buyData.to_csv('buysData.csv')
# print buyData
# print actionData

# playoutTurn([copper,copper,copper,copper,copper,copper,copper,estate,estate,estate,smithy,lab])
# playoutTurn([copper,copper,estate,estate,estate,estate,estate,estate,estate,monLen])