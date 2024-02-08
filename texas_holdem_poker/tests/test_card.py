from card import Card, Suite

def test_card_init():
    card = Card(Suite.HEART, 10)
    assert card is not None and card.suite == Suite.HEART and card.value == 10
    assert str(card) == 'Card(10, Suite.HEART)'

def test_special_card():
    card = Card(Suite.HEART, 1)
    assert card is not None and card.suite == Suite.HEART and card.value == 1
    assert str(card) == 'Card(Ace, Suite.HEART)'

    card = Card(Suite.SPADE, 13)
    assert card is not None and card.suite == Suite.SPADE and card.value == 13
    assert str(card) == 'Card(King, Suite.SPADE)'

