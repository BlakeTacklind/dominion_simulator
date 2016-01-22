from __future__ import division
import B_card_classes
name_to_inst_dict = B_card_classes.name_to_inst_dict

f = open("output.csv", "w+")
#player number
f.write("player,")

#turn
f.write("turn,")

#type
f.write("type,")

#treasure
f.write("tresure,")

#extra
f.write("extra,")

#turns
f.write("turns,")

#p1Points
f.write("p1Points,")

#p2Points
f.write("p2Points,")

#hand
f.write("hand,")

#deck
f.write("deck,")

#discard
f.write("discard")

#current deck stats

f.write(",ds")
f.write(",dsf")

f.write(",gpc")
f.write(",gpcf")

f.write(",apc")
f.write(",apcf")

f.write(",ea")
f.write(",eaf")

f.write(",eb")
f.write(",ebf")

f.write(",dpc")
f.write(",dpcf")

f.write(",vc")
f.write(",vcf")

f.write(",vp")

#bank stats
for i in B_card_classes.kingdom_cards:
	f.write(','+i)

for i in B_card_classes.standard_supply:
	f.write(','+i)

#buy stats
for i in B_card_classes.kingdom_cards:
	f.write(','+i)

for i in B_card_classes.standard_supply:
	f.write(','+i)

f.write(',None')

#actions played
actionsCards = []
for i in range(0, len(B_card_classes.kingdom_cards)):
	if name_to_inst_dict[B_card_classes.kingdom_cards[i]].grouping is "Action":
		actionsCards.append(B_card_classes.kingdom_cards[i])

for i in actionsCards:
	f.write(','+i)

f.write('\n')


buysFile = open("output-buys.csv", "w+")
buysFile.write("player,")
buysFile.write("turn,")
buysFile.write("treasure,")
buysFile.write("turns,")
buysFile.write("p1Points,")
buysFile.write("p2Points")

#current deck stats

buysFile.write(",ds")
buysFile.write(",dsf")

buysFile.write(",gpc")
buysFile.write(",gpcf")

buysFile.write(",apc")
buysFile.write(",apcf")

buysFile.write(",ea")
buysFile.write(",eaf")

buysFile.write(",eb")
buysFile.write(",ebf")

buysFile.write(",dpc")
buysFile.write(",dpcf")

buysFile.write(",vc")
buysFile.write(",vcf")

buysFile.write(",vp")

#bank stats
for i in B_card_classes.kingdom_cards:
	buysFile.write(','+i)

for i in B_card_classes.standard_supply:
	buysFile.write(','+i)

#buy stats
for i in B_card_classes.kingdom_cards:
	buysFile.write(','+i)

for i in B_card_classes.standard_supply:
	buysFile.write(','+i)

buysFile.write(',None')



def deckstats(turnData):
	s = ""

	goldInDeck = sum([name_to_inst_dict[i].treasure for i in turnData["deck"]])
	goldInDeckFull = sum([name_to_inst_dict[i].treasure for i in turnData["hand"]+turnData["discard"]]) + goldInDeck
	extraActionsInDeck = sum([name_to_inst_dict[i].gain_actions for i in turnData["deck"]])
	extraActionsInDeckFull = sum([name_to_inst_dict[i].gain_actions for i in turnData["hand"]+turnData["discard"]]) + extraActionsInDeck
	extraBuysInDeck = sum([name_to_inst_dict[i].gain_buys for i in turnData["deck"]])
	extraBuysInDeckFull = sum([name_to_inst_dict[i].gain_buys for i in turnData["hand"]+turnData["discard"]]) + extraBuysInDeck
	drawInDeck = sum([name_to_inst_dict[i].draw_cards for i in turnData["deck"]])
	drawInDeckFull = sum([name_to_inst_dict[i].draw_cards for i in turnData["hand"]+turnData["discard"]]) + drawInDeck
	victoryCardsInDeck = sum([name_to_inst_dict[i].grouping is 'Victory' for i in turnData["deck"]])
	victoryCardsInDeckFull = sum([name_to_inst_dict[i].grouping is 'Victory' for i in turnData["hand"]+turnData["discard"]])+victoryCardsInDeck
	actionsCardsInDeck = sum([name_to_inst_dict[i].grouping is 'Action' for i in turnData["deck"]])
	actionsCardsInDeckFull = sum([name_to_inst_dict[i].grouping is 'Action' for i in turnData["hand"]+turnData["discard"]])+actionsCardsInDeck
	victoryPoints = sum([name_to_inst_dict[i].victory for i in turnData["hand"]+turnData["discard"]+turnData["deck"]])

	deckSize = len(turnData["deck"])
	deckSizeFull = deckSize+len(turnData["hand"])+len(turnData["discard"])

	s+=str(deckSize)
	s+=','
	s+=str(deckSizeFull)
	s+=','

	if deckSize is not 0:
		s+=str(goldInDeck/deckSize)
		s+=','
	else:
		s+='0,'
	s+=str(goldInDeckFull/deckSizeFull)
	s+=','

	if deckSize is not 0:
		s+=str(actionsCardsInDeck/deckSize)
		s+=','
	else:
		s+='0,'
	s+=str(actionsCardsInDeckFull/deckSizeFull)
	s+=','

	if deckSize is not 0:
		s+=str(extraActionsInDeck/deckSize)
		s+=','
	else:
		s+='0,'
	s+=str(extraActionsInDeckFull/deckSizeFull)
	s+=','

	if deckSize is not 0:
		s+=str(extraBuysInDeck/deckSize)
		s+=','
	else:
		s+='0,'
	s+=str(extraBuysInDeckFull/deckSizeFull)
	s+=','

	if deckSize is not 0:
		s+=str(drawInDeck/deckSize)
		s+=','
	else:
		s+='0,'
	s+=str(drawInDeckFull/deckSizeFull)
	s+=','

	if deckSize is not 0:
		s+=str(victoryCardsInDeck/deckSize)
		s+=','
	else:
		s+='0,'
	s+=str(victoryCardsInDeckFull/deckSizeFull)
	s+=','

	s+=str(victoryPoints)

	return s

def arr2Str(arr):
	s=""
	for i in arr:
		s+=i
		s+=' '

	return s

def bankStats(turnData):
	s=""

	#bank stats
	for i in B_card_classes.kingdom_cards:
		s+=str(turnData['bank'][i])
		s+=','

	for i in B_card_classes.standard_supply:
		s += str(turnData['bank'][i])
		s+=','

	return s

def buyStats(buy):
	s=""

	for i in B_card_classes.kingdom_cards:
		if i is buy:
			s+="1,"
		else:
			s+="0,"

	for i in B_card_classes.standard_supply:
		if i is buy:
			s+="1,"
		else:
			s+="0,"

	if "None" is buy:
		s+="1"
	else:
		s+="0"

	return s

def actionStats(action):
	s=""

	for i in actionsCards:
		if i is action:
			s+=",1"
		else:
			s+=",0"

	return s

def buyCSV(turnsData, game_result):
	s=""

	turns = (game_result.player_one_turns + game_result.player_two_turns) / 2

	#only consered with self range
	for i in range(0, len(turnsData),2):
		turnData = turnsData[i]

		#actions writer
		for a in turnData['actions']:
			if a['action'] is "Workshop" or a['action'] is "Feast":
				s+='\n'

				#player number
				s+=str(turnData['player'])
				s+=','

				#turn
				s+=str(i/2)
				s+=','

				#treasure
				if a['action'] is "Workshop":
					s+="4,"
				else:
					s+="5,"
				
				#turns
				s+=str(turns)
				s+=','

				#p1Points
				s+=str(game_result.player_one_points)
				s+=','

				#p2Points
				s+=str(game_result.player_two_points)
				s+=','

				#current deck stats
				s+=deckstats(turnData)
				s+=','

				#bank stats
				s+=bankStats(turnData)

				#buy stats
				s+=buyStats(a['strat'])


		#buys
		spent=0
		for buy in turnData['buys']['buys']:
			s+="\n"
			#player number
			s+=str(turnData['player'])
			s+=','

			#turn
			s+=str(i/2)
			s+=','

			#treasure
			s+=str(turnData['buys']['tres'] - spent)
			s+=','

			spent+=name_to_inst_dict[buy].cost

			#turns
			s+=str(turns)
			s+=','

			#p1Points
			s+=str(game_result.player_one_points)
			s+=','

			#p2Points
			s+=str(game_result.player_two_points)
			s+=','

			#current deck stats
			s+=deckstats(turnData)
			s+=','

			#bank stats
			s+=bankStats(turnData)

			#buy stats
			s+=buyStats(buy)

		if not turnData['buys']['buys']:
			s+="\n"
			#player number
			s+=str(turnData['player'])
			s+=','

			#turn
			s+=str(i/2)
			s+=','

			#treasure
			s+=str(turnData['buys']['tres'])
			s+=','

			#turns
			s+=str(turns)
			s+=','

			#p1Points
			s+=str(game_result.player_one_points)
			s+=','

			#p2Points
			s+=str(game_result.player_two_points)
			s+=','

			#current deck stats
			s+=deckstats(turnData)
			s+=','

			#bank stats
			s+=bankStats(turnData)

			#buy stats
			s+=buyStats("None")


	return s

def csvify(turnsData, game_result):
	s = ""

	turns = (game_result.player_one_turns + game_result.player_two_turns) / 2

	#only consered with self range
	for i in range(0, len(turnsData),2):
		turnData = turnsData[i]

		#player number
		s+=str(turnData['player'])
		s+=','

		#turn
		s+=str(i/2)
		s+=','

		#type
		s+='begin,'

		#treasure
		s+=','

		#extra
		s+=','

		#turns
		s+=str(turns)
		s+=','

		#p1Points
		s+=str(game_result.player_one_points)
		s+=','

		#p2Points
		s+=str(game_result.player_two_points)
		s+=','

		#hand
		s+=str(arr2Str(turnData['hand']))
		s+=','

		#deck
		s+=str(arr2Str(turnData['deck']))
		s+=','

		#discard
		s+=str(arr2Str(turnData['discard']))
		s+=','

		#current deck stats
		s+=deckstats(turnData)
		s+=','

		#bank stats
		s+=bankStats(turnData)

		#buy stats
		s+=buyStats(" ")
		s+=','

		#actions writer
		for a in turnData['actions']:
			s+='\n'

			#player number
			s+=str(turnData['player'])
			s+=','

			#turn
			s+=str(i/2)
			s+=','

			#type
			s+=a['action']
			s+=','

			#treasure
			if a['action'] is "Workshop":
				s+="4"
			elif a['action'] is "Feast":
				s+="5"
			
			s+=','

			#extra
			s+=str(a['strat'])
			s+=','

			#turns
			s+=str(turns)
			s+=','

			#p1Points
			s+=str(game_result.player_one_points)
			s+=','

			#p2Points
			s+=str(game_result.player_two_points)
			s+=','

			#hand
			s+=str(arr2Str(turnData['hand']))
			s+=','

			#deck
			s+=str(arr2Str(turnData['deck']))
			s+=','

			#discard
			s+=str(arr2Str(turnData['discard']))
			s+=','

			#current deck stats
			s+=deckstats(turnData)
			s+=','

			#bank stats
			s+=bankStats(turnData)

			#buy stats
			if a['action'] is "Workshop":
				s+=buyStats(a['strat'])
			elif a['action'] is "Feast":
				s+=buyStats(a['strat'])
			else:
				s+=buyStats(' ')

			# action stats
			s+=actionStats(a['action'])

		#buys
		spent=0
		for buy in turnData['buys']['buys']:
			s+="\n"
			#player number
			s+=str(turnData['player'])
			s+=','

			#turn
			s+=str(i/2)
			s+=','

			#type
			s+="buy,"

			#treasure
			s+=str(turnData['buys']['tres'] - spent)
			s+=','

			spent+=name_to_inst_dict[buy].cost

			#extra
			s+=buy
			s+=','

			#turns
			s+=str(turns)
			s+=','

			#p1Points
			s+=str(game_result.player_one_points)
			s+=','

			#p2Points
			s+=str(game_result.player_two_points)
			s+=','

			#hand
			s+=str(arr2Str(turnData['hand']))
			s+=','

			#deck
			s+=str(arr2Str(turnData['deck']))
			s+=','

			#discard
			s+=str(arr2Str(turnData['discard']))
			s+=','

			#current deck stats
			s+=deckstats(turnData)
			s+=','

			#bank stats
			s+=bankStats(turnData)

			#buy stats
			s+=buyStats(buy)

		s+="\n"
	return s

def closeFiles():
	global f
	f.close()
	buysFile.close()

def fileWrites(turnData, game_result):
	# if game_result.player_two_points >= game_result.player_one_points*(.9):
	global f
	global buysFile
	f.write(csvify(turnData, game_result))
	buysFile.write(buyCSV(turnData, game_result))
