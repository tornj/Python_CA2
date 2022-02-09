from enum import Enum


class PlayingCard(object):
    def __init__(self, suit):
        self.suit = suit

    def __eq__(self, other):
        return self.suit == other.suit


class NumberedCard(PlayingCard):
    def __init__(self, value, suit):
        super().__init__(suit)
        self.value = value

    def get_value(self):
        return self.value

    def __str__(self):
        return f"{self.value} of {self.suit}"


class JackCard(PlayingCard):
    def __init__(self, suit):
        super().__init__(suit)

    def get_value(self):
        return 11


class QueenCard(PlayingCard):
    def __init__(self, suit):
        super().__init__(suit)

    def get_value(self):
        return 12


class KingCard(PlayingCard):
    def __init__(self, suit):
        super().__init__(suit)

    def __str__(self):
        return f"{13} of {self.suit}"


    def get_value(self):
        return 13



class AceCard(PlayingCard):
    def __init__(self, suit):
        super().__init__(suit)

    def get_value(self):
        return 14


class Suit(Enum):
    Hearts = 1
    Spades = 2
    Clubs = 3
    Diamonds = 4


s = Suit(1)
print(s)

class Hand(object):
    def __init__(self):
        pass

    def add_card(self):
        pass

    def drop_cards(self):
        pass

    def sort(self):
        pass


print(Suit.Hearts == Suit.Spades)
sk = KingCard(Suit.Spades)
print(sk)
h5 = NumberedCard(4, Suit.Hearts)
print(h5)
print(Suit.Hearts)
x = isinstance(h5.suit, Enum)
print(x)


