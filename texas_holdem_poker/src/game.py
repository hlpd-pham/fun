import logging
import random
from typing import List

from card import Card, CardDealAmount
from constants import ALL_CARDS
from game_evaluator import GameEvaluator, HandResult
from utils.strings import to_string


class Game:

    def __init__(self, num_players=1, debug=False):
        if num_players < 0 or num_players > 8:
            raise ValueError(f"Invalid number of players: {num_players}")
        self._debug: bool = debug
        self.players: List[List[Card]] = []
        self.board: List[Card] = []
        self.deck, self.deck_hash = self._get_deck()
        self._dealing_to_players(num_players)
        self.game_evaluator = GameEvaluator()

    def _get_deck(self):
        deck = ALL_CARDS.copy()
        random.shuffle(deck)
        deck_hash = {card.get_card_value_suite(): card for card in deck}
        return deck, deck_hash

    def evaluate_hand(
        self, all_player_cards: List[Card]
    ) -> tuple[HandResult, List[Card]]:
        logging.info(f"evaluating hand: {to_string(all_player_cards)}")
        return self.game_evaluator.evaluate_hand(all_player_cards)

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

    def find_winners(self):
        pass
        # scores_players_map = {}
        # for idx, player_hand in enumerate(players):
        #     score, hand
            


