from enum import Enum
import abc
from random import shuffle
from collections import Counter


class PlayingCard(abc.ABC):
    """Parent class for all the different playing cards

    methods
    -------
    get_value
        Abstract method that gives the value of playing card"""

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
    """ A class that creates Numbered playing cards"""
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
    """ A class that creates Jack playing cards"""
    def __init__(self, suit):
        super().__init__(suit)

    def get_value(self):
        return 11

    def __str__(self):
        return f"Jack of {self.suit.name}"

    def __repr__(self):
        return 'Card(%r, %r)' % (self.get_value(), self.suit.name)


class QueenCard(PlayingCard):
    """ A class that creates Queen playing cards"""
    def __init__(self, suit):
        super().__init__(suit)

    def get_value(self):
        return 12

    def __str__(self):
        return f"Queen of {self.suit.name}"

    def __repr__(self):
        return 'Card(%r, %r)' % (self.get_value(), self.suit.name)


class KingCard(PlayingCard):
    """ A class that creates King playing cards"""
    def __init__(self, suit):
        super().__init__(suit)

    def __str__(self):
        return f"King of {self.suit.name}"

    def get_value(self):
        return 13

    def __repr__(self):
        return 'Card(%r, %r)' % (self.get_value(), self.suit.name)


class AceCard(PlayingCard):
    """ A class that creates Ace playing cards"""
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
    """
    A class used to represent a players hand

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
        :param card: A playing card
        """

        self.cards.append(card)

    def drop_cards(self, discards):
        """ Drop the desired cards from the players hand
        :param discards: A list of desired discards
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

    def best_poker_hand(self, table_cards):
        """A method that creates a poker hand object and returns the combination of the 5 best playing cards.
        :param table_cards: A list of the cards on the table.
        :return: A poker hand of the 5 best cards out of the cards on hand and card on the table."""
        all_cards = self.cards
        for tc in table_cards:
            all_cards.append(tc)
        ph = PokerHand(all_cards)
        return ph


class StandardDeck(object):
    """Initializes and creates a deck of all 52 playing cards.
    methods
    -------
    create_deck
       Creates a deck containing all 52 playing cards
    show_deck
      Prints the deck in the command window in the current order
    shuffle
        shuffles the deck
    draw
        draws the top cards of the deck
    """

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
        self.cards = cards
        self.type = 0
        self.check_checks(self.cards)

    def check_checks(self, cards):
        tests = [self.check_straight_flush, self.check_four_of_a_kind, self.check_full_house, self.check_flush,
                 self.check_straight, self.check_three_of_a_kind, self.check_two_pair, self.check_pair, self.check_high_card]
        self.type = 10
        for t in tests:
            self.cards = t(cards)
            self.type -= 1
            if self.cards is None:
                continue
            else:
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

    def __str__(self):
        s = ""
        for c in self.cards:
            s = s + str(c) + '\n'
        return s

    @staticmethod
    def check_straight_flush(cards):
        """
        Checks for the best straight flush in a list of cards (may be more than just 5)
        :param cards: A list of playing cards.
        :return: None if no straight flush is found, else the value of the top card.
        """
        cards.sort()
        vals = [(c.get_value(), c.suit.name) for c in cards] \
               + [(1, c.suit.name) for c in cards if c.get_value() == 14]  # Add the aces!
        for c in reversed(cards):  # Starting point (high card)
            # Check if we have the value - k in the set of cards:
            found_straight = True
            for k in range(1, 5):
                if (c.get_value() - k, c.suit) not in vals:
                    found_straight = False
                    break

            if found_straight:
                return c.get_value()

    @staticmethod
    def check_four_of_a_kind(cards):
        """Check for the best four of a kind and highest single card and returns them
        :param cards: A list of playing cards.
        :return: None if no four of a kind is found, else the value of the four of a kind and the highest remaining card"""
        vals = [c.get_value() for c in cards]
        vals.sort(reverse=True)
        count_vals = Counter(vals)
        potential_four = count_vals.most_common(1)
        # Kollar om det finns fyra lika av samma kort, potential four = [(val, antal)]
        if potential_four[0][1] == 4:
            four = potential_four[0][0]
            # plockar fram det sista kortet som är högst
            if vals[0] != potential_four[0][0]:
                one = vals[0]
                return four, one
            else:
                one = vals[1]
                return four, one

    @staticmethod
    def check_full_house(cards):
        """
        Checks for the best full house in a list of cards (may be more than just 5)
        :param cards: A list of playing cards
        :return: None if no full house is found, else a tuple of the values of the triple and pair.
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
        pass
        """Check for the best flush out of the given list
        :param cards: A list of playing cards.
        :return: None if no flush is found, else the highest card in the flush"""
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
        for index in card:
            if suitt[0] in index:
                caaard.append(index[0])

        if count[0] >= 5:
            caaard.sort(reverse=True)
            return caaard[0:5]

    @staticmethod
    def check_straight(cards):
        """Checks for the best straight flush in a list of cards (may be more than just 5)
        :param cards: A list of playing cards.
        :return: None if no straight is found, else the value of the top card.
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
        :return: None if no three of a kind is found, else the highest flush"""
        vals = [c.get_value() for c in cards]
        counted_cards = Counter(vals)
        most_common, count = zip(*counted_cards.most_common(1))
        if count[0] == 3:
            three = most_common[0]
            cards = counted_cards.elements()
            return three, cards[1:3]

    @staticmethod
    def check_two_pair(cards):
        """Check for the best flush out of the given list
        :param cards: A list of playing cards.
        :return: None if no two pair is found, else the value of the cards in each pair and the highest remaining card"""
        vals = [c.get_value() for c in cards]
        vals.sort(reverse=True)
        count_vals = Counter(vals)
        potential_pairs = count_vals.most_common(2)
        # Kollar om det finns två lika av samma kort, potential pair = [(val, antal)]
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
        :return: None of no pair is found, else the value of the highest pair and value of the highest three remaining
        cards. """
        vals = [c.get_value() for c in cards]
        count_vals = Counter(vals)
        potential_pair = count_vals.most_common(1)
        #Kollar om det finns två lika av samma kort, potential pair = [(val, antal)]
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
        :return: The 5 best cards out of the list in descending order. """
        vals = [c.get_value() for c in cards]
        vals.sort(reverse=True)
        high_card = vals[0]
        return high_card, vals[1:5]


d = StandardDeck()
#print(d)
#d.show_deck()
# d.show_deck()
sh = JackCard(Suit.Hearts)
# print(sh.get_value())
# print(Suit.Hearts.value)
# print(Suit.Hearts > Suit.Spades)
h = Hand()

h.add_card(d.draw())
h.add_card(d.draw())


T_cards = [NumberedCard(10, Suit.Spades), NumberedCard(10, Suit.Diamonds), NumberedCard(10, Suit.Spades), QueenCard(Suit.Hearts), NumberedCard(2, Suit.Hearts), NumberedCard(3, Suit.Spades), NumberedCard(4, Suit.Diamonds), NumberedCard(5, Suit.Diamonds), KingCard(Suit.Spades), KingCard(Suit.Hearts), AceCard(Suit.Hearts), NumberedCard(7, Suit.Clubs)]
K_cards = [NumberedCard(10, Suit.Spades), NumberedCard(10, Suit.Clubs), NumberedCard(10, Suit.Hearts), QueenCard(Suit.Hearts), QueenCard(Suit.Hearts)]

# pok = h.best_poker_hand(K_cards)
# # pok.show_poker_hand()
# print(pok)