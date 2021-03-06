from enum import Enum
import abc
from random import shuffle
from collections import Counter
from enum import IntEnum


class PlayingCard(abc.ABC):
    """Parent class for all the different playing cards

    :param suit: suit of card
    :type suit: Suit"""

    def __init__(self, suit):
        self.suit = suit

    @abc.abstractmethod
    def get_value(self):
        """ A method returning the value of the card"""
        pass

    def __eq__(self, other):
        return self.get_value() == other.get_value() and self.suit == other.suit

    def __lt__(self, other):
        if self.get_value() == other.get_value():
            return self.suit < other.suit
        else:
            return self.get_value() < other.get_value()


class NumberedCard(PlayingCard):
    """ A class that creates Numbered playing cards

    :param suit: suit of card
    :type suit: Suit
    :param value: value of card
    :type value: int
    """
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
    """ A class that creates Jack playing cards

    :param suit: suit of card
    :type suit: Suit
    """
    def __init__(self, suit):
        super().__init__(suit)

    def get_value(self):
        return 11

    def __str__(self):
        return f"Jack of {self.suit.name}"

    def __repr__(self):
        return 'Card(%r, %r)' % (self.get_value(), self.suit.name)


class QueenCard(PlayingCard):
    """ A class that creates Queen playing cards

    :param suit: suit of card
    :type suit: Suit
    """
    def __init__(self, suit):
        super().__init__(suit)

    def get_value(self):
        return 12

    def __str__(self):
        return f"Queen of {self.suit.name}"

    def __repr__(self):
        return 'Card(%r, %r)' % (self.get_value(), self.suit.name)


class KingCard(PlayingCard):
    """ A class that creates King playing cards

    :param suit: suit of card
    :type suit: Suit
    """
    def __init__(self, suit):
        super().__init__(suit)

    def __str__(self):
        return f"King of {self.suit.name}"

    def get_value(self):
        return 13

    def __repr__(self):
        return 'Card(%r, %r)' % (self.get_value(), self.suit.name)


class AceCard(PlayingCard):
    """ A class that creates Ace playing cards

    :param suit: suit of card
    :type suit: Suit
    """
    def __init__(self, suit):
        super().__init__(suit)

    def get_value(self):
        return 14

    def __str__(self):
        return f"Ace of {self.suit.name}"

    def __repr__(self):
        return 'Card(%r, %r)' % (self.get_value(), self.suit.name)


class Suit(Enum):
    """Enum class that represents the suits of each playing card"""
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
    """A class used to represent a players hand"""

    def __init__(self):
        self.cards = []

    def __str__(self):
        s = ""
        for c in self.cards:
            s = s + str(c) + '\n'
        return s

    def add_card(self, card):
        """Adds a card to the players hand

        :param card: A playing card
        :type card: PlayingCard
        """

        self.cards.append(card)

    def drop_cards(self, discards):
        """ Drop the desired cards from the players hand

        :param discards: A list of desired discards
        :type discards: list
        """
        discards.sort(reverse=True)
        for n in discards:
            self.cards.pop(n)

    def show_hand(self):
        """Method that displays the hand in the command window"""
        for c in self.cards:
            print(c)

    def sort(self):
        """Sorts the hand from the lowest to the highest card"""
        self.cards.sort()

    def best_poker_hand(self, table_cards=[]):
        """A method that creates a poker hand object and returns the combination of the 5 best playing cards

        :param table_cards: A list of the cards on the table.
        :type table_cards: list

        :return: A poker hand of the 5 best cards out of the cards on hand and card on the table.
        :return type: PokerHand
        """
        all_cards = self.cards + table_cards
        ph = PokerHand(all_cards)
        return ph


class StandardDeck(object):
    """Initializes and creates a deck of all 52 playing cards."""

    def __init__(self):
        self.deck = []
        self.create_deck()

    def create_deck(self):
        """A method that creates a deck of 52 unique playingcards. """
        for s in Suit:
            self.deck.append(AceCard(s))
            self.deck.append(KingCard(s))
            self.deck.append(QueenCard(s))
            self.deck.append(JackCard(s))
            for val in range(2, 11):
                card = NumberedCard(val, s)
                self.deck.append(card)

    def show_deck(self):
        """ A method that prints each card in the deck to the command window. """
        for c in self.deck:
            print(c)

    def __repr__(self):
        s = str()
        for i in range(len(self.deck)):
            s += str(self.deck[i]) + "\n"
            return s

    def shuffle(self):
        """ A method that shuffles the deck"""
        shuffle(self.deck)

    def draw(self):
        """ A method that draws a card from the deck

        :return: The card that have been drawn
        :return type: PlayingCard
        """
        return self.deck.pop()


class Pokerhand_types(IntEnum):
    """Enum class that represents the different hand types"""
    straight_flush = 9
    four_of_a_kind = 8
    full_house = 7
    flush = 6
    straight = 5
    three_of_a_kind = 4
    two_pair = 3
    pair = 2
    high_card = 1


class PokerHand(object):
    """ A class used to represent a players hand"""

    def __init__(self, cards):
        self.cards = cards
        self.type = 0
        self.check_checks()

    def check_checks(self):
        """Loops through the checks and returns a tuple of the best cards and what hand type they represent

        :param cards: A list of playing cards
        :type list

        :return Tuple  of the best cards and their corresponding hand type.
        :return type: tuple
        """
        functions = [self.check_straight_flush, self.check_four_of_a_kind, self.check_full_house, self.check_flush,
                     self.check_straight, self.check_three_of_a_kind, self.check_two_pair, self.check_pair,
                     self.check_high_card]
        for func, t in zip(functions, Pokerhand_types):
            test_cards = func(self.cards)
            self.type = t
            if test_cards is not None:
                self.cards = test_cards
                break
        return self.type, self.cards

    def show_poker_hand(self):
        for c in self.cards:
            print(c)

    def __lt__(self, other):
        if self.type == other.type:
            return self.cards < other.cards
        else:
            return self.type < other.type

    def __eq__(self, other):
        if self.type == other.type:
            return self.cards == other.cards
        else:
            return self.type == other.type

    def __str__(self):
        if self.type.name == 'straight_flush':
            handtype=''.join(self.type.name.split('_'))
            rep = f'({handtype} high {self.cards})'
            return rep
        elif self.type.name == 'four_of_a_kind':
            handtype=' '.join(self.type.name.split('_'))
            rep = f'{handtype} of {self.cards[0]}, kicker: {self.cards[1]}'
            return rep
        elif self.type.name == 'full_house':
            rep = f"full house {self.cards[0]}'s over {self.cards[1]}'s"
            return rep
        elif self.type.name == 'flush':
            rep = f'{self.type.name} with {self.cards}'
            return rep
        elif self.type.name == 'straight':
            rep = f'{self.cards} high {self.type.name}'
            return rep
        elif self.type.name == 'three_of_a_kind':
            handtype = ''.join(self.type.name.split('_'))
            rep = f'{handtype} of {self.cards[0]}, kickers: {self.cards[1]}'
            return rep
        elif self.type.name == 'two_pair':
            handtype = ''.join(self.type.name.split('_'))
            rep = f'{handtype} of {self.cards[0]}, kickers: {self.cards[1]}'
            return rep
        elif self.type.name == 'pair':
            rep = f'{self.type.name} of {self.cards[0]}, kickers: {self.cards[1]}'
            return rep
        elif self.type.name == 'high_card':
            handtype = ''.join(self.type.name.split('_'))
            rep = f'{handtype} of {self.cards[0]}, kickers: {self.cards[1]}'
            return rep

    @staticmethod
    def check_straight_flush(cards):
        """
        Checks for the best straight flush in a list of cards (may be more than just 5)

        :param cards: A list of playing cards.
        :type: list

        :return: None if no straight flush is found, else the value of the top card.
        :return type: Tuple
        """
        cards.sort(reverse=True)
        vals = [(c.get_value(), c.suit.name) for c in cards] \
               + [(1, c.suit.name) for c in cards if c.get_value() == 14]  # Add the aces!
        for c in cards:  # Starting point (high card)
            # Check if we have the value - k in the set of cards:
            found_straight = True
            for k in range(1, 5):
                if (c.get_value() - k, c.suit.name) not in vals:
                    found_straight = False
                    break
            if found_straight:
                return c.get_value()

    @staticmethod
    def check_four_of_a_kind(cards):
        """Check for the best four of a kind and highest single card and returns them

        :param cards: A list of playing cards.
        :type: list

        :return: None if no four of a kind is found, else the value of the four of a kind and the highest remaining card
        :return type: tuple
            """
        vals = [c.get_value() for c in cards]
        vals.sort(reverse=True)
        count_vals = Counter(vals)
        potential_four = count_vals.most_common(1)
        # Kollar om det finns fyra lika av samma kort, potential four = [(val, antal)]
        if potential_four[0][1] == 4:
            four = potential_four[0][0]
            # plockar fram det sista kortet som ??r h??gst
            if vals[0] == four:
                one = vals[4]
                return four, one
            else:
                one = vals[0]
                return four, one

    @staticmethod
    def check_full_house(cards):
        """
        Checks for the best full house in a list of cards (may be more than just 5)

        :param cards: A list of playing cards
        :type: list

        :return: None if no full house is found, else a tuple of the values of the triple and pair.
        :return type: tuple
        """
        value_count = Counter()
        for c in cards:
            value_count[c.get_value()] += 1
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

    @staticmethod
    def check_flush(cards):
        """Check for the best flush out of the given list

        :param cards: A list of playing cards.
        :type: list

        :return: None if no flush is found, else the highest card in the flush
        :return type: tuple
        """
        cards = [(c.get_value(), c.suit.name) for c in cards]
        # suit=[c.suit.name for c in cards]
        # card=[c.get_value() for c in cards]
        suit = []
        card = []
        for element in cards:
            suit.append(element[1])
            card.append(element[0])
        suitt, count = zip(*Counter(suit).most_common(1))
        caaard = []
        for index in cards:
            if suitt[0] in index:
                caaard.append(index[0])

        if count[0] >= 5:
            caaard.sort(reverse=True)
            return caaard[0:5]

    @staticmethod
    def check_straight(cards):
        """Checks for the best straight flush in a list of cards (may be more than just 5)
        :param cards: A list of playing cards.
        :type: list

        :return: None if no straight is found, else the value of the top card.
        :return type: tuple
        """
        cards.sort()
        vals = [c.get_value() for c in cards] \
               + [1 for c in cards if c.get_value() == 14]  # Add the aces!
        for c in reversed(cards):  # Starting point (high card)
            # Check if we have the value - k in the set of cards:
            found_straight = True
            for k in range(1, 5):
                if c.get_value() - k not in vals:
                    found_straight = False
                    break

            if found_straight:
                return c.get_value()

    @staticmethod
    def check_three_of_a_kind(cards):
        """Check for the best three of a kind of the given list

        :param cards: A list of playing cards.
        :type: list
        :return: None if no three of a kind is found, else the highest flush
        :return type: tuple
        """
        vals = [c.get_value() for c in cards]
        counted_cards = Counter(vals)
        most_common, count = zip(*counted_cards.most_common(1))
        if count[0] == 3:
            three = most_common[0]
            del counted_cards[three]
            cards = sorted(counted_cards.keys(), reverse=True)
            return three, cards[0:2]

    @staticmethod
    def check_two_pair(cards):
        """Check for the best flush out of the given list

        :param cards: A list of playing cards.
        :type: list
        :return: None if no two pair is found, else the value of the cards in each pair and the highest remaining card
        :return type: tuple
        """
        vals = [c.get_value() for c in cards]
        vals.sort(reverse=True)
        count_vals = Counter(vals)
        potential_pairs = count_vals.most_common(2)
        # Kollar om det finns tv?? lika av samma kort, potential pair = [(val, antal)]
        if potential_pairs[0][1] == 2 and potential_pairs[1][1] == 2:
            pairs = [potential_pairs[0][0], potential_pairs[1][0]]
            del count_vals[pairs[0]]
            del count_vals[pairs[1]]
            count_vals = sorted(count_vals.elements(), reverse=True)
            one = count_vals[0]
            return pairs, one

    @staticmethod
    def check_pair(cards):
        """Check for the best pair out of the given list

        :param cards: A list of playing cards.
        :type: list

        :return: None of no pair is found, else the value of the highest pair and value of the highest three remaining
        cards.
        :return type: tuple
        """
        vals = [c.get_value() for c in cards]
        count_vals = Counter(vals)
        potential_pair = count_vals.most_common(1)
        #Kollar om det finns tv?? lika av samma kort, potential pair = [(val, antal)]
        if potential_pair[0][1] == 2:
            pair = potential_pair[0][0]
            del count_vals[pair]
            count_vals = sorted(count_vals.elements(), reverse=True)
            ones = count_vals[0:3]
            return pair, ones

    @staticmethod
    def check_high_card(cards):
        """Check for the highest card out of the given list

        :param cards: A list of playing cards.
        :type: list

        :return: The 5 best cards out of the list in descending order.
        :return type: tuple
        """
        vals = [c.get_value() for c in cards]
        vals.sort(reverse=True)
        high_card = vals[0]
        return high_card, vals[1:5]

