import logging
import random
from typing import Dict, List

from card import Card, CardDealAmount
from constants import ALL_CARDS
from game_evaluator import GameEvaluator
from player import Player
from utils.strings import to_string


class Game:

    def __init__(self, num_players=1, debug=False):
        if num_players < 0 or num_players > 8:
            raise ValueError(f"Invalid number of players: {num_players}")
        self.game_evaluator = GameEvaluator()
        self._debug: bool = debug
        self.players: Dict[str, Player] = {}
        self.board: List[Card] = []
        self.deck, self.deck_hash = self._get_deck()
        self._poplulate_players(num_players)

    def _get_deck(self):
        deck = ALL_CARDS.copy()
        random.shuffle(deck)
        deck_hash = {card.get_card_value_suite(): card for card in deck}
        return deck, deck_hash

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

    def _poplulate_players(self, num_players) -> None:
        logging.info(f'dealing cards to {num_players} players')
        for _ in range(num_players):
            new_player = Player()
            player_cards = self._deal_card(
                f"dealing cards for player {new_player.id}", CardDealAmount.PLAYER
            )
            new_player.cards = player_cards
            self.players[new_player.id] = new_player


    def dealing_to_board(self, dealing_type: CardDealAmount):
        self._deal_card(f"burn 1 for {dealing_type}", CardDealAmount.BURN)
        cards_dealt = self._deal_card(f"{dealing_type}", dealing_type)
        self.board.extend(cards_dealt)

    def evaluating_players(self) -> dict[str, Player]:
        logging.info('evaluating player hands')
        logging.info(f'players: {to_string(self.players)}')
        for player_id in self.players.keys():
            player_cards = self.players[player_id].cards + self.get_board()
            hand_result, _ = self.game_evaluator.evaluate_hand(player_cards)
            self.players[player_id].hand_result = hand_result
            logging.info(f'player_id: {player_id}, player_cards: {to_string(player_cards)}, hand result: {to_string(hand_result)}')
        return self.players


    def get_board(self):
        if self._debug:
            logging.info(f"board cards - {[str(c) for c in self.board]}")
        return self.board

    def find_winners(self):
        '''TODO'''
        pass

