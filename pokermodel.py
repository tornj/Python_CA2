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
        self.flipped_cards = False

    def __iter__(self):
        return iter(self.cards)

    def flip(self):
        # Flips over the cards (to hide them)
        self.flipped_cards = not self.flipped_cards
        self.new_cards.emit()  # something changed, better emit the signal!

    def flipped(self):
        # This model only flips all or no cards, so we don't care about the index.
        # Might be different for other games though!
        return self.flipped_cards

    def add_card(self, card):
        super().add_card(card)
        self.new_cards.emit()  # something changed, better emit the signal!


# class MoneyModel(QObject):
#     new_signal = pyqtSignal()
#
#     def __init__(self):
#         super().__init__()

class PlayerModel(QObject):
    data_changed = pyqtSignal()

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.balance = 0
        self.bet = 0
        self.bet_gap = 0
        self.cards = []
        self.active = False

        self.hand = Hand()

    def set_active(self,active):
        self.active = active
        self.data_changed.emit()

class GameModel(QObject):

    new_signal = pyqtSignal()

    def __init__(self, players):
        self.winner = None
        self.end_round = False
        self.players = players
        self.deck = StandardDeck()
        self.table_cards = []
        self.pot = 0
        #self.acting_player = PlayerModel()
        self.player_turn = -1

        self.list_of_players = []
        self.list_of_players_left = []

        self.player_bet_gap = 0
        self.highest_bet = 0

    # def answer(self, player):
    #     player.bet_gap = self.highest_bet - player.bet
    #
    #     while True:
    #         if player.response == "Fold":
    #             self.list_of_players_left.pop(player)
    #             self.end_round = True
    #
    #         if player.response == "Call/Check":
    #             return True  # Starta nästa runda
    #
    #         if player.response == "Bet/Raise":
    #             pass
    #
    # def Game_round(self):
    #     # Ge båda spelarna två kort
    #     self.deck.shuffle()
    #     self.deal_to_players()
    #     self.asking_round()
    #
    #     if not self.end_round:
    #         self.deal_flop()
    #         self.asking_round()
    #
    #     if not self.end_round:
    #         self.deal_turn()
    #         self.asking_round()
    #
    #     if not self.end_round:
    #         self.deal_river()
    #         self.asking_round()
    #
    #     self.find_winner()  # Ska implementera
    #     self.end_round()  # Ska implementera
    #
    #
    def CALL(self):  #När man klickar på call så ska ja byta fönster (och flippa korten)
        self.list_of_players[self.player_turn].set_active(False)
        self.player_turn = (self.player_turn + 1) % len(self.list_of_players)
        self.list_of_players[self.player_turn].set_active(True)
        self.new_signal.emit()
    #
    # def asking_round(self):
    #     i = 0
    #     while True:
    #         self.acting_player = self.list_of_players[i]
    #         player_answer = self.answer(self.acting_player)
    #
    #         if player_answer:  # Starta nästa runda
    #             break
    #
    #         if player_answer == "Fold":  #Annonsera vinnare
    #             pass
    #
    # def deal_to_players(self):
    #     for player in self.list_of_players:
    #         player.hand.add_card(self.deck.draw())
    #         player.hand.add_card(self.deck.draw())
    #
    # def deal_flop(self):  # 3 första
    #     self.table_cards.append(self.deck.draw())
    #     self.table_cards.append(self.deck.draw())
    #     self.table_cards.append(self.deck.draw())
    #
    # def deal_turn(self):
    #     self.table_cards.append(self.deck.draw())
    #
    # def deal_river(self):
    #     self.table_cards.append(self.deck.draw())
    #
    # def clear_for_new_round(self):
    #     self.table_cards.clear()
    #     self.winner = None
    #     self.deck = StandardDeck()
    #     self.pot = 0
    #
    # def end_round(self):  # cl
    #     for player in self.list_of_players:
    #         if player.balance == 0:
    #             pass # Quit game, announce winner
    #
    #     self.pot = 0
    #     self.table_cards.clear()
    #     for player in self.list_of_players:
    #         player.hand.drop_cards([0, 1])
    #
    #     # Måste lägga till mer saker som skall rensas innan nästa omgång
    #
    #
    #
    # def find_winner(self):
    #     pass


