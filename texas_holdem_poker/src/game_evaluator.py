import logging
from collections import defaultdict
from typing import List

from card import Card

class GameEvaluator:
    '''This class always assume player cards have 7 cards to make it simple'''

    @classmethod
    def get_pair_cards(cls, all_player_cards: List[Card]) -> List[Card]:
        value_cards_map = defaultdict(list)
        logging.info(f"player cards: {[str(card) for card in all_player_cards]}")
        for c in all_player_cards:
            value_cards_map[c.value].append(c)
            if len(value_cards_map[c.value]) == 2:
                return value_cards_map[c.value]
        return []

    @classmethod
    def get_two_pair_cards(cls, all_player_cards: List[Card]) -> List[Card]:
        hand_cards = sorted(all_player_cards.copy())
        first_pair_cards = GameEvaluator.get_pair_cards(hand_cards)
        if len(first_pair_cards) == 0:
            return []
        for card in first_pair_cards:
            hand_cards.remove(card)
        second_pair_cards = GameEvaluator.get_pair_cards(hand_cards)
        if len(second_pair_cards) == 0:
            return []
        return first_pair_cards + second_pair_cards

    @classmethod
    def get_three_of_a_kind_cards(cls, all_player_cards: List[Card]) -> List[Card]:
        value_cards_map = defaultdict(list)
        for c in all_player_cards:
            value_cards_map[c.value].append(c)
            if len(value_cards_map[c.value]) == 3:
                return value_cards_map[c.value]
        return []

    @classmethod
    def get_straight_cards(cls, all_player_cards: List[Card]) -> List[Card]:
        """
        only return the highest straight cards
        """
        hand_cards = all_player_cards.copy()
        unique_cards = {}
        for card in hand_cards:
            unique_cards[card.value] = card
        sorted_cards = sorted(unique_cards.values())
        for straight_end_idx in range(len(sorted_cards)-1, len(sorted_cards)-4, -1):
            straight_start_idx = straight_end_idx - 4
            found_straight = True
            for i in range(straight_start_idx, straight_end_idx):
                if not(sorted_cards[i].value + 1 == sorted_cards[i+1].value):
                    found_straight = False
                    break
            if found_straight:
                return sorted_cards[straight_start_idx:straight_end_idx+1]

        potential_broadway_values = [sorted_cards[0].value] + [card.value for card in sorted_cards[-4:]]
        if potential_broadway_values == [1,10,11,12,13]:
            return [sorted_cards[0]] + sorted_cards[-4:]

        return []

    @classmethod
    def get_flush_cards(cls, all_player_cards: List[Card]) -> List[Card]:
        """
        only return the highest flush cards
        """
        hand_cards = sorted(all_player_cards)
        suite_cards_map = defaultdict(list)
        flush_suite = None
        for card in hand_cards:
            suite_cards_map[card.suite].append(card)
            if len(suite_cards_map[card.suite]) >= 5:
                flush_suite = card.suite

        if flush_suite:
            return suite_cards_map[flush_suite][-5:]

        return []

    @classmethod
    def get_full_house_cards(cls, all_player_cards: List[Card]) -> List[Card]:
        hand_cards = all_player_cards.copy()
        three_of_a_kind_cards = cls.get_three_of_a_kind_cards(hand_cards)
        if len(three_of_a_kind_cards) == 0:
            return []
        for c in three_of_a_kind_cards:
            hand_cards.remove(c)
        pair_cards = cls.get_pair_cards(hand_cards)
        if len(pair_cards) == 0:
            return []
        return three_of_a_kind_cards + pair_cards

    @classmethod
    def get_four_of_a_kind_cards(cls, all_player_cards: List[Card]) -> List[Card]:
        value_cards_map = defaultdict(list)
        for c in all_player_cards:
            value_cards_map[c.value].append(c)
            if len(value_cards_map[c.value]) == 4:
                return value_cards_map[c.value]
        return []

    @classmethod
    def get_straight_flush_cards(cls, all_player_cards: List[Card]) -> List[Card]:
        straight_cards = sorted(
            GameEvaluator.get_straight_cards(all_player_cards),
            key=lambda card: (card.value, card.suite),
        )
        flush_cards = sorted(
            GameEvaluator.get_flush_cards(all_player_cards),
            key=lambda card: (card.value, card.suite),
        )
        if straight_cards != flush_cards:
            return []
        return straight_cards

    @classmethod
    def get_royal_flush_cards(cls, all_player_cards: List[Card]) -> List[Card]:
        straight_flush_cards = GameEvaluator.get_straight_flush_cards(all_player_cards)
        straight_flush_card_values = set([c.value for c in straight_flush_cards])

        ROYAL_FLUSH_VALUES = set([10, 11, 12, 13, 1])
        if ROYAL_FLUSH_VALUES <= straight_flush_card_values:
            return straight_flush_cards
        return []
