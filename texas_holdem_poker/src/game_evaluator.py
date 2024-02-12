from collections import defaultdict
from typing import List

from card import Card


class GameEvaluator:

    @classmethod
    def get_pair_cards(cls, all_player_cards: List[Card]) -> List[Card]:
        value_cards_map = defaultdict(list)
        for c in all_player_cards:
            value_cards_map[c.value].append(c)
            if len(value_cards_map[c.value]) == 2:
                return value_cards_map[c.value]
        return []

    @classmethod
    def get_two_pair_cards(cls, all_player_cards: List[Card]) -> List[Card]:
        hand_cards = sorted(all_player_cards.copy(), key=lambda card: card.value)
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

        2 4 5 6 7 8 10
        """
        hand_cards = sorted(all_player_cards, key=lambda card: card.value)
        longest_start, longest_end = 0, 1
        left = 0
        for right in range(1, len(hand_cards)):
            if hand_cards[right - 1].value < hand_cards[right].value - 1:
                if right - left >= longest_end - longest_start:
                    longest_start, longest_end = left, right

        # broadway
        if (
            longest_end - longest_start + 1 == 4
            and hand_cards[-1].value == 13
            and hand_cards[0].value == 1
        ):
            return [hand_cards[0]] + hand_cards[longest_start : longest_end + 1]

        # normal straight
        if longest_end - longest_start + 1 == 5:
            return hand_cards[longest_start : longest_end + 1]

        return []

    @classmethod
    def get_flush_cards(cls, all_player_cards: List[Card]) -> List[Card]:
        """
        only return the highest flush cards
        """
        hand_cards = sorted(all_player_cards, key=lambda card: card.value)
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
