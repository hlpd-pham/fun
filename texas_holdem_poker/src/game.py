import logging
import random
from enum import Enum
from typing import List

from card import Card, CardDealAmount
from constants import ALL_CARDS
from game_evaluator import GameEvaluator
from utils.strings import to_string


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
        deck_hash = {card.get_card_value_suite(): card for card in deck}
        return deck, deck_hash

    def evaluate_hand(
        self, all_player_cards: List[Card]
    ) -> tuple[HandResult, List[Card]]:
        if len(set(all_player_cards)) != 7:
            err_message = f"there must be 7 cards in hand for evaluation, found: {to_string(all_player_cards)}"
            logging.error(err_message)
            raise ValueError(err_message)
        hand_result, result_cards = HandResult.HIGH_CARD, []
        pair_cards = GameEvaluator.get_pair_cards(all_player_cards)
        if pair_cards:
            hand_result, result_cards = HandResult.PAIR, pair_cards

        two_pair_cards = GameEvaluator.get_two_pair_cards(all_player_cards)
        if two_pair_cards:
            hand_result, result_cards = (HandResult.TWO_PAIRS, two_pair_cards)

        three_of_a_kind_cards = GameEvaluator.get_three_of_a_kind_cards(
            all_player_cards
        )
        if three_of_a_kind_cards:
            hand_result, result_cards = (
                HandResult.THREE_OF_A_KIND,
                three_of_a_kind_cards,
            )

        straight_cards = GameEvaluator.get_straight_cards(all_player_cards)
        if straight_cards:
            hand_result, result_cards = (HandResult.STRAIGHT, straight_cards)

        flush_cards = GameEvaluator.get_flush_cards(all_player_cards)
        if flush_cards:
            hand_result, result_cards = HandResult.FLUSH, flush_cards

        full_house_cards = GameEvaluator.get_full_house_cards(all_player_cards)
        if full_house_cards:
            hand_result, result_cards = (HandResult.FULL_HOUSE, full_house_cards)

        four_of_a_kind_cards = GameEvaluator.get_four_of_a_kind_cards(all_player_cards)
        if four_of_a_kind_cards:
            hand_result, result_cards = (
                HandResult.FOUR_OF_A_KIND,
                four_of_a_kind_cards,
            )

        straight_flush_cards = GameEvaluator.get_straight_flush_cards(all_player_cards)
        if straight_flush_cards:
            hand_result, result_cards = (
                HandResult.STRAIGHT_FLUSH,
                straight_flush_cards,
            )

        royal_flush_cards = GameEvaluator.get_royal_flush_cards(all_player_cards)
        if royal_flush_cards:
            hand_result, result_cards = (HandResult.ROYAL_FLUSH, royal_flush_cards)

        if hand_result != HandResult.HIGH_CARD:
            return hand_result, result_cards

        sorted_cards = sorted(all_player_cards, key=lambda card: card.value)
        highest_card = sorted_cards[-1] if sorted_cards[0] != 1 else sorted_cards[0]
        return HandResult.HIGH_CARD, [highest_card]

    def _deal_card(
        self, announcement: str, dealing_type: CardDealAmount, is_show=False
    ) -> List[Card]:
        logging.info(announcement)
        cards_dealt: List[Card] = random.sample(self.deck, dealing_type.value)
        if self._debug or is_show:
            logging.info([str(c) for c in cards_dealt])
        for card in cards_dealt:
            if card.get_card_value_suite() not in self.deck_hash:
                raise ValueError(f"card is not in deck: {card} ")
            del self.deck_hash[card.get_card_value_suite()]
        self.deck = list(self.deck_hash.values())
        logging.info(f"cards type {type(self.deck[0])}")
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
