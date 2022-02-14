from enum import Enum
import abc
from random import shuffle
from collections import Counter  # Counter is convenient for counting objects (a specialized dictionary)


class PlayingCard(abc.ABC):
    def __init__(self, suit):
        self.suit = suit

    @abc.abstractmethod
    def get_value(self):
        pass

    def __eq__(self, other):
        return self.get_value() == other.get_value() and self.suit == other.suit

    def __lt__(self, other):
        if self.get_value() == other.get_value():
            return self.suit < other.suit
        else:
            return self.get_value() < other.get_value()


class NumberedCard(PlayingCard):
    def __init__(self, value, suit):
        super().__init__(suit)
        self.value = value

    def get_value(self):
        return self.value

    def __str__(self):
        return f"{self.value} of {self.suit.name}"

    def __repr__(self):
        return 'Card(%r, %r)' % (self.get_value(), self.suit.name)


class JackCard(PlayingCard):
    def __init__(self, suit):
        super().__init__(suit)

    def get_value(self):
        return 11

    def __str__(self):
        return f"Jack of {self.suit.name}"

    def __repr__(self):
        return 'Card(%r, %r)' % (self.get_value(), self.suit.name)


class QueenCard(PlayingCard):
    def __init__(self, suit):
        super().__init__(suit)

    def get_value(self):
        return 12

    def __str__(self):
        return f"Queen of {self.suit.name}"

    def __repr__(self):
        return 'Card(%r, %r)' % (self.get_value(), self.suit.name)


class KingCard(PlayingCard):
    def __init__(self, suit):
        super().__init__(suit)

    def __str__(self):
        return f"King of {self.suit.name}"

    def get_value(self):
        return 13

    def __repr__(self):
        return 'Card(%r, %r)' % (self.get_value(), self.suit.name)


class AceCard(PlayingCard):
    def __init__(self, suit):
        super().__init__(suit)

    def get_value(self):
        return 14

    def __str__(self):
        return f"Ace of {self.suit.name}"

    def __repr__(self):
        return 'Card(%r, %r)' % (self.get_value(), self.suit.name)


class Suit(Enum):
    Hearts = 1
    Spades = 2
    Clubs = 3
    Diamonds = 4

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return 'Suit(%r)' % Suit

    def __lt__(self, other):
        return self.value < other.value


class Hand(object):
    """
    A class used to represent a players hand

    Attributes
    ----------
    None

    Methods
    -------
    add_card(card)
        Adds a card to the players hand
    drop_card(discards)
        Drop the desired cards from the players hand
    show_hand
        Prints the hand to the terminal
    sort
        Sorts the cards in the players hand by ?value?
    best_poker_hand
        Checks what combination of the cards on hand that produces the most value
    """

    def __init__(self):
        """
        Parameters
        ----------
        None?  is cards a parameter
        """

        self.cards = []

    # def __repr__(self):
    #     s = ""
    #     for c in self.cards:
    #         s += str(c) + '\n'
    #     s.split('\n')
    #     return "Hand(" + ','.join(s) + ")"

    def __str__(self):
        s = ""
        for c in self.cards:
            s = s + str(c) + '\n'  # c.__str__() + "\n"
        return s

    def add_card(self, card):
        """Adds a card to the players hand

        Parameters
        ----------
        card(tuple)
            A playing card
        """

        self.cards.append(card)

    def drop_cards(self, discards):
        """ Drop the desired cards from the players hand

        Parametes
        ---------


        :param discards:
        :return:
        """
        discards.sort(reverse=True)
        for n in discards:
            self.cards.pop(n)

    def show_hand(self):
        for c in self.cards:
            print(c)

    def sort(self):
        self.cards.sort()

    def best_poker_hand(self, table_cards=[]):
        for tc in table_cards:
            self.cards.append(tc)
        return self.cards


class StandardDeck(object):
    """Initializes and creates a deck of all 52 playing cards. Method create_deck: creates the deck,
     draw: draws the top card in the deck, shuffle: shuffles the deck, show_deck: shows the deck in the current order"""
    def __init__(self):
        self.deck = []
        self.create_deck()

    def create_deck(self):
        for s in Suit:
            self.deck.append(AceCard(s))
            self.deck.append(KingCard(s))
            self.deck.append(QueenCard(s))
            self.deck.append(JackCard(s))
            for val in range(2, 11):
                card = NumberedCard(val, s)
                self.deck.append(card)

    def show_deck(self):
        for c in self.deck:
            print(c)

    def __repr__(self):
        s = str()
        for i in range(len(self.deck)):
            s += str(self.deck[i]) + "\n"
            return s

    def shuffle(self):
        return shuffle(self.deck)

    def draw(self):
        return self.deck.pop()


class PokerHand(object):
    def __init__(self, cards):
        #super().__init__(cards)
        self.cards = cards

    def give_value(self):
        pass

    def __lt__(self, other):
        pass

    @staticmethod
    def check_straight_flush(cards):
        """
        Checks for the best straight flush in a list of cards (may be more than just 5)
        :param cards: A list of playing cards.
        :return: None if no straight flush is found, else the value of the top card.
        """
        vals = [(c.give_value(), c.suit) for c in cards] \
               + [(1, c.suit) for c in cards if c.give_value() == 14]  # Add the aces!
        for c in reversed(cards):  # Starting point (high card)
            # Check if we have the value - k in the set of cards:
            found_straight = True
            for k in range(1, 5):
                if (c.give_value() - k, c.suit) not in vals:
                    found_straight = False
                    break

            if found_straight:
                return c.give_value()

    def check_four_of_a_kind(self):
        pass

    def check_full_house(self, cards):
        """
        Checks for the best full house in a list of cards (may be more than just 5)
        :param cards: A list of playing cards
        :return: None if no full house is found, else a tuple of the values of the triple and pair.
        """
        value_count = Counter()
        for c in cards:
            value_count[c.give_value()] += 1
        # Find the card ranks that have at least three of a kind
        threes = [v[0] for v in value_count.items() if v[1] >= 3]
        threes.sort()
        # Find the card ranks that have at least a pair
        twos = [v[0] for v in value_count.items() if v[1] >= 2]
        twos.sort()
        # Threes are dominant in full house, lets check that value first:
        for three in reversed(threes):
            for two in reversed(twos):
                if two != three:
                    return three, two

    def check_flush(self):
        pass

    def check_straight(self):
        pass

    def check_three_of_a_kind(self):
        pass

    def check_two_pair(self):
        pass

    def check_pair(self, cards):
        pass

    def check_high_card(self):
        pass


d = StandardDeck()
# d.show_deck()
sh = JackCard(Suit.Hearts)
# print(sh.get_value())
# print(Suit.Hearts.value)
# print(Suit.Hearts > Suit.Spades)
h = Hand()

h.add_card(d.draw())
h.add_card(d.draw())
T_cards = [JackCard(Suit.Hearts), QueenCard(Suit.Hearts), KingCard(Suit.Hearts), AceCard(Suit.Hearts), NumberedCard(10, Suit.Hearts)]
#ph1 = h.best_poker_hand(cl)
print(h.best_poker_hand(T_cards))
print(isinstance(h, Hand))
print(type(h), type(Hand))
#print(check_straight_flush(T_cards))
# card = KingCard(Suit.Hearts)
# print(card.give_value())
# h.show_hand()
#print(h)


