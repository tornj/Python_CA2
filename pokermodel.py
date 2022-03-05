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


class MoneyModel(QObject):
    new_value = pyqtSignal()

    def __init__(self, value=0):
        super().__init__()
        self.value = value

    def __iadd__(self, other):
        self.value += other
        self.new_value.emit()
        return self

    def __isub__(self, other):
        self.value -= other
        self.new_value.emit()
        return self

    def __eq__(self, other: int):
        return self.value == other

    def __str__(self):
        return f'{self.value}'

    def clear(self):
        self.value = 0


class PlayerModel(QObject):
    active_changed = pyqtSignal()

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.balance = MoneyModel(100)
        self.bet = MoneyModel()
        self.bet_gap = MoneyModel()
        self.cards = []

        self.active = False

        self.hand = HandModel()

    def set_active(self, active):
        self.active = active
        self.hand.flip(not active)
        self.active_changed.emit()


class GameModel(QObject):
    new_signal = pyqtSignal()

    def __init__(self, players):
        super().__init__()
        self.winner = None
        self.End_Round = False
        self.players = players
        self.deck = StandardDeck()
        self.table_cards = []
        self.pot = 0
        # self.acting_player = PlayerModel()
        self.player_turn = -1
        self.turn = 0
        self.player_response = 'Ja vet inte'
        self.list_of_players_left = []

        self.player_bet_gap = 0
        self.highest_bet = 0

    def Start(self):
        self.players[self.player_turn].set_active(True)
        self.deal_to_players()
        self.new_signal.emit()

    def bet_limits(self):
        return , 5

    def Game_round(self):
        # Ge båda spelarna två kort
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

    def answer(self, player):  # Måste skicka in player model object
        player.bet_gap = self.highest_bet - player.bet

        if self.player_response == "Fold":
            self.list_of_players_left.pop(player)
            self.End_Round = True

        if self.player_response == "Call/Check":
            player.bet = player.bet_gap
            player.bet_gap = 0
            player.balance -= player.bet
            self.pot += player.bet
            return True  # Starta nästa runda

        if self.player_response == "Bet/Raise":
            # player.bet = INPUT??
            self.pot += player.bet
            self.highest_bet = player.bet
            return True

    def asking_round(self):
        i = 0
        self.turn = 0
        while True:
            self.player_turn = self.players[i]  # Player turn ska vara ett PlayerModel objekt
            player_answer = self.answer(self.player_turn)
            i += 1
            i %= 2

            if player_answer and self.turn > 1:  # Starta nästa runda
                break

            if player_answer == "Fold":  # Annonsera vinnare
                pass

            self.turn += 1

    def deal_to_players(self):
        for player in self.players:
            player.hand.add_card(self.deck.draw())
            player.hand.add_card(self.deck.draw())

    def deal_flop(self):  # 3 första
        self.table_cards.append(self.deck.draw())
        self.table_cards.append(self.deck.draw())
        self.table_cards.append(self.deck.draw())

    def deal_turn(self):
        self.table_cards.append(self.deck.draw())

    def deal_river(self):
        self.table_cards.append(self.deck.draw())

    def clear_for_new_round(self):
        self.table_cards.clear()
        self.winner = None
        self.deck = StandardDeck()
        self.pot = 0

    def end_round(self):
        for player in self.players:
            if player.balance == 0:
                pass  # Quit game, announce winner

        self.pot.clear()
        self.table_cards.clear()
        for player in self.players:
            player.hand.drop_cards([0, 1])

        # Måste lägga till mer saker som skall rensas innan nästa omgång

    def find_winner(self):
        pass

    def new_turn(self):
        self.players[self.player_turn].set_active(False)
        self.player_turn = (self.player_turn + 1) % len(self.players)
        self.players[self.player_turn].set_active(True)
        self.new_signal.emit()

    def fold(self):
        self.player_response = 'Fold'
        self.players[self.player_turn].set_active(False)
        self.player_turn = (self.player_turn + 1) % len(self.players)
        self.players[self.player_turn].set_active(True)
        self.new_signal.emit()

    def call(self):  # När man klickar på call så ska ja byta fönster (och flippa korten)
        self.player_response = 'Call/Check'
        self.new_turn()
        self.pot = 10
        self.new_pot.emit()

    def bet(self, amount: int):
        self.player_response = 'Bet/Raise'
        self.players[self.player_turn].set_active(False)
        self.player_turn = (self.player_turn + 1) % len(self.players)
        self.players[self.player_turn].set_active(True)
        self.new_signal.emit()