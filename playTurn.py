import B_card_classes
import player_one_turn
from random import shuffle
from random import choice

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

def playoutActions(Ohand, Odeck, rep=10):

	Oactions = return_action_cards(Ohand)
	
	if not Oactions:
		return

	if chapel in (Ohand + Odeck):
		rep *= 10
	elif remodel in (Ohand + Odeck):
		rep *= 4

	for i in range(rep):
		deck = list(Odeck)
		shuffle(deck)
		hand = list(Ohand)
		action_list = list(Oactions)
		action_list.append(None)

		another = True

		actionsTaken = []
		actions = 1
		treasure = 0
		buys = 1
		aquire = []

		while actions > 0 and action_list and another:
			choose = choice(action_list)
			# print action_list
			# print choose
			if choose is None:
				another = False
			else:
				actionsTaken.append(choose.name)
				actions -= 1

				hand.remove(choose)

				if choose.name is "Money Lender":
					hand.remove(copper)
					treasure+=3
					
				if choose.name is "Remodel":
					remod = choice(hand)
					aquire.append(remod.cost+2)
					actionsTaken.append("R - " + remod.name)

				if choose.name is "Workshop":
					aquire.append(4)

				if choose.name is "Feast":
					aquire.append(5)

				if choose.name is "Chapel":
					r = choice([1,2,3,4])
					
					if r > len(hand):
						r = len(hand)
					
					for i in range(r):
						c = choose(hand)
						actionsTaken.append("C - " + c.name)
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

				action_list = return_action_cards(hand)
			# End Else
		# End While
		print "end of action "+str(treasure)+","+str(buys)+","+str(actions)+","+str(aquire)+","+str(len(hand))+","+str(actionsTaken)
		printArray(hand)



	# return

def playoutTurn(Odeck, rep=10):

	for i in range(rep):
		deck = list(Odeck)
		buys = 1

		#shuffle deck
		shuffle(deck)

		#draw hand
		hand = deck[:5]
		deck = deck[5:]

		print "hand"
		printArray(hand)
		print "deck"
		printArray(deck)

		#action phase
		playoutActions(hand, deck)

		#buy phase

copper = B_card_classes.Copper()
estate = B_card_classes.Estate()
smithy = B_card_classes.Smithy()
village = B_card_classes.Village()
monLen = B_card_classes.Moneylender()
chapel = B_card_classes.Chapel()
remodel = B_card_classes.Remodel()
playoutTurn([copper,copper,copper,copper,copper,copper,copper,estate,estate,estate, remodel])
# playoutTurn([copper,copper,estate,estate,estate,estate,estate,estate,estate,monLen])