from card import Card, Suite
from game_evaluator import GameEvaluator


def test_get_one_pair_happy_path_return_2_cards():
    hand_cards = [
        Card(1, Suite.HEART),
        Card(1, Suite.CLUB),
        Card(2, Suite.HEART),
        Card(3, Suite.HEART),
        Card(4, Suite.HEART),
        Card(5, Suite.HEART),
        Card(6, Suite.HEART),
    ]
    result = GameEvaluator.get_pair_cards(hand_cards)
    assert len(result) == 2


def test_get_one_pair_sad_path_return_0_cards():

    hand_cards = [
        Card(1, Suite.HEART),
        Card(10, Suite.CLUB),
        Card(2, Suite.HEART),
        Card(3, Suite.HEART),
        Card(4, Suite.HEART),
        Card(5, Suite.HEART),
        Card(6, Suite.HEART),
    ]
    result = GameEvaluator.get_pair_cards(hand_cards)
    assert len(result) == 0


def test_two_pairs_happy_path_return_4_cards():
    hand_cards = [
        Card(1, Suite.HEART),
        Card(1, Suite.CLUB),
        Card(2, Suite.HEART),
        Card(2, Suite.CLUB),
        Card(4, Suite.HEART),
        Card(5, Suite.HEART),
        Card(6, Suite.HEART),
    ]
    result = GameEvaluator.get_two_pair_cards(hand_cards)
    assert len(result) == 4

def test_two_pairs_happy_path_return_0_cards():
    '''only 1 pair, return 0 cards'''
    hand_cards = [
        Card(1, Suite.HEART),
        Card(1, Suite.CLUB),
        Card(3, Suite.HEART),
        Card(9, Suite.CLUB),
        Card(4, Suite.HEART),
        Card(5, Suite.HEART),
        Card(6, Suite.HEART),
    ]
    result = GameEvaluator.get_two_pair_cards(hand_cards)
    assert len(result) == 0
