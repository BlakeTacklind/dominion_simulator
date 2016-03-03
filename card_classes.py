class Card(object):
	def __init__(self, name, cost=0, treasure=0, grouping='', draw_cards=0, gain_treasure=0, gain_actions=0,gain_buys=0,victory=0,isVictory=False,isTreasure=False,isAction=False):
		self.name=name
		self.cost=cost
		self.treasure=treasure
		self.grouping=grouping
		self.draw_cards=draw_cards
		self.gain_actions=gain_actions
		self.gain_buys=gain_buys
		self.gain_treasure=gain_treasure
		self.victory=victory
		self.isVictory=isVictory
		self.isTreasure=isTreasure
		self.isAction=isAction
		self.key=None

class Copper(Card):
	def __init__(self):
		super(Copper, self).__init__("Copper",grouping="Treasure",treasure=1,isTreasure=True)


class Estate(Card):
	def __init__(self):
		super(Estate, self).__init__("Estate",2,grouping="Victory",victory=1,isVictory=True)


class Silver(Card):
	def __init__(self):
		super(Silver, self).__init__("Silver",3,grouping="Treasure",treasure=2,isTreasure=True)


class Gold(Card):
	def __init__(self):
		super(Gold, self).__init__("Gold",6,grouping="Treasure",treasure=3,isTreasure=True)


class Province(Card):
	def __init__(self):
		super(Province, self).__init__("Province",8,grouping="Victory",victory=6,isVictory=True)


class Duchy(Card):
	def __init__(self):
		super(Duchy, self).__init__("Duchy",5,grouping="Victory",victory=3,isVictory=True)


class Smithy(Card):
	def __init__(self):
		super(Smithy, self).__init__("Smithy",4,grouping="Action",draw_cards=3,isAction=True)

	def execute_action(self, turn, none):
		standard_action_execute(turn,self)


class Village(Card):
	def __init__(self):
		super(Village, self).__init__("Village",3,grouping="Action",draw_cards=1,gain_actions=2,isAction=True)

	def execute_action(self, turn, none):
		standard_action_execute(turn,self)


class Laboratory(Card):
	def __init__(self):
		super(Laboratory, self).__init__("Laboratory",5,grouping="Action",draw_cards=2,gain_actions=1,isAction=True)

	def execute_action(self, turn, none):
		standard_action_execute(turn,self)


class Market(Card):
	def __init__(self):
		super(Market, self).__init__("Market",5,grouping="Action",draw_cards=1,gain_actions=1,gain_buys=1,gain_treasure=1,isAction=True)

	def execute_action(self, turn, none):
		standard_action_execute(turn,self)


class Moneylender(Card):
	def __init__(self):
		super(Moneylender, self).__init__("Money Lender",4,grouping="Action",isAction=True)

	def execute_action(self, turn, none):
		standard_action_execute(turn,self)
		copper_in_hand = turn.player.check_for_card_type(turn.player.hand, 'Copper')
		if copper_in_hand > 0:
			turn.player.trash_card(turn.player.hand, 'Copper')
			turn.treasure += 3


class Woodcutter(Card):
	def __init__(self):
		super(Woodcutter, self).__init__("Woodcutter",3,grouping="Action",gain_buys=1,gain_treasure=2,isAction=True)

	def execute_action(self, turn, none):
		standard_action_execute(turn,self)


class Festival(Card):
	def __init__(self):
		super(Festival, self).__init__("Festival",5,grouping="Action",gain_actions=2,gain_buys=1,gain_treasure=2,isAction=True)

	def execute_action(self, turn, none):
		standard_action_execute(turn,self)


class Remodel(Card):
	def __init__(self):
		super(Remodel, self).__init__("Remodel",4,grouping="Action",isAction=True)

	def execute_action(self, turn, trash_gain):
		standard_action_execute(turn,self)
		trash_card = trash_gain[0]
		gain_card = trash_gain[1]
		trash_card_inst = name_to_inst_dict[trash_card]
		gain_card_inst = name_to_inst_dict[gain_card]
		if trash_card_inst.cost +2 >= gain_card_inst.cost:
			turn.player.trash_card(turn.player.hand,trash_card)
			turn.player.gain_card(gain_card_inst,trash_card_inst.cost + 2)



class Workshop(Card):
	def __init__(self):
		super(Workshop, self).__init__("Workshop",3,grouping="Action",isAction=True)

	def execute_action(self, turn, gain_card):
		standard_action_execute(turn,self)
		gain_card = name_to_inst_dict[gain_card]
		if gain_card.cost <= 4:
			turn.player.gain_card(gain_card,4)


class Feast(Card):
	def __init__(self):
		super(Feast, self).__init__("Feast",4,grouping="Action",isAction=True)

	def execute_action(self,turn, gain_card):
		standard_action_execute(turn,self)
		gain_card = name_to_inst_dict[gain_card]
		if gain_card.cost <= 5:
			turn.player.gain_card(gain_card,5)
			turn.player.trash_card(turn.player.played_actions,'Feast')

class Chapel(Card):
	def __init__(self):
		super(Chapel, self).__init__("Chapel",2,grouping="Action",isAction=True)


	def execute_action(self,turn, cards_to_trash):
		standard_action_execute(turn,self)
		if len(cards_to_trash) <= 4:
			for x in range(0,len(cards_to_trash)):
			  # card_to_trash = name_to_inst_dict[cards_to_trash[x]]
				turn.player.trash_card(turn.player.hand,cards_to_trash[x])


def standard_action_execute(turn,action):
	turn.player.draw_cards(action.draw_cards)
	turn.actions_remaining += (action.gain_actions - 1)
	turn.buys_remaining += (action.gain_buys)
	turn.treasure += (action.gain_treasure)

kingdom_cards = ['Village','Chapel','Workshop','Smithy','Money Lender', 'Remodel', 'Feast','Market', 'Festival', 'Laboratory']
standard_supply = ['Copper', 'Silver', 'Gold', 'Estate', 'Duchy', 'Province']
all_cards_in_play_list = kingdom_cards + standard_supply
name_to_inst_dict = {'Copper':Copper(), 'Duchy':Duchy(), 'Estate':Estate(), 'Gold':Gold(), 'Silver':Silver(),
					 'Province':Province(), 'Laboratory':Laboratory(),'Market':Market(), 'Smithy':Smithy(),
					 'Village':Village(),'Money Lender':Moneylender(), 'Woodcutter': Woodcutter(),
					 'Festival':Festival(), 'Remodel':Remodel(), 'Workshop':Workshop(), 'Feast':Feast(),
					 'Chapel' : Chapel()}
bank = {'Copper':40, 'Estate':8, 'Silver':40, 'Duchy':8, 'Gold':25, 'Province':8, 'Money Lender':10}
trash = {'Copper':0, 'Estate':0, 'Silver':0, 'Village':0, 'Smithy':0, 'Duchy':0, 'Gold':0, 'Province':0}

allCardInst = sorted([name_to_inst_dict[name] for name in all_cards_in_play_list], key=lambda c: (c.cost,c.name))

for i in range(len(allCardInst)):
	allCardInst[i].key = i

maxKey = len(allCardInst) - 1
