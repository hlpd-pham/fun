from card import Card, Suite


def test_card_init():
    card = Card(10, Suite.HEART)
    assert card is not None and card.suite == Suite.HEART and card.value == 10
    assert str(card) == "Card(10, Suite.HEART)"


def test_special_card():
    card = Card(1, Suite.HEART)
    assert card is not None and card.suite == Suite.HEART and card.value == 1
    assert str(card) == "Card(Ace, Suite.HEART)"

    card = Card(13, Suite.SPADE)
    assert card is not None and card.suite == Suite.SPADE and card.value == 13
    assert str(card) == "Card(King, Suite.SPADE)"
