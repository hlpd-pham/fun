import pytest
from card import Card, Suite
from game_evaluator import GameEvaluator, HandResult


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
    result = GameEvaluator()._get_pair_cards(hand_cards)
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
    result = GameEvaluator()._get_pair_cards(hand_cards)
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
    result = GameEvaluator()._get_two_pair_cards(hand_cards)
    assert len(result) == 4


def test_two_pairs_happy_path_return_0_cards():
    """only 1 pair"""
    hand_cards = [
        Card(1, Suite.HEART),
        Card(1, Suite.CLUB),
        Card(3, Suite.HEART),
        Card(9, Suite.CLUB),
        Card(4, Suite.HEART),
        Card(5, Suite.HEART),
        Card(6, Suite.HEART),
    ]
    result = GameEvaluator()._get_two_pair_cards(hand_cards)
    assert len(result) == 0


def test_two_pairs_happy_path_return_0_cards_3_of_a_kind():
    """only 1 pair"""
    hand_cards = [
        Card(1, Suite.HEART),
        Card(1, Suite.CLUB),
        Card(1, Suite.SPADE),
        Card(9, Suite.CLUB),
        Card(4, Suite.HEART),
        Card(5, Suite.HEART),
        Card(6, Suite.HEART),
    ]
    result = GameEvaluator()._get_two_pair_cards(hand_cards)
    assert len(result) == 0


def test_two_pairs_sad_path_0_pair():
    hand_cards = [
        Card(1, Suite.HEART),
        Card(2, Suite.CLUB),
        Card(3, Suite.SPADE),
        Card(9, Suite.CLUB),
        Card(4, Suite.HEART),
        Card(5, Suite.HEART),
        Card(6, Suite.HEART),
    ]
    result = GameEvaluator()._get_two_pair_cards(hand_cards)
    assert len(result) == 0


def test_three_of_a_kind_happy_path():
    """classic happy path hand"""
    hand_cards = [
        Card(3, Suite.HEART),
        Card(3, Suite.CLUB),
        Card(3, Suite.SPADE),
        Card(9, Suite.CLUB),
        Card(4, Suite.HEART),
        Card(5, Suite.HEART),
        Card(6, Suite.HEART),
    ]
    result = GameEvaluator()._get_three_of_a_kind_cards(hand_cards)
    assert len(result) == 3


def test_three_of_a_kind_sad_path():
    hand_cards = [
        Card(3, Suite.HEART),
        Card(3, Suite.CLUB),
        Card(2, Suite.SPADE),
        Card(9, Suite.CLUB),
        Card(4, Suite.HEART),
        Card(5, Suite.HEART),
        Card(6, Suite.HEART),
    ]
    result = GameEvaluator()._get_three_of_a_kind_cards(hand_cards)
    assert len(result) == 0


def test_straight_happy_path_normal():
    hand_cards = [
        Card(3, Suite.HEART),
        Card(4, Suite.CLUB),
        Card(5, Suite.SPADE),
        Card(6, Suite.CLUB),
        Card(7, Suite.HEART),
        Card(10, Suite.HEART),
        Card(11, Suite.HEART),
    ]
    expected = [
        Card(3, Suite.HEART),
        Card(4, Suite.CLUB),
        Card(5, Suite.SPADE),
        Card(6, Suite.CLUB),
        Card(7, Suite.HEART),
    ]
    result = GameEvaluator()._get_straight_cards(hand_cards)
    assert expected == result


def test_straight_happy_path_higher_straight():
    hand_cards = [
        Card(3, Suite.HEART),
        Card(4, Suite.CLUB),
        Card(5, Suite.SPADE),
        Card(6, Suite.CLUB),
        Card(7, Suite.HEART),
        Card(8, Suite.HEART),
        Card(11, Suite.HEART),
    ]
    expected = [
        Card(4, Suite.CLUB),
        Card(5, Suite.SPADE),
        Card(6, Suite.CLUB),
        Card(7, Suite.HEART),
        Card(8, Suite.HEART),
    ]
    result = GameEvaluator()._get_straight_cards(hand_cards)
    assert expected == result


def test_straight_happy_path_broadway():
    hand_cards = [
        Card(1, Suite.HEART),
        Card(4, Suite.CLUB),
        Card(5, Suite.SPADE),
        Card(10, Suite.CLUB),
        Card(11, Suite.HEART),
        Card(12, Suite.HEART),
        Card(13, Suite.HEART),
    ]
    expected = [
        Card(1, Suite.HEART),
        Card(10, Suite.CLUB),
        Card(11, Suite.HEART),
        Card(12, Suite.HEART),
        Card(13, Suite.HEART),
    ]
    result = GameEvaluator()._get_straight_cards(hand_cards)
    assert expected == result


def test_straight_happy_path_broadway_7_cards():
    hand_cards = [
        Card(1, Suite.HEART),
        Card(8, Suite.CLUB),
        Card(9, Suite.SPADE),
        Card(10, Suite.CLUB),
        Card(11, Suite.HEART),
        Card(12, Suite.HEART),
        Card(13, Suite.HEART),
    ]
    expected = [
        Card(1, Suite.HEART),
        Card(10, Suite.CLUB),
        Card(11, Suite.HEART),
        Card(12, Suite.HEART),
        Card(13, Suite.HEART),
    ]
    result = GameEvaluator()._get_straight_cards(hand_cards)
    assert expected == result


def test_straight_happy_path_smallest_straight():
    hand_cards = [
        Card(1, Suite.HEART),
        Card(2, Suite.CLUB),
        Card(3, Suite.SPADE),
        Card(4, Suite.CLUB),
        Card(5, Suite.HEART),
        Card(12, Suite.HEART),
        Card(13, Suite.HEART),
    ]
    expected = [
        Card(1, Suite.HEART),
        Card(2, Suite.CLUB),
        Card(3, Suite.SPADE),
        Card(4, Suite.CLUB),
        Card(5, Suite.HEART),
    ]
    result = GameEvaluator()._get_straight_cards(hand_cards)
    assert expected == result


def test_straight_sad_path_no_straight():
    hand_cards = [
        Card(1, Suite.HEART),
        Card(3, Suite.CLUB),
        Card(3, Suite.SPADE),
        Card(4, Suite.CLUB),
        Card(5, Suite.HEART),
        Card(12, Suite.HEART),
        Card(13, Suite.HEART),
    ]
    expected = []
    result = GameEvaluator()._get_straight_cards(hand_cards)
    assert expected == result


def test_flush_happy_path_normal():
    hand_cards = [
        Card(1, Suite.HEART),
        Card(2, Suite.HEART),
        Card(3, Suite.HEART),
        Card(4, Suite.HEART),
        Card(5, Suite.HEART),
        Card(4, Suite.SPADE),
        Card(5, Suite.SPADE),
    ]
    expected = [
        Card(2, Suite.HEART),
        Card(3, Suite.HEART),
        Card(4, Suite.HEART),
        Card(5, Suite.HEART),
        Card(1, Suite.HEART),
    ]
    result = GameEvaluator()._get_flush_cards(hand_cards)
    assert expected == result


def test_flush_happy_path_6_cards_flush():
    hand_cards = [
        Card(1, Suite.HEART),
        Card(2, Suite.HEART),
        Card(3, Suite.HEART),
        Card(4, Suite.HEART),
        Card(5, Suite.HEART),
        Card(13, Suite.HEART),
        Card(5, Suite.SPADE),
    ]
    expected = [
        Card(3, Suite.HEART),
        Card(4, Suite.HEART),
        Card(5, Suite.HEART),
        Card(13, Suite.HEART),
        Card(1, Suite.HEART),
    ]
    result = GameEvaluator()._get_flush_cards(hand_cards)
    assert expected == result


def test_flush_sad_path():
    hand_cards = [
        Card(1, Suite.HEART),
        Card(2, Suite.DIAMOND),
        Card(3, Suite.CLUB),
        Card(4, Suite.HEART),
        Card(5, Suite.HEART),
        Card(4, Suite.SPADE),
        Card(5, Suite.SPADE),
    ]
    expected = []
    result = GameEvaluator()._get_flush_cards(hand_cards)
    assert expected == result


def test_full_house_happy_path_one_pair():
    hand_cards = [
        Card(1, Suite.HEART),
        Card(1, Suite.DIAMOND),
        Card(1, Suite.CLUB),
        Card(2, Suite.HEART),
        Card(2, Suite.HEART),
        Card(4, Suite.SPADE),
        Card(5, Suite.SPADE),
    ]
    expected = [
        Card(1, Suite.HEART),
        Card(1, Suite.DIAMOND),
        Card(1, Suite.CLUB),
        Card(2, Suite.HEART),
        Card(2, Suite.HEART),
    ]
    result = GameEvaluator()._get_full_house_cards(hand_cards)
    assert expected == result


def test_full_house_happy_path_two_pairs():
    hand_cards = [
        Card(1, Suite.HEART),
        Card(1, Suite.DIAMOND),
        Card(1, Suite.CLUB),
        Card(2, Suite.HEART),
        Card(2, Suite.HEART),
        Card(3, Suite.SPADE),
        Card(3, Suite.CLUB),
    ]
    expected = [
        Card(1, Suite.HEART),
        Card(1, Suite.DIAMOND),
        Card(1, Suite.CLUB),
        Card(3, Suite.SPADE),
        Card(3, Suite.CLUB),
    ]
    result = GameEvaluator()._get_full_house_cards(hand_cards)
    assert expected == result


def test_full_house_sad_path_no_trips():
    hand_cards = [
        Card(1, Suite.HEART),
        Card(1, Suite.DIAMOND),
        Card(8, Suite.CLUB),
        Card(2, Suite.HEART),
        Card(2, Suite.HEART),
        Card(4, Suite.SPADE),
        Card(5, Suite.SPADE),
    ]
    expected = []
    result = GameEvaluator()._get_full_house_cards(hand_cards)
    assert expected == result


def test_full_house_sad_path_has_trip_no_pair():
    hand_cards = [
        Card(1, Suite.HEART),
        Card(1, Suite.DIAMOND),
        Card(1, Suite.CLUB),
        Card(2, Suite.HEART),
        Card(8, Suite.HEART),
        Card(4, Suite.SPADE),
        Card(5, Suite.SPADE),
    ]
    expected = []
    result = GameEvaluator()._get_full_house_cards(hand_cards)
    assert expected == result


def test_four_of_a_kind_happy_path():
    hand_cards = [
        Card(1, Suite.HEART),
        Card(1, Suite.DIAMOND),
        Card(1, Suite.CLUB),
        Card(1, Suite.SPADE),
        Card(8, Suite.HEART),
        Card(4, Suite.SPADE),
        Card(5, Suite.SPADE),
    ]
    expected = [
        Card(1, Suite.HEART),
        Card(1, Suite.DIAMOND),
        Card(1, Suite.CLUB),
        Card(1, Suite.SPADE),
    ]
    result = GameEvaluator()._get_four_of_a_kind_cards(hand_cards)
    assert expected == result


def test_four_of_a_kind_sad_path():
    hand_cards = [
        Card(1, Suite.HEART),
        Card(1, Suite.DIAMOND),
        Card(1, Suite.CLUB),
        Card(2, Suite.SPADE),
        Card(8, Suite.HEART),
        Card(4, Suite.SPADE),
        Card(5, Suite.SPADE),
    ]
    expected = []
    result = GameEvaluator()._get_four_of_a_kind_cards(hand_cards)
    assert expected == result


def test_straight_flush_happy_path_smallest_straight():
    hand_cards = [
        Card(1, Suite.DIAMOND),
        Card(2, Suite.DIAMOND),
        Card(3, Suite.DIAMOND),
        Card(4, Suite.DIAMOND),
        Card(5, Suite.DIAMOND),
        Card(11, Suite.CLUB),
        Card(1, Suite.CLUB),
    ]
    expected = [
        Card(2, Suite.DIAMOND),
        Card(3, Suite.DIAMOND),
        Card(4, Suite.DIAMOND),
        Card(5, Suite.DIAMOND),
        Card(1, Suite.DIAMOND),
    ]
    result = GameEvaluator()._get_straight_flush_cards(hand_cards)
    assert expected == result


def test_straight_flush_happy_path():
    hand_cards = [
        Card(1, Suite.HEART),
        Card(2, Suite.HEART),
        Card(3, Suite.HEART),
        Card(4, Suite.HEART),
        Card(5, Suite.HEART),
        Card(6, Suite.SPADE),
        Card(7, Suite.SPADE),
    ]
    expected = [
        Card(2, Suite.HEART),
        Card(3, Suite.HEART),
        Card(4, Suite.HEART),
        Card(5, Suite.HEART),
        Card(1, Suite.HEART),
    ]
    result = GameEvaluator()._get_straight_flush_cards(hand_cards)
    assert expected == result


def test_straight_flush_happy_path_higher_straight():
    hand_cards = [
        Card(1, Suite.HEART),
        Card(2, Suite.HEART),
        Card(3, Suite.HEART),
        Card(4, Suite.HEART),
        Card(5, Suite.HEART),
        Card(6, Suite.HEART),
        Card(7, Suite.SPADE),
    ]
    expected = [
        Card(2, Suite.HEART),
        Card(3, Suite.HEART),
        Card(4, Suite.HEART),
        Card(5, Suite.HEART),
        Card(6, Suite.HEART),
    ]
    result = GameEvaluator()._get_straight_flush_cards(hand_cards)
    assert expected == result


def test_straight_flush_happy_path_royal():
    hand_cards = [
        Card(1, Suite.HEART),
        Card(10, Suite.HEART),
        Card(11, Suite.HEART),
        Card(12, Suite.HEART),
        Card(13, Suite.HEART),
        Card(8, Suite.HEART),
        Card(9, Suite.HEART),
    ]
    expected = [
        Card(10, Suite.HEART),
        Card(11, Suite.HEART),
        Card(12, Suite.HEART),
        Card(13, Suite.HEART),
        Card(1, Suite.HEART),
    ]
    result = GameEvaluator()._get_straight_flush_cards(hand_cards)
    assert expected == result


def test_straight_flush_sad_path_no_flush():
    hand_cards = [
        Card(1, Suite.HEART),
        Card(2, Suite.HEART),
        Card(3, Suite.HEART),
        Card(4, Suite.HEART),
        Card(5, Suite.DIAMOND),
        Card(6, Suite.CLUB),
        Card(7, Suite.SPADE),
    ]
    expected = []
    result = GameEvaluator()._get_straight_flush_cards(hand_cards)
    assert expected == result


def test_straight_flush_sad_path_no_straight():
    hand_cards = [
        Card(1, Suite.HEART),
        Card(2, Suite.HEART),
        Card(3, Suite.HEART),
        Card(4, Suite.HEART),
        Card(8, Suite.DIAMOND),
        Card(10, Suite.CLUB),
        Card(11, Suite.SPADE),
    ]
    expected = []
    result = GameEvaluator()._get_straight_flush_cards(hand_cards)
    assert expected == result


def test_royal_flush_happy_path():
    hand_cards = [
        Card(1, Suite.HEART),
        Card(10, Suite.HEART),
        Card(11, Suite.HEART),
        Card(12, Suite.HEART),
        Card(13, Suite.HEART),
        Card(8, Suite.HEART),
        Card(9, Suite.HEART),
    ]
    expected = [
        Card(10, Suite.HEART),
        Card(11, Suite.HEART),
        Card(12, Suite.HEART),
        Card(13, Suite.HEART),
        Card(1, Suite.HEART),
    ]
    result = GameEvaluator()._get_royal_flush_cards(hand_cards)
    assert expected == result


def test_royal_flush_sad_path():
    hand_cards = [
        Card(1, Suite.HEART),
        Card(10, Suite.HEART),
        Card(11, Suite.SPADE),
        Card(12, Suite.HEART),
        Card(13, Suite.CLUB),
        Card(8, Suite.HEART),
        Card(9, Suite.DIAMOND),
    ]
    expected = []
    result = GameEvaluator()._get_royal_flush_cards(hand_cards)
    assert expected == result


def test_evaluating_hand_bad_input():
    with pytest.raises(
        ValueError, match="there must be 7 cards in hand for evaluation"
    ):
        GameEvaluator().evaluate_hand([])

def test_evaluating_hand_bad_input_duplicate_cards():
    hand_cards = [
        Card(4, Suite.DIAMOND),
        Card(4, Suite.SPADE),
        Card(4, Suite.SPADE),
        Card(7, Suite.CLUB),
        Card(10, Suite.SPADE),
        Card(11, Suite.SPADE),
        Card(1, Suite.CLUB),
    ]
    with pytest.raises(
        ValueError, match="there must be 7 cards in hand for evaluation"
    ):
        GameEvaluator().evaluate_hand(hand_cards)

def test_evaluating_hand_high_card():
    hand_cards = [
        Card(4, Suite.DIAMOND),
        Card(13, Suite.SPADE),
        Card(7, Suite.HEART),
        Card(9, Suite.CLUB),
        Card(10, Suite.SPADE),
        Card(11, Suite.SPADE),
        Card(1, Suite.CLUB),
    ]
    hand_result, _ = GameEvaluator().evaluate_hand(hand_cards)
    assert hand_result == HandResult.HIGH_CARD

def test_evaluating_hand_1_pair():
    hand_cards = [
        Card(4, Suite.DIAMOND),
        Card(4, Suite.SPADE),
        Card(7, Suite.HEART),
        Card(9, Suite.CLUB),
        Card(10, Suite.SPADE),
        Card(11, Suite.SPADE),
        Card(1, Suite.CLUB),
    ]
    hand_result, _ = GameEvaluator().evaluate_hand(hand_cards)
    assert hand_result == HandResult.PAIR

def test_evaluating_hand_2_pairs():
    hand_cards = [
        Card(4, Suite.DIAMOND),
        Card(4, Suite.SPADE),
        Card(7, Suite.HEART),
        Card(7, Suite.CLUB),
        Card(10, Suite.SPADE),
        Card(11, Suite.SPADE),
        Card(1, Suite.CLUB),
    ]
    hand_result, _ = GameEvaluator().evaluate_hand(hand_cards)
    assert hand_result == HandResult.TWO_PAIRS

def test_evaluating_hand_trips():
    hand_cards = [
        Card(4, Suite.DIAMOND),
        Card(4, Suite.SPADE),
        Card(4, Suite.CLUB),
        Card(7, Suite.CLUB),
        Card(10, Suite.SPADE),
        Card(11, Suite.SPADE),
        Card(1, Suite.CLUB),
    ]
    hand_result, _ = GameEvaluator().evaluate_hand(hand_cards)
    assert hand_result == HandResult.THREE_OF_A_KIND

def test_evaluating_hand_straight():
    hand_cards = [
        Card(1, Suite.DIAMOND),
        Card(2, Suite.SPADE),
        Card(3, Suite.CLUB),
        Card(4, Suite.CLUB),
        Card(5, Suite.SPADE),
        Card(11, Suite.SPADE),
        Card(1, Suite.CLUB),
    ]
    hand_result, _ = GameEvaluator().evaluate_hand(hand_cards)
    assert hand_result == HandResult.STRAIGHT

def test_evaluating_hand_flush():
    hand_cards = [
        Card(1, Suite.DIAMOND),
        Card(2, Suite.SPADE),
        Card(3, Suite.CLUB),
        Card(4, Suite.CLUB),
        Card(5, Suite.CLUB),
        Card(11, Suite.CLUB),
        Card(1, Suite.CLUB),
    ]
    hand_result, _ = GameEvaluator().evaluate_hand(hand_cards)
    assert hand_result == HandResult.FLUSH

def test_evaluating_hand_full_house():
    hand_cards = [
        Card(1, Suite.DIAMOND),
        Card(3, Suite.SPADE),
        Card(3, Suite.CLUB),
        Card(3, Suite.DIAMOND),
        Card(5, Suite.CLUB),
        Card(11, Suite.CLUB),
        Card(1, Suite.CLUB),
    ]
    hand_result, _ = GameEvaluator().evaluate_hand(hand_cards)
    assert hand_result == HandResult.FULL_HOUSE

def test_evaluating_hand_four_of_a_kind():
    hand_cards = [
        Card(1, Suite.DIAMOND),
        Card(1, Suite.SPADE),
        Card(1, Suite.CLUB),
        Card(3, Suite.DIAMOND),
        Card(5, Suite.CLUB),
        Card(11, Suite.CLUB),
        Card(1, Suite.HEART),
    ]
    hand_result, _ = GameEvaluator().evaluate_hand(hand_cards)
    assert hand_result == HandResult.FOUR_OF_A_KIND

def test_evaluating_hand_straight_flush():
    hand_cards = [
        Card(1, Suite.DIAMOND),
        Card(2, Suite.DIAMOND),
        Card(3, Suite.DIAMOND),
        Card(4, Suite.DIAMOND),
        Card(5, Suite.DIAMOND),
        Card(11, Suite.CLUB),
        Card(1, Suite.CLUB),
    ]
    hand_result, _ = GameEvaluator().evaluate_hand(hand_cards)
    assert hand_result == HandResult.STRAIGHT_FLUSH

def test_evaluating_hand_royal():
    hand_cards = [
        Card(1, Suite.DIAMOND),
        Card(10, Suite.DIAMOND),
        Card(11, Suite.DIAMOND),
        Card(12, Suite.DIAMOND),
        Card(13, Suite.DIAMOND),
        Card(11, Suite.CLUB),
        Card(1, Suite.CLUB),
    ]
    hand_result, _ = GameEvaluator().evaluate_hand(hand_cards)
    assert hand_result == HandResult.ROYAL_FLUSH
