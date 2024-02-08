from enum import Enum
import random
from typing import List

from card import Card, CardDealAmount
from constants import ALL_CARDS

class HandResult(Enum):
    ROYAL_FLUSH = 'ROYAL_FLUSH'
    FOUR_OF_A_KIND = 'FOUR_OF_A_KIND'
    FULL_HOUSE = 'FULL_HOUSE'
    FLUSH = 'FLUSH'
    STRAIGHT = 'STRAIGHT'
    THREE_OF_A_KIND = 'THREE_OF_A_KIND'
    TWO_PAIRS = 'TWO_PAIRS'
    PAIR = 'PAIR'
    HIGH_CARD = 'HIGH_CARD'


class Game:
    separators = '---------------'

    def __init__(self, num_players=1, debug=False):
        if num_players < 0 or num_players > 8:
            raise ValueError(f'Invalid number of players: {num_players}')
        self.debug: bool = debug
        self.players: List[List[Card]] = []
        self.board: List[Card] = []
        self.game_cards: List[Card] = ALL_CARDS.copy()
        random.shuffle(self.game_cards)
        self._dealing_to_players(num_players)


    def _is_royal_flush(self, player: List[Card], board: List[Card]):
        royal_flush_values = [10,11,12,13,1]
        all_player_cards = player + board
        all_player_card_values = [c.value for c in all_player_cards]
        all_player_card_suites = [c.suite for c in all_player_cards]


    def _evaluate_hand(self, player: List[Card], board: List[Card]):
        if self._is_royal_flush(player, board):
            return HandResult.ROYAL_FLUSH


    def _deal_card(self, announcement: str, dealing_type: CardDealAmount, is_show=False) -> List[Card]:
        print(announcement, end=' - ')
        cards_dealt = random.sample(self.game_cards, dealing_type.value)
        if self.debug or is_show:
            print([str(c) for c in cards_dealt])
        for c in cards_dealt:
            self.game_cards.remove(c)
        return cards_dealt


    def _dealing_to_players(self, num_players):
        print('deal cards to players')
        for i in range(num_players):
            player_cards = self._deal_card(f"dealing cards for player {i}", CardDealAmount.PLAYER, False)
            self.players.append(player_cards)
        print(Game.separators)

        
    def dealing_to_board(self, dealing_type: CardDealAmount):
        self._deal_card(f'burn 1 for {dealing_type}', CardDealAmount.BURN, False)
        cards_dealt = self._deal_card(f'{dealing_type}', dealing_type, False)
        self.board.extend(cards_dealt)
        print(Game.separators)


    def get_board(self):
        if self.debug:
            print('board cards')
            print([str(c) for c in self.board])
        return self.board





