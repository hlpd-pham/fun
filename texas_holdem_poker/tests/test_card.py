from card import Card, Suite


def test_card_init():
    """init card and assert face value of regular cards"""
    card = Card(10, Suite.HEART)
    assert card is not None and card.suite == Suite.HEART and card.value == 10
    assert str(card) == "Card(10, Suite.HEART)"


def test_special_card():
    """init card and assert face value of special cards"""
    card = Card(1, Suite.HEART)
    assert card is not None and card.suite == Suite.HEART and card.value == 1
    assert str(card) == "Card(Ace, Suite.HEART)"

    card = Card(13, Suite.SPADE)
    assert card is not None and card.suite == Suite.SPADE and card.value == 13
    assert str(card) == "Card(King, Suite.SPADE)"
