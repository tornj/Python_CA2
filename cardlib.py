from enum import Enum
from functools import total_ordering
import abc
from random import shuffle


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
    def __init__(self):
        self.cards = []

    # def __repr__(self):
    #     s = ''
    #     for i in self.cards:
    #         s = s + str(self.cards[i]) + '\n'
    #         return s

    def add_card(self, card):
        self.cards.append(card)

    def drop_cards(self, discards):
        discards.sort(reverse=True)
        for n in discards:
            self.cards.pop(n)

    def show_hand(self):
        for c in self.cards:
            print(c)

    def sort(self):
        self.cards.sort()


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

    # def __repr__(self):
    #     s = str()
    #     for i in range(len(self.deck)):
    #         s += str(self.deck[i])# + "\n"
    #         return s

    def shuffle(self):
        return shuffle(self.deck)

    def draw(self):
        return self.deck.pop()

d = StandardDeck()
#d.show_deck()
sh = Suit.Hearts
print(sh.value)
print(Suit.Hearts.value)
print(Suit.Hearts > Suit.Spades)
#print(repr(d))
# d.shuffle()
# H1 = Hand()
# H1.add_card(d.draw())
# H1.add_card(d.draw())
# H1.add_card(d.draw())
# H1.add_card(d.draw())
# H1.add_card(d.draw())
# H1.sort()
# H1.show_hand()

# for i in range(4):
#     print('new', H1.cards[i])
#     print(H1.cards[i+1])
#     assert H1.cards[i] < H1.cards[i + 1] or H1.cards[i] == H1.cards[i + 1]


#print(len(H1.cards))
# H1.drop_cards([1, 0, 4])
# H1.show_hand()
# sj = JackCard(Suit.Spades)
# print(type(sj))


# print(d.show_deck())

# a = AceCard(Suit.Spades)
# print(a)
#
# h5 = NumberedCard(4, Suit.Hearts)
# print(JackCard(Suit.Spades) > NumberedCard(4, Suit.Hearts))
