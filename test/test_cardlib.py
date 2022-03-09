#from enum import Enum
import pytest
from cardlib import *
# This test assumes you call your suit class "Suit" and the suits "Hearts and  "Spades"


def test_cards():
    h5 = NumberedCard(4, Suit.Hearts)
    assert isinstance(h5.suit, Enum)
    assert isinstance(h5, PlayingCard)
    assert issubclass(NumberedCard, PlayingCard)
    sk = KingCard(Suit.Spades)

    assert issubclass(KingCard, PlayingCard)
    assert isinstance(sk.suit, Enum)
    assert isinstance(sk, PlayingCard)
    assert sk.get_value() == 13 #checks value of card

    assert h5 == h5
    assert h5 < sk
    with pytest.raises(TypeError):
        pc = PlayingCard(Suit.Clubs)
    with pytest.raises(TypeError):
        nc= NumberedCard(Suit.Hearts)
    with pytest.raises(TypeError):
        qc= QueenCard(10, Suit.Hearts)

    cj = JackCard(Suit.Clubs)
    assert isinstance(cj.suit, Enum)
    assert isinstance(cj, PlayingCard)
    assert issubclass(JackCard, PlayingCard)
    assert cj.get_value() == 11
    hq = QueenCard(Suit.Hearts)
    assert isinstance(hq.suit, Enum)
    assert isinstance(hq, PlayingCard)
    assert issubclass(QueenCard, PlayingCard)
    assert hq.get_value() == 12
    sk = KingCard(Suit.Spades)
    assert issubclass(KingCard, PlayingCard)
    assert isinstance(sk.suit, Enum)
    assert isinstance(sk, PlayingCard)
    assert sk.get_value() == 13  # checks value of card
    da = AceCard(Suit.Diamonds)
    assert isinstance(da.suit, Enum)
    assert isinstance(da, PlayingCard)
    assert issubclass(AceCard, PlayingCard)
    assert da.get_value() == 14

    #checks operators between different cards
    assert h5 == h5
    assert h5 < sk
    assert da > hq
    assert hq > cj
    assert hq < sk
    assert not cj == hq
    assert da.get_value() != 13

    with pytest.raises(TypeError):
        pc = PlayingCard(Suit.Clubs)
    with pytest.raises(TypeError):
        nc= NumberedCard(Suit.Hearts)
    with pytest.raises(TypeError):
        qc= QueenCard(10, Suit.Hearts)

    assert str(h5) == "4 of Hearts"    #check if it prints a card in a nice way,
    assert str(cj) == "Jack of Clubs"
    assert issubclass(PlayingCard, abc.ABC)

    # Checks Enum, if Clubs is > Hearts
    assert isinstance(h5, PlayingCard)
    assert isinstance(h5, NumberedCard)
    c5 = NumberedCard(4, Suit.Clubs)
    assert c5.get_value() == 4
    assert h5 < c5
    assert isinstance(c5.suit, Enum)

# This test assumes you call your shuffle method "shuffle" and the method to draw a card "draw"
def test_deck():
    d = StandardDeck()
    c1 = d.draw()        # test to draw card
    c2 = d.draw()
    assert not c1 == c2  # checks if the cards are unique
    d2 = StandardDeck()
    d2.shuffle()         # checks the shuffle method
    c3 = d2.draw()
    c4 = d2.draw()
    assert d.deck is not d2.deck # the probability that the decks are sorted in the exact same manner are almost unlikely
    assert len(d.deck) == len(d2.deck)
    assert not ((c3, c4) == (c1, c2))
    d3 = StandardDeck()
    cards = []
    for c in range(52):   # Checks if all 52 cards in deck are unique
        new_card = d3.draw()
        assert new_card not in cards
        cards.append(new_card)

    assert not d3.deck  #check that the deck is empty
    assert isinstance(d, StandardDeck)
    assert isinstance(d2.draw(), PlayingCard)

    # Check shuffle
    d = StandardDeck()
    d2 = StandardDeck()
    d.shuffle()
    assert d2.deck != d.deck

# This test builds on the assumptions above and assumes you store the cards in the hand in the list "cards",
# and that your sorting method is called "sort" and sorts in increasing order
def test_hand():
    h = Hand()
    assert len(h.cards) == 0
    d = StandardDeck()
    d.shuffle()
    h.add_card(d.draw())  # checks if we can add card to the deck
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    assert len(h.cards) == 5
    h.sort()
    for i in range(4):
        assert h.cards[i] < h.cards[i + 1] or h.cards[i] == h.cards[i + 1]
    cards = h.cards.copy()
    h.drop_cards([3, 0, 1])
    assert len(h.cards) == 2
    assert h.cards[0] == cards[2]
    assert h.cards[1] == cards[4]
    h2 = Hand()
    h2.add_card(d.draw())
    h2.add_card(d.draw())
    h2.add_card(d.draw())
    h2.add_card(d.draw())
    h2.add_card(d.draw())
    cards = h2.cards.copy()
    h2.drop_cards([2, 1, 4])
    assert h2.cards[0] == cards[0]
    assert h2.cards[1] == cards[3]

    '''Testing if a certain cards gives a specific handtype '''

    cl2 = [KingCard(Suit.Hearts), QueenCard(Suit.Hearts), JackCard(Suit.Hearts), NumberedCard(10, Suit.Hearts),
           NumberedCard(9, Suit.Hearts), NumberedCard(2, Suit.Spades)]
    assert PokerHand.check_straight_flush(cl2) is not None
    assert PokerHand.check_straight(cl2) is not None
    # Check four of a kind, full house, three of a kind, two pair, pair, high card
    cl3 = [JackCard(Suit.Hearts), JackCard(Suit.Clubs), JackCard(Suit.Spades), JackCard(Suit.Diamonds),
           NumberedCard(5, Suit.Hearts), NumberedCard(5, Suit.Diamonds), NumberedCard(3, Suit.Diamonds)]
    assert PokerHand.check_four_of_a_kind(cl3) is not None
    assert PokerHand.check_full_house(cl3) is not None
    cl3.pop(0)
    assert PokerHand.check_three_of_a_kind(cl3) is not None
    cl3.pop(0)
    assert PokerHand.check_two_pair(cl3) is not None
    assert PokerHand.check_pair(cl3) is not None
    assert PokerHand.check_high_card(cl3) is not None

    h5 = Hand()
    h5.add_card(AceCard(Suit.Hearts))
    h5.add_card(JackCard(Suit.Clubs))
    # Check if you can send in an empty list
    h6 = h5
    haj = h6.best_poker_hand()
    assert isinstance(haj, PokerHand)
    assert isinstance(h6, Hand)

    # Checks sort and if drop_cards drops the expected cards
    h5.add_card(KingCard(Suit.Spades))
    h5.sort()
    h5.drop_cards([0, 2])
    assert len(h5.cards) == 1
    assert isinstance(h5.cards[0], KingCard)
    assert not isinstance(h5.cards[0], AceCard)


# This test builds on the assumptions above. Add your type and data for the commented out tests
# and uncomment them!
def test_pokerhands():
    h1 = Hand()
    h1.add_card(QueenCard(Suit.Diamonds))
    h1.add_card(KingCard(Suit.Hearts))
    h2 = Hand()
    h2.add_card(QueenCard(Suit.Hearts))
    h2.add_card(AceCard(Suit.Hearts))
    cl = [NumberedCard(10, Suit.Diamonds), NumberedCard(9, Suit.Diamonds),
          NumberedCard(8, Suit.Clubs), NumberedCard(6, Suit.Spades)]
    ph1 = h1.best_poker_hand(cl)
    assert isinstance(ph1, PokerHand)
    assert ph1.type == Pokerhand_types.high_card
    assert ph1.cards
    ph2 = h2.best_poker_hand(cl)
    assert isinstance(ph2, PokerHand)
    assert ph2.type == Pokerhand_types.high_card
    assert ph2.cards
    assert ph1 < ph2                    # test if the operators works between different hands
    cl.pop(0)
    cl.append(QueenCard(Suit.Spades))
    cl.append(KingCard(Suit.Clubs))
    cl.append(AceCard(Suit.Diamonds))
    ph3 = h1.best_poker_hand(cl)
    ph4 = h2.best_poker_hand(cl)
    assert isinstance(ph3, PokerHand)
    assert ph3.type == Pokerhand_types.two_pair
    assert ph3.cards
    assert isinstance(ph4, PokerHand)
    assert ph4.type == Pokerhand_types.two_pair
    assert ph4.cards
    assert ph3 < ph4
    assert ph1 < ph2

    cl = [JackCard(Suit.Diamonds), AceCard(Suit.Diamonds), KingCard(Suit.Diamonds), NumberedCard(3, Suit.Spades), NumberedCard(7, Suit.Diamonds)]
    ph5 = h1.best_poker_hand(cl)
    assert isinstance(ph5, PokerHand)
    assert ph5.type is Pokerhand_types.flush
    assert ph5.cards
    h3 = Hand()
    h3.add_card(KingCard(Suit.Spades))
    h3.add_card(NumberedCard(9, Suit.Clubs))
    ph6 = h3.best_poker_hand(cl)
    h4 = Hand()
    h4.add_card(NumberedCard(3, Suit.Clubs))
    h4.add_card(NumberedCard(3, Suit.Hearts))
    ph7 = h4.best_poker_hand(cl)
    assert isinstance(ph6, PokerHand)
    assert ph6.type is Pokerhand_types.pair
    assert ph6.cards
    assert ph5 > ph6
        # test if a random hand is a specific hand
    assert isinstance(ph7, PokerHand)
    assert ph7.type is Pokerhand_types.three_of_a_kind
    assert ph7.cards
    h5 = Hand()
    cl2 = [NumberedCard(3, Suit.Spades), NumberedCard(3, Suit.Spades), NumberedCard(3, Suit.Spades),
           NumberedCard(3, Suit.Spades), QueenCard(Suit.Spades), AceCard(Suit.Spades), AceCard(Suit.Clubs)]
    ph8 = h5.best_poker_hand(cl2)
    assert isinstance(ph8, PokerHand)
    assert ph8.type is Pokerhand_types.four_of_a_kind
    assert ph8.cards
    h6 = Hand()
    h6.add_card(KingCard(Suit.Spades))
    h6.add_card(NumberedCard(9, Suit.Spades))
    ph9 = h6.best_poker_hand(cl)
    assert isinstance(ph9, PokerHand)
    assert ph9.cards
    assert ph9.type is Pokerhand_types.pair
    assert ph6.cards == ph9.cards
    assert ph6.type == ph9.type
    cl2.pop(0)
    cl2.pop(-1)
    h7= Hand()
    h7.add_card(QueenCard(Suit.Diamonds))
    h7.add_card(NumberedCard(5,Suit.Clubs))
    ph10=h7.best_poker_hand(cl2)
    assert isinstance(ph10, PokerHand)
    assert ph10.cards
    assert ph10.type is Pokerhand_types.full_house
    cl3 = [NumberedCard(3, Suit.Spades), NumberedCard(4, Suit.Spades), NumberedCard(5, Suit.Spades),
           NumberedCard(8, Suit.Diamonds), QueenCard(Suit.Hearts), JackCard(Suit.Clubs)]
    h8=Hand()
    h8.add_card(NumberedCard(6, Suit.Spades))
    h8.add_card(NumberedCard(7, Suit.Spades))
    ph11= h8.best_poker_hand(cl3)
    assert isinstance(ph11, PokerHand)
    assert ph11.cards
    assert ph11.type is Pokerhand_types.straight_flush
    h9=Hand()
    h9.add_card(NumberedCard(9, Suit.Spades))
    h9.add_card(NumberedCard(10, Suit.Hearts))
    ph12= h9.best_poker_hand(cl3)
    assert isinstance(ph12, PokerHand)
    assert ph12.cards
    assert ph12.type is Pokerhand_types.straight

    #all types of existing pokerhands
    assert ph11 > ph8 and ph8 < ph11   #straight flush vs four of a kind
    assert ph8 > ph10 and ph10 < ph8   #four of a kind vs full house
    assert ph10 > ph5 and ph5 < ph10   #full house vs flush
    assert ph5 > ph12 and ph12 < ph5   #flush vs straight
    assert ph12 > ph7 and ph7 < ph12   #straight vs three of a kind
    assert ph7 > ph4 and ph4 < ph7     # three of a kind vs two pair
    assert ph4 > ph6 and ph6 < ph4     #two pair vs pair
    assert ph6 > ph1 and ph1 < ph6     # pair vs high card

    tp = Pokerhand_types(3)
    fl = Pokerhand_types(6)
    assert tp == Pokerhand_types.two_pair
    assert isinstance(tp, Pokerhand_types)
    assert isinstance(tp, IntEnum)
    assert fl > tp

    tk = Pokerhand_types.three_of_a_kind.value
    fk = Pokerhand_types.four_of_a_kind.value
    assert tk < fk
    assert issubclass(Pokerhand_types, IntEnum)

    sf = Pokerhand_types.straight_flush
    s = Pokerhand_types.straight
    assert sf > s

    tp = Pokerhand_types(3)
    fl = Pokerhand_types(6)
    assert tp == Pokerhand_types.two_pair
    assert isinstance(tp, Pokerhand_types)
    assert isinstance(tp, IntEnum)
    assert fl > tp

    tk = Pokerhand_types.three_of_a_kind.value
    fk = Pokerhand_types.four_of_a_kind.value
    assert tk < fk
    assert issubclass(Pokerhand_types, IntEnum)

    sf = Pokerhand_types.straight_flush

    s = Pokerhand_types.straight
    assert sf > s

    sf2 = Pokerhand_types.straight_flush
    assert sf == sf2

