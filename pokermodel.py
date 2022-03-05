import abc
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
from abc import abstractmethod
import sys
from cardlib import *


class CardModel(QObject):
    """ Base class that described what is expected from the CardView widget """

    new_cards = pyqtSignal()  #: Signal should be emited when cards change.

    @abc.abstractmethod
    def __iter__(self):
        """Returns an iterator of card objects"""

    @abc.abstractmethod
    def flipped(self):
        """Returns true of cards should be drawn face down"""


class HandModel(Hand, CardModel):
    def __init__(self):
        Hand.__init__(self)
        CardModel.__init__(self)
        # Additional state needed by the UI
        self.flipped_cards = True

    def __iter__(self):
        return iter(self.cards)

    def flip(self, state):
        # Flips over the cards (to hide them)
        self.flipped_cards = state
        self.new_cards.emit()  # something changed, better emit the signal!

    def flipped(self):
        # This model only flips all or no cards, so we don't care about the index.
        # Might be different for other games though!
        return self.flipped_cards

    def add_card(self, card):
        super().add_card(card)
        self.new_cards.emit()  # something changed, better emit the signal!


class TableCardsModel(HandModel):
    def __init__(self):
        CardModel.__init__(self)
        self.table_cards = []

    def __iter__(self):
        return iter(self.table_cards)


class MoneyModel(QObject):
    player_money = pyqtSignal()

    def __init__(self, value=0):
        super().__init__()
        self.value = value

    def __iadd__(self, other: int):
        self.value += other
        self.player_money.emit()
        return self

    def __isub__(self, other):
        self.value -= other.value
        self.player_money.emit()
        return self

    def __add__(self, other):
        add = self.value + other, other + self.value
        self.player_money.emit()
        return add

    def __sub__(self, other):
        sub = self.value - other
        self.player_money.emit()
        return sub

    def __eq__(self, other: int):
        return self.value == other

    def __str__(self):
        return f'{self.value}'

    def __repr__(self):
        return str(self.value)

    def clear(self):
        self.value = 0
        self.player_money.emit()


class PlayerModel(QObject):
    active_changed = pyqtSignal()

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.balance = MoneyModel(1000)
        self.bet = MoneyModel()
        self.bet_gap = MoneyModel()
        self.cards = []
        self.active = False
        self.hand = HandModel()
        self.max_bet = self.balance.value

    def set_active(self, active):
        self.active = active
        self.hand.flip(not active)
        self.active_changed.emit()


class GameModel(QObject):
    new_turn_signal = pyqtSignal()
    #money_signal = pyqtSignal()
    game_signal = pyqtSignal()
    #pot_signal = pyqtSignal
    data_changed = pyqtSignal()

    def __init__(self, players):
        super().__init__()
        self.winner = None
        self.End_Round = False
        self.players = players
        self.deck = StandardDeck()
        self.table_cards = TableCardsModel()
        self.pot = MoneyModel()
        self.player_turn = 0
        self.turn = 0
        self.active_player = players[self.player_turn]
        self.player_ready = False
        self.list_of_players_left = players
        self.highest_bet = 0
        self.min_bet = 5
        
    def Start(self):
        self.players[self.player_turn].set_active(True)
        self.deal_to_players()
        self.game_signal.emit()
  
    def bet_limits(self):
        return self.min_bet, self.active_player.max_bet

    def Game_round(self):
        # Ge båda spelarna två kort
        self.deck = StandardDeck()
        self.deck.shuffle()
        self.deal_to_players()
        self.asking_round()

        if not self.End_Round:
            self.deal_flop()
            self.asking_round()

        if not self.End_Round:
            self.deal_turn()
            self.asking_round()

        if not self.End_Round:
            self.deal_river()
            self.asking_round()

        self.find_winner()  # Ska implementera
        self.end_round()  # Ska implementera

    def asking_round(self):
        self.turn = 0
        while True:
            if self.player_ready and self.turn >= 1:  # Starta nästa runda
                break
            self.turn += 1

    def deal_to_players(self):
        for player in self.players:
            player.hand.add_card(self.deck.draw())
            player.hand.add_card(self.deck.draw())

    def deal_flop(self):  # 3 första
        self.table_cards.add_card(self.deck.draw())  # table cards måste vara en lista för att jag ska kunna använda
        self.table_cards.add_card(self.deck.draw())  # pokerhand, men måste samtidigt vara ett Handmodel objekt för
        self.table_cards.add_card(self.deck.draw())  # att ja ska kunna visa dem med CardView...

    def deal_turn(self):
        self.table_cards.add_card(self.deck.draw())

    def deal_river(self):
        self.table_cards.add_card(self.deck.draw())

    def end_round(self):
        for player in self.players:
            if player.balance == 0:
                pass  # Quit game, announce winner

        self.pot.clear()
        self.table_cards.clear()
        for player in self.players:
            player.hand.drop_cards([0, 1])  # Måste lägga till mer saker som skall rensas innan nästa omgång

    def find_winner(self):
        players_ph = []
        for player in self.players:
            players_ph.append(player.hand.best_poker_hand(self.table_cards))

        if players_ph[0] < players_ph[1]:
            self.players[1].balance += self.pot
        elif players_ph[0] > players_ph[1]:
            self.players[0].balance += self.pot
        else:
            pass


    def new_turn(self):
        self.players[self.player_turn].set_active(False)
        self.player_turn = (self.player_turn + 1) % len(self.players)
        self.players[self.player_turn].set_active(True)

        self.active_player = self.players[self.player_turn]
        self.new_turn_signal.emit()

    def fold(self):
        self.list_of_players_left.pop(self.active_player)
        self.End_Round = True
        self.new_turn()

    def call(self):
        # self.active_player.bet_gap = self.highest_bet - self.active_player.bet
        # self.active_player.bet = self.active_player.bet_gap
        # self.active_player.bet_gap = 0
        self.active_player.bet = self.highest_bet - self.active_player.bet
        self.active_player.balance -= self.active_player.bet
        self.pot += self.active_player.bet
        self.player_ready = True
        self.data_changed.emit()

        self.new_turn()

        #self.new_pot.emit()

    def bet(self, amount: int):
        self.active_player.bet = amount
        self.active_player.balance -= amount
        self.pot += amount
        self.highest_bet = amount
        self.player_ready = False
        #self.pot_signal.emit()
        self.data_changed.emit()
        self.new_turn()


