from __future__ import division
import C_card_classes
from random import shuffle
from random import choice

import itertools

import numpy as np
import pandas as pd

import time

lastTime = time.time()

#Run constants
numberMoreTurns = 1
actRep = 5
buyRep = 2
chapelBias = 5
remodelBias = 2


#used refrences

copper = C_card_classes.name_to_inst_dict['Copper']
estate = C_card_classes.name_to_inst_dict['Estate']
duchy = C_card_classes.name_to_inst_dict['Duchy']
monLen = C_card_classes.name_to_inst_dict['Money Lender']
chapel = C_card_classes.name_to_inst_dict['Chapel']
remodel = C_card_classes.name_to_inst_dict['Remodel']
workshop = C_card_classes.name_to_inst_dict['Workshop']
feast = C_card_classes.name_to_inst_dict['Feast']

allCardInst = C_card_classes.allCardInst
maxKey = C_card_classes.maxKey

allCardsConsidered = reduce(lambda x,y: x+[y] if y is not estate and y is not duchy and y is not copper else x, 
	allCardInst, [])
allCardsConsidered2 = reduce(lambda x,y: x+[y] if y is not copper else x, allCardInst, [])

actionData = pd.DataFrame()
buyData = pd.DataFrame()
stagedDecks = dict()


#Functions Begin

#stringfiying functions

#convert a list of cards into a string
def listToString(arr):
	return reduce(lambda x, y: x + ' ' + y.name, arr, "")[1:]

#convert a list into a string of their key numbers
#used for generating dictionary keys
def listToStortString(arr):
	return reduce(lambda x, y: x + ' ' + str(y.key), arr, "")[1:]


def cardsToKeys(cards):
	return map(lambda x: x.key, cards)

def stringifyTaken(taken):
	return reduce(lambda x, (a,b): x+' '+a.name+('' if b is None else '(' + listToString(b) + ')'), taken, '')

def stringifyActions(row):
	return {'taken':row['taken'], 'treasure':row['treasure'], 'buys':row['buys'], 
	'acquire':row['acquire'], 'actions':row['actions'], 'startHand':cardsToKeys(row['startHand']), 
	'EndHand':cardsToKeys(row['EndHand']), 'discarded':cardsToKeys(row['discarded']), 
	'trash':cardsToKeys(row['trash']), 'deck':cardsToKeys(row['deck'])}

def ActionsToBuys(row):
	global Turn
	return {'buys':row['buys'], 'treasure':row['treasure'], 'ohand':row['startHand'], 'hand':row['EndHand'],
	'deck':sorted(row['deck']+row['discarded']+row['EndHand']+row['trash']), 
	'endDeck':sorted(row['deck']+row['discarded']+row['EndHand']), 'turn':Turn}


#Possibility functions

#Get list of possible to use actions from set of cards
def return_action_cards(hand):
	action_list = []
	for card in hand:
		if card.isAction:
			if (card is not monLen or copper in hand) and (((card is not remodel) and (card is not chapel)) or (len(hand) != 1)):
				action_list.append(card)
	return action_list

#generate list of possible buys
#will create a list of all possible purchases (no repeats)
def possibleBuysGen(treasure,buys=1,cap=8,keyCap=maxKey):
	if buys == 0:
		return

	buysList = reduce(lambda x, y: x+[y] if y.cost <= treasure and y.cost <= cap and y.key <= keyCap else x, 
		allCardsConsidered, [])
	
	if buys == 1:
		return [[]]+ [[i] for i in (buysList)]

	moreBuys = (possibleBuysGen(treasure-i.cost, buys-1, i.cost, i.key) for i in buysList)

	out = []

	i = 0
	for ele in moreBuys:
		out = out + [[buysList[i]] + j for j in ele]
		i+=1

	return [[]] + out

#generate matrix of possible buys
limitMon = 17
limitBuys = 4

pBuysList = list()
for i in range(limitBuys):
	pBuysList.append(list(range(limitMon)))
	for j in range(limitMon):
		pBuysList[i][j] = possibleBuysGen(j,i)

#look up for possible buys
used = 0
def possibleBuys(treasure,buys=1):
	if treasure < limitMon and buys < limitBuys:
		global pBuysList
		return pBuysList[buys][treasure]

	global used
	used += 1

	return possibleBuysGen(treasure, buys)

#get a list of possible 'gains' at or below value
def getPossibleAcquires(value):
	return reduce(lambda x,y: [y]+x if y.cost <= value else x, allCardsConsidered2, [])

#returns a generator of all possible 'gains' in 
def getPossibleAcquires2(arr):
	arr = sorted(arr, reverse=True)
	gen = itertools.product(*map(getPossibleAcquires, arr))

	global maxKey
	for i in gen:
		keyCap = maxKey
		good = True
		for j in i:
			if j.key > keyCap:
				good = False
				break
			else:
				keyCap = j.key

		if good:
			yield list(i)

#play actions from hand 'rep' times.
def playoutActions(Ohand, Odeck, rep=actRep):

	Oactions = return_action_cards(Ohand)
	
	if not Oactions:
		return None

	if chapel in (Ohand + Odeck):
		global chapelBias
		rep *= chapelBias
	elif remodel in (Ohand + Odeck):
		global remodelBias
		rep *= remodelBias

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
					actionsTaken.append((choose,cardsToKeys([copper])))
					
				elif choose.name is workshop:
					acquire.append(4)
					actionsTaken.append((choose.key,None))

				elif choose is feast:
					acquire.append(5)
					discard.remove(choose)
					trash = trash + [choose]
					actionsTaken.append((choose.key,None))

				elif choose is remodel:
					remod = choice(hand)
					acquire.append(remod.cost+2)
					# actionsTaken.append("R - " + remod.name)
					trash = trash + [remod]
					hand.remove(remod)
					actionsTaken.append((choose.key,cardsToKeys([remod])))

				elif choose is chapel:
					r = choice([1,2,3,4])
					
					if r > len(hand):
						r = len(hand)
					
					actionsTaken.append((choose.key,[]))

					for i in range(r):
						c = choice(hand)
						a,b = actionsTaken[len(actionsTaken)-1]
						b.append(c.key)
						trash = trash + [c]
						hand.remove(c)



				else:
					actionsTaken.append((choose.key,None))


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
		data.append({'taken':actionsTaken, 'treasure':inHandTreasure, 
			'buys':buys, 'acquire':acquire, 'actions':actions, 'startHand':Ohand, 
			'EndHand':hand, 'discarded':discard, 'trash':trash, 'deck':deck})

	return data

def getPossibleCombinations(cards, lower, upper=None):
	if upper is None:
		upper = lower+1

	l = set()
	for j in range(lower,upper):
		for i in itertools.combinations(cards, j):
			l.add(i)

	return map(list, l)

def getPossibleCombinationsAndProb(cards, lower):

	l = dict()
	num = 0

	for i in itertools.combinations(cards, lower):
		num += 1

		if i in l:
			l[i] += 1
		else:
			l[i] = 1

	print num
	for i in l:
		yield list(i), l[i]/num
	# return map(list, l)

# initialHand = [copper,copper,copper,copper,copper,copper,copper,estate,estate,estate]

# for n,p in getPossibleCombinationsAndProb(initialHand,1):
# 	print listToString(n), p

def treasInHand(hand):
	return reduce(lambda x,y: x+y.treasure, hand, 0)

def playoutActions2(Ohand, Odeck, actions=1, buys=1,treasure=0):
	if actions == 0:
		return None

	Oactions = set(return_action_cards(Ohand))

	if not Oactions:
		return None

	data = []

	for action in Oactions:
		if action is None:
			data.append({'taken':[], 'treasure':treasInHand(Ohand), 'buys':buys, 'acquire':[], 
				'actions':actions, 'startHand':Ohand, 'EndHand':Ohand, 'discarded':[], 'trash':[], 'deck':Odeck})
		elif action.draw_cards > 0:
			for k, p in getPossibleCombinationsAndProb(sorted(Odeck, lambda x: x.key), action.draw_cards):
				deck = list(Odeck)
				for i in k:
					deck.remove(i)
				playoutActions2((Ohand + k), deck, actions + action.gain_actions - 1, 
					buys + action.gain_buys, treasure + action.gain_treasure)
			pass
		elif action is chapel:
			pass
		elif action is remodel:
			pass
		else:
			playoutActions2(list(Ohand).remove(action), list(Odeck), actions + action.gain_actions - 1, 
				buys + action.gain_buys, treasure + action.gain_treasure)




# exit()


def incrementDest(myKey, key):
	global allDecks
	dest = allDecks[myKey]['dest']
	
	if key in dest:
		dest[key] += 1
	else:
		dest[key] = 1


#play one turn of a deck 'rep' times. Shuffles before each play 
def playoutTurn(Odeck, rep=buyRep):

	myKey = listToStortString(Odeck)
	if allDecks[myKey]['done']:
		return None, None

	allDecks[myKey]['done'] = True
	allDecks[myKey]['dest'] = dict()

	global actionColumns
	global buyColumns
	actionDataTurn = pd.DataFrame(columns=actionColumns)
	buyDataTurn = pd.DataFrame(columns=buyColumns)

	global deckKeys
	global stagedDecks
	global Turn

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

					incrementDest(myKey, key)
						

					if key not in allDecks:
						if key in stagedDecks:
							stagedDecks[key]['origin'].append(Odeck)
						else:
							stagedDecks[key]={'done':False, 'deck':k,'origin':[Odeck]}
							deckKeys.append(key)
							# print key
					else:
						allDecks[key]['origin'].append(Odeck)
			# print nextTurnDecks
			# print set(nextTurnDecks)

		else:
			Bdata = [{'buys':1, 'treasure':reduce(lambda x, y: x+y.treasure, hand, 0), 
			'hand':cardsToKeys(hand), 'deck':cardsToKeys(Odeck), 'endDeck':cardsToKeys(Odeck), 'turn':Turn}]
			deck = hand + deck
			for k in (sorted(deck + i, key= lambda c: c.key) for i in possibleBuys(Bdata[0]['treasure'])):
				key = listToStortString(k)
				incrementDest(myKey, key)
					

				if key not in allDecks:
					if key in stagedDecks:
						stagedDecks[key]['origin'].append(Odeck)
					else:
						stagedDecks[key]={'done':False, 'deck':k,'origin':[Odeck]}
						deckKeys.append(key)
				else:
					allDecks[key]['origin'].append(Odeck)

			# print nextTurnDecks

		buyDataTurn = buyDataTurn.append(Bdata, ignore_index=True)

	# print actionDataTurn
	# print buyDataTurn
	with open('buysData.csv', 'a') as f:
		buyDataTurn.to_csv(f, header=False, index=False)

	with open('actionsData.csv', 'a') as f:
		actionDataTurn.to_csv(f, header=False, index=False)

	# global printed
	# global printing
	# if printing and printed > 0:
	# 	printed -= 1
	# 	print len(deckKeys), len(set(deckKeys))

	with open('deckData.csv', 'a') as f:
		pd.DataFrame(columns=deckKeys).append(pd.Series(allDecks[myKey]['dest'], name=myKey),0).to_csv(f, header=False, index=False)

	del buyDataTurn
	del actionDataTurn
	# return buyDataTurn, actionDataTurn

printed = 5
printing = False
# exit()

actionColumns = ['taken', 'treasure', 'buys', 'acquire', 'actions', 'startHand', 
								 'EndHand', 'discarded', 'trash', 'deck']
buyColumns = ['turn','buys', 'treasure', 'ohand', 'hand', 'deck', 'endDeck']

holder = pd.DataFrame(columns=actionColumns)

with open('actionsData.csv', 'w') as f:
	holder.to_csv(f, index=False)

holder = pd.DataFrame(columns=buyColumns)

with open('buysData.csv', 'w') as f:
	holder.to_csv(f, index=False)

open('deckData.csv', 'w').close()

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
deckKeys = [listToStortString(initialHand)]

allDecks = dict({listToStortString(initialHand):{'done':True, 'deck':initialHand,'origin':[], 'dest':dict()}})



print 'turn ', str(3)," - Seconds:",time.time() - lastTime
lastTime = time.time()

Turn = 3

for initBuys in possibleBuysGen(7, 2, 5):
	if copper not in initBuys and estate not in initBuys and duchy not in initBuys and initBuys:
		# print initBuys
		rundeck = sorted(initialHand + initBuys, key=lambda x: x.key)
		allDecks[listToStortString(rundeck)] = {'done':False, 'deck':rundeck,'origin':[initialHand]}
		playoutTurn(rundeck)
		# actionData = actionData.append(adT, ignore_index=True)
		# buyData = buyData.append(bdT, ignore_index=True)

for key in stagedDecks:
	allDecks[key] = stagedDecks[key]
print 'number of decks created:', len(stagedDecks)

Turn += 1

printing = True

for i in range(numberMoreTurns):
	print 'turn', str(Turn)," - Seconds:",time.time() - lastTime
	lastTime = time.time()
	
	stagedDecks = dict()

	for key in allDecks:
		if not allDecks[key]['done']:
			playoutTurn(allDecks[key]['deck'])
			# actionData = actionData.append(adT, ignore_index=True)
			# buyData = buyData.append(bdT, ignore_index=True)

	Turn +=1

	for key in stagedDecks:
		allDecks[key] = stagedDecks[key]
	print 'number of decks created:', len(stagedDecks)

print "Seconds:",time.time() - lastTime
print "Generated",used,"more buys"

decks = pd.DataFrame(columns=deckKeys)

with open('deckData.csv', 'a') as f:
	decks.to_csv(f)


# decksColumns = ['key','origin','dest','done']
# decks = pd.DataFrame(columns=decksColumns)

# x = 0
# y = 0

# printed = False
# for k in allDecks:
# 	if allDecks[k]['done']:
# 		if not printed:
# 			printed = True
# 			print pd.Series(allDecks[k]['dest'], name=k)
# 		decks = decks.append(pd.Series(allDecks[k]['dest'], name=k),0)
		# for k in dest:
		# 	num += dest[k]
		# 	num2 += 1
		# print num,'across',num2,'-',k

# print decks.shape
# decks.to_csv('decksData.csv')
# print x, y
