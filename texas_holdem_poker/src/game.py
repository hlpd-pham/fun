import logging
import random
from collections import defaultdict
from enum import Enum
from typing import List

from card import Card, CardDealAmount
from constants import ALL_CARDS


class HandResult(Enum):
    ROYAL_FLUSH = 10
    STRAIGHT_FLUSH = 9
    FOUR_OF_A_KIND = 8
    FULL_HOUSE = 7
    FLUSH = 6
    STRAIGHT = 5
    THREE_OF_A_KIND = 4
    TWO_PAIRS = 3
    PAIR = 2
    HIGH_CARD = 1


class Game:

    def __init__(self, num_players=1, debug=False):
        if num_players < 0 or num_players > 8:
            raise ValueError(f"Invalid number of players: {num_players}")
        self._debug: bool = debug
        self.players: List[List[Card]] = []
        self.board: List[Card] = []
        self.deck, self.deck_hash = self._get_deck()
        self._dealing_to_players(num_players)

    def _get_deck(self):
        deck = ALL_CARDS.copy()
        random.shuffle(deck)
        deck_hash = {card.get_card_value_suite(): True for card in deck}
        return deck, deck_hash

    def _get_pair_cards(self, all_player_cards: List[Card]) -> List[Card]:
        return []

    def _get_two_pair_cards(self, all_player_cards: List[Card]) -> List[Card]:
        return []

    def _get_three_of_a_kind_cards(self, all_player_cards: List[Card]) -> List[Card]:
        return []

    def _get_straight_cards(self, all_player_cards: List[Card]) -> List[Card]:
        """
        only return the highest straight cards
        """
        return []

    def _get_flush_cards(self, all_player_cards: List[Card]) -> List[Card]:
        """
        only return the highest flush cards
        """
        return []

    def _get_full_house_cards(self, all_player_cards: List[Card]) -> List[Card]:
        hand_cards = all_player_cards.copy()
        three_of_a_kind_cards = self._get_three_of_a_kind_cards(hand_cards)
        if len(three_of_a_kind_cards) == 0:
            return []
        for c in three_of_a_kind_cards:
            hand_cards.remove(c)
        pair_cards = self._get_pair_cards(hand_cards)
        if len(pair_cards) == 0:
            return []
        return three_of_a_kind_cards + pair_cards

    def _is_four_of_a_kind(self, all_player_cards: List[Card]) -> List[Card]:
        value_cards_map = defaultdict(list)
        for c in all_player_cards:
            value_cards_map[c.value].append(c)
            if len(value_cards_map[c.value]) == 4:
                return value_cards_map[c.value]
        return []

    def _get_straight_flush_cards(self, all_player_cards: List[Card]) -> List[Card]:
        straight_cards = sorted(
            self._get_straight_cards(all_player_cards),
            key=lambda card: (card.value, card.suite),
        )
        flush_cards = sorted(
            self._get_flush_cards(all_player_cards),
            key=lambda card: (card.value, card.suite),
        )
        if straight_cards != flush_cards:
            return []
        return straight_cards

    def _get_royal_flush_cards(self, all_player_cards: List[Card]) -> List[Card]:
        straight_flush_cards = self._get_straight_flush_cards(all_player_cards)
        straight_flush_card_values = set([c.value for c in straight_flush_cards])

        ROYAL_FLUSH_VALUES = set([10, 11, 12, 13, 1])
        if ROYAL_FLUSH_VALUES <= straight_flush_card_values:
            return straight_flush_cards
        return []

    def _evaluate_hand(self, all_player_cards: List[Card]) -> HandResult:
        if self._get_royal_flush_cards(all_player_cards):
            return HandResult.ROYAL_FLUSH

        return HandResult.HIGH_CARD

    def _deal_card(
        self, announcement: str, dealing_type: CardDealAmount, is_show=False
    ) -> List[Card]:
        logging.info(announcement)
        cards_dealt: List[Card] = random.sample(self.deck, dealing_type.value)
        if self._debug or is_show:
            logging.info([str(c) for c in cards_dealt])
        for card in cards_dealt:
            if card.get_card_value_suite() not in self.deck_hash:
                raise ValueError(f"card {card} is not in deck")
            del self.deck_hash[card.get_card_value_suite()]
        self.deck = list(self.deck_hash.keys())
        return cards_dealt

    def _dealing_to_players(self, num_players):
        logging.info("deal cards to players")
        for i in range(num_players):
            player_cards = self._deal_card(
                f"dealing cards for player {i}", CardDealAmount.PLAYER, False
            )
            self.players.append(player_cards)

    def dealing_to_board(self, dealing_type: CardDealAmount):
        self._deal_card(f"burn 1 for {dealing_type}", CardDealAmount.BURN, False)
        cards_dealt = self._deal_card(f"{dealing_type}", dealing_type, False)
        self.board.extend(cards_dealt)

    def get_board(self):
        if self._debug:
            logging.info(f"board cards - {[str(c) for c in self.board]}")
        return self.board
