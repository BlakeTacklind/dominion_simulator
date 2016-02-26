__author__ = 'stevenkerr'
import card_classes
# import learnedRandomStrategy as player_two_alg
import learnedRandomStrategy2 as player_two_alg
import player_one_alg
from random import shuffle
import pandas as pd

class Player_info():
    def __init__(self):
        self.bank = 0
        self.trash = 0
        self.deck = 0
        self.discard = 0
        self.hand = 0
        self.actions_played = 0
        self.opponent_discard = 0
        self.opponent_hand_deck = 0
        self.actions_remaining = 0
        self.actions_available = 0
        self.buys = 0
        self.treasure = 0


class Turn():
    def __init__(self):
        self.player = 0
        self.opponent = 0
        self.actions_remaining = 1
        self.actions_available = []
        self.buys_remaining = 1
        self.bank = 0
        self.treasure = 0
        self.card_to_buy = []
        self.trash = 0

turn = Turn()
ccd = card_classes.name_to_inst_dict
bank = card_classes.bank

def take_turn(player, opponent, one_or_two):
    start_turn(player,bank,turn,opponent)
    bankcp = dict(bank)
    turn.actions_available = return_action_cards(turn.player)
    starthand = [i.name for i in player.hand]
    deck = [i.name for i in player.deck]
    discard = [i.name for i in player.discard]
    actions = action_phase(one_or_two)
    buys = buy_phase(one_or_two)
    end_turn()

    return {"hand": starthand, "actions": actions, "buys": buys, "bank": bankcp, "player": one_or_two, "deck": deck, "discard": discard}

def action_phase(one_or_two):
    actions = []

    while turn.actions_available != [] and turn.actions_remaining != 0:
        player_info = Player_info()
        update_player_info(turn,player_info)
        ate_name = get_ate(player_info,one_or_two)
        if ate_name == 'None':
            break
        ate = ccd[ate_name]
        if one_or_two == 1:
            #HACKABLE here, passed object not string
            strategy = player_one_alg.execute_action_strategy(player_info,ate)
        elif one_or_two == 2:
            strategy = player_two_alg.execute_action_strategy(player_info,ate)    
        move_executed_actions(ate)
        ate.execute_action(turn,strategy)
        actions.append({'action': ate_name, 'strat': strategy, 'hand': [i.name for i in turn.player.hand], 'deck': [i.name for i in turn.player.deck], 'discard': [i.name for i in turn.player.discard]})
        turn.actions_available = return_action_cards(turn.player)

    return actions



def get_ate(player_info,one_or_two):
    if one_or_two == 1:
        action_name = player_one_alg.action_choice(player_info)
    elif one_or_two == 2:
        action_name = player_two_alg.action_choice(player_info)
    return action_name

def move_executed_actions(action):
    player = turn.player
    player.hand.remove(action)
    player.played_actions.append(action)


def buy_phase(one_or_two):
    play_treasures()
    tres = turn.treasure
    buys = []
    while turn.buys_remaining > 0:
        ctbn = get_card_to_buy(one_or_two)
        if ctbn == 'None':
            break
        else:
            ctb = ccd[ctbn]
            turn.player.gain_card(ctb,turn.treasure)
            turn.buys_remaining -= 1
            turn.treasure -= ctb.cost
            buys.append(ctbn)

    return {"tres": tres, "buys": buys}


def get_card_to_buy(one_or_two):
    player_info = Player_info()
    update_player_info(turn,player_info)
    if one_or_two == 1:
        ctb_name = player_one_alg.buy_choice(player_info)
    elif one_or_two == 2:
        ctb_name = player_two_alg.buy_choice(player_info)

    return ctb_name



def play_treasures():
    player = turn.player
    for x in range(0,len(player.hand)):
        card = player.hand[x]
        if card.grouping == 'Treasure':
            turn.treasure += card.treasure


def return_action_cards(player):
    action_list = []
    for x in range(0,len(player.hand)):
        action_check = player.hand[x].grouping
        if action_check == 'Action':
            action_list.append(player.hand[x])
    return action_list

def start_turn(player,bank,turn, opponent):
    turn.actions_remaining = 1
    turn.player = player
    turn.opponent = opponent
    turn.bank = bank
    turn.buys_remaining = 1
    turn.treasure = 0
    turn.number = player.turn
    player.turn += 1

def update_player_info(turn, player_info):
    player_info.bank = turn.bank
    player_info.trash = turn.trash
    player_info.deck = inst_to_string_convert(turn.player.deck)
    player_info.discard = inst_to_string_convert(turn.player.discard)
    player_info.hand = inst_to_string_convert(turn.player.hand)
    player_info.actions_played = turn.player.played_actions
    player_info.opponent_discard = inst_to_string_convert(turn.opponent.discard)
    player_info.opponent_hand_deck = inst_to_string_convert(randomize_opponent(turn.opponent))
    player_info.actions_remaining = turn.actions_remaining
    player_info.actions_available = turn.actions_available
    player_info.buys = turn.buys_remaining
    player_info.treasure = turn.treasure
    player_info.turn = turn.number
    return player_info

def end_turn():
    turn.player.discard_played_actions()
    turn.player.discard_hand()
    turn.player.draw_cards(5)

def inst_to_string_convert(instance_list):
    string_list = []
    for x in range(0,len(instance_list)):
        string_list.append(instance_list[x].name)
    return string_list


def randomize_opponent(opponent):
    deck_hand = opponent.deck + opponent.hand
    shuffle(deck_hand)
    return deck_hand

