#from enum import Enum
import pytest
from cardlib import *
# This test assumes you call your suit class "Suit" and the suits "Hearts and  "Spades"

def test_cards():
    h5 = NumberedCard(4, Suit.Hearts)
    assert isinstance(h5.suit, Enum)
    sk = KingCard(Suit.Spades)
    assert sk.get_value() == 13
    assert h5 == h5
    assert h5 < sk
    with pytest.raises(TypeError):
        pc = PlayingCard(Suit.Clubs)
    cj = JackCard(Suit.Clubs)
    da = AceCard(Suit.Diamonds)
    hq = QueenCard(Suit.Hearts)
    assert da > hq
    assert hq > cj
    assert hq.get_value() == 12

    assert da.get_value() != 13
    print(h5)
    assert isinstance(h5, PlayingCard)
    assert isinstance(h5, NumberedCard)
    assert str(h5) == "4 of Hearts"
    assert str(cj) == "Jack of Clubs"


# This test assumes you call your shuffle method "shuffle" and the method to draw a card "draw"
def test_deck():
    d = StandardDeck()
    c1 = d.draw()
    c2 = d.draw()
    assert not c1 == c2
    d2 = StandardDeck()
    d2.shuffle()
    c3 = d2.draw()
    c4 = d2.draw()
    assert not ((c3, c4) == (c1, c2))
    d3 = StandardDeck()
    cards = []
    for c in range(52):  # Checks if all 52 cards in deck are unique
        new_card = d3.draw()
        assert new_card not in cards
        cards.append(new_card)

    assert isinstance(d, StandardDeck)

    assert isinstance(d2.draw(), PlayingCard)



# This test builds on the assumptions above and assumes you store the cards in the hand in the list "cards",
# and that your sorting method is called "sort" and sorts in increasing order
def test_hand():
    h = Hand()
    assert len(h.cards) == 0
    d = StandardDeck()
    d.shuffle()
    h.add_card(d.draw())
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
    # assert PokerHand.check_four_of_a_kind(cl3) is not None
    # assert PokerHand.check_full_house(cl3) is not None
    cl3.pop(0)
    assert PokerHand.check_three_of_a_kind(cl3) is not None
    cl3.pop(0)
    assert PokerHand.check_two_pair(cl3) is not None
    assert PokerHand.check_pair(cl3) is not None
    assert PokerHand.check_high_card(cl3) is not None

    h5 = Hand()
    h5.add_card(AceCard(Suit.Hearts))
    h5.add_card(JackCard(Suit.Clubs))

    assert str(h5) == "Ace of Hearts\nJack of Clubs\n"


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
    # ph1 = h1.best_poker_hand(cl)
    # assert isinstance(ph1, PokerHand)
    # ph2 = h2.best_poker_hand(cl)
    # assert isinstance(ph2, PokerHand)
    # assert ph1 < ph2

    cl.pop(0)
    cl.append(QueenCard(Suit.Spades))
    # ph3 = h1.best_poker_hand(cl)
    # ph4 = h2.best_poker_hand(cl)
    # assert isinstance(ph3, PokerHand)
    # assert isinstance(ph4, PokerHand)
    # assert ph3 < ph4
    # assert ph1 < ph2

    #Check two hand with same type:
    # cl = [JackCard(Suit.Clubs), AceCard(Suit.Spades), KingCard(Suit.Clubs), NumberedCard(3,Suit.Spades)]
    # ph5 = h1.best_poker_hand(cl)
    # assert isinstance(ph5, PokerHand)
    h3 = Hand()
    h3.add_card(KingCard(Suit.Spades))
    h3.add_card(NumberedCard(9, Suit.Clubs))
    # ph6 = h3.best_poker_hand(cl)
    # assert isinstance(ph6, PokerHand)
    # assert ph5 > ph6


    cl2 = [NumberedCard(3, Suit.Spades), NumberedCard(3, Suit.Spades), NumberedCard(3, Suit.Spades),
           NumberedCard(3, Suit.Spades), QueenCard(Suit.Spades)]
    ph7 = h3.best_poker_hand(cl2)
    ph8 = h1.best_poker_hand(cl2)
    print(ph7)   # HUR?!?!?! DENNA ÄR JU INTE ENS KÅK
    print(ph8)  # VARFÖR BLIR DESSA INTE FOUR OF A KIND??
    print(PokerHand.check_four_of_a_kind(cl2))
    #assert ph7.check_four_of_a_kind([])

