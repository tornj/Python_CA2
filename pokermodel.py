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
        self.cards = []
        self.flipped_cards = False

    def __iter__(self):
        return iter(self.cards)


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
        self.value -= other
        self.player_money.emit()
        return self

    def __add__(self, other):
        add = self.value + other.value
        self.player_money.emit()
        return add

    def __sub__(self, other):
        sub = self.value - other.value
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

    def __init__(self, name, stake):
        super().__init__()
        self.name = name
        self.balance = int(stake)
        self.bet = 0
        self.bet_gap = 0
        self.cards = []
        self.active = False
        self.hand = HandModel()
        self.max_bet = self.balance

    def set_active(self, active):
        self.active = active
        self.hand.flip(not active)
        self.active_changed.emit()


class GameModel(QObject):
    new_turn_signal = pyqtSignal()
    data_changed = pyqtSignal()
    game_message = pyqtSignal((str,))
    game_signal = pyqtSignal()
    update_table_cards = pyqtSignal()
    disable_bet_button = pyqtSignal()

    # update_bet = pyqtSignal()

    def __init__(self, players):
        super().__init__()
        self.winner = None
        self.End_Round = False
        self.players = players
        self.deck = StandardDeck()
        self.table_cards = TableCardsModel()
        self.pot = 0
        self.player_turn = 0
        self.turn = 0
        self.active_player = players[self.player_turn]
        self.player_ready = False
        self.list_of_players_left = players
        self.highest_bet = 0
        self.min_bet = self.highest_bet
        self.disable_bet = []

        self.dealt_flop = False
        self.dealt_turn = False
        self.dealt_river = False

    def Start(self):
        self.players[self.player_turn].set_active(True)
        self.deck = StandardDeck()
        self.deck.shuffle()
        self.deal_to_players()
        # self.game_signal.emit()

    def bet_limits(self):
        self.min_bet = self.highest_bet + 1
        self.active_player.max_bet = min([self.players[0].balance, self.players[1].balance])
        #
        # self.min_bet = self.players[(self.player_turn + 1) % 2].bet
        # self.active_player.max_bet = self.players[(self.player_turn + 1) % 2].bet

        return self.min_bet, self.active_player.max_bet

    # def check_all_in(self):
    #     if self.active_player.max_bet == 0:
    #         self.deal()

    def deal_to_players(self):
        for player in self.players:
            player.hand.add_card(self.deck.draw())
            player.hand.add_card(self.deck.draw())
        self.data_changed.emit()

    def deal_flop(self):  # 3 första
        self.table_cards.add_card(self.deck.draw())  # table cards måste vara en lista för att jag ska kunna använda
        self.table_cards.add_card(self.deck.draw())  # pokerhand, men måste samtidigt vara ett Handmodel objekt för
        self.table_cards.add_card(self.deck.draw())  # att ja ska kunna visa dem med CardView...
        self.dealt_flop = True
        self.new_round()
        self.data_changed.emit()

    def deal_turn(self):
        self.table_cards.add_card(self.deck.draw())
        self.dealt_turn = True
        self.new_round()
        self.data_changed.emit()

    def deal_river(self):
        self.table_cards.add_card(self.deck.draw())
        self.dealt_river = True
        self.new_round()
        self.data_changed.emit()

    def new_round(self):
        self.turn = 0
        self.highest_bet = 0
        for player in self.players:
            player.bet = 0

    def end_round(self):
        for player in self.players:
            if player.balance == 0:
                quit()  # Quit game, announce winner

        # self.pot.clear()
        self.dealt_flop = False
        self.dealt_turn = False
        self.dealt_river = False
        self.turn = 0
        self.pot = 0
        self.highest_bet = 0
        self.table_cards.cards.clear()
        self.update_table_cards.emit()
        for player in self.players:
            player.hand.cards.clear()
            player.bet= 0

        self.Start()

    def find_winner(self):
        players_ph = []
        for player in self.players:
            players_ph.append(player.hand.best_poker_hand(self.table_cards))

        if players_ph[0] < players_ph[1]:
            self.players[1].balance += self.pot
            self.game_message.emit(self.players[1].name + ' won ' + str(self.pot) + '$')
            # self.game_message.emit(self.players[1].name + ' won ' + str(self.pot) + '$, with: ' + self.players[1].hand
            #  + ' against: ' + self.players[0].hand)
        elif players_ph[0] > players_ph[1]:
            self.players[0].balance += self.pot
            self.game_message.emit(self.players[0].name + ' won ' + str(self.pot) + '$')
        else:
            pass

    def new_turn(self):
        self.players[self.player_turn].set_active(False)
        self.player_turn = (self.player_turn + 1) % len(self.players)
        self.players[self.player_turn].set_active(True)
        self.active_player = self.players[self.player_turn]
        # self.new_turn_signal.emit()

    def deal(self):
        self.turn += 1
        if self.turn > 1:  # Starta nästa runda
            if not self.dealt_flop:
                self.deal_flop()
            elif not self.dealt_turn:
                self.deal_turn()
            elif not self.dealt_river:
                self.deal_river()
            else:
                self.find_winner()
                self.end_round()

    def fold(self):
        #self.game_message.emit(self.players[(self.player_turn + 1) % 2].name + ' won ' + str(self.pot) + '$')
        self.players[(self.player_turn+1) % len(self.players)].balance += self.pot
        self.end_round()
        self.new_turn()

    def call(self):
        self.active_player.bet_gap = self.highest_bet - self.active_player.bet
        self.active_player.bet = self.active_player.bet_gap
        self.active_player.bet_gap = 0
        # self.active_player.bet = self.highest_bet - self.active_player.bet
        self.active_player.balance -= self.active_player.bet
        self.pot += self.active_player.bet
        self.deal()
        if self.active_player.balance == 0:
            self.turn = 1
            self.deal()
            self.turn = 1
            self.deal()
            self.turn = 1
            self.deal()

        self.data_changed.emit()
        self.new_turn()

    def bet(self, amount: int):
        self.active_player.bet += amount
        self.active_player.balance -= amount
        self.pot += amount
        self.highest_bet += amount
        self.player_ready = False
        self.turn += 1
        self.data_changed.emit()
        self.new_turn()
        if self.players[(self.player_turn + 1) % 2].balance == 0:
            self.disable_bet_button.emit()