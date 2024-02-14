import logging
import random
from collections import defaultdict
from typing import Dict, List

from card import Card, CardDealAmount
from constants import ALL_CARDS
from game_evaluator import GameEvaluator, HandResult
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

    def _get_kickers_from_hand(
        self, player_cards: List[Card], main_cards: List[Card]
    ) -> List[Card]:
        if len(player_cards) != 7 or len(main_cards) > 5:
            raise ValueError(
                f"player_cards or main_cards not valid: {to_string(player_cards)}, {to_string(main_cards)}"
            )
        # max cards allowed for a hand
        if len(main_cards) == 5:
            return []

        cards_used_for_kickers = 5 - len(main_cards)
        kicker_options = set(player_cards) - set(main_cards)
        sorted_kicker_options = sorted(
            list(kicker_options), key=lambda card: card.get_high_card_value()
        )
        return sorted_kicker_options[-cards_used_for_kickers:]

    def _evaluating_player_hands(self) -> dict[str, Player]:
        logging.info("evaluating player hands")
        logging.info(f"players: {to_string(self.players)}")
        for player_id in self.players.keys():
            player_cards = self.players[player_id].cards + self.get_board()
            hand_result, main_cards = self.game_evaluator.evaluate_hand(player_cards)
            self.players[player_id].hand_result = hand_result
            self.players[player_id].main_cards = main_cards
            self.players[player_id].kickers = self._get_kickers_from_hand(
                player_cards, main_cards
            )

        logging.info(
            f"player_id: {player_id}, player_cards: {to_string(player_cards)}, hand result: {to_string(hand_result)}"
        )

        return self.players

    def _poplulate_players(self, num_players) -> None:
        logging.info(f"dealing cards to {num_players} players")
        for _ in range(num_players):
            new_player = Player()
            player_cards = self._deal_card(
                f"dealing cards for player {new_player.id}", CardDealAmount.PLAYER
            )
            new_player.cards = player_cards
            self.players[new_player.id] = new_player

    def _find_tie_break_kicker_winners(self, tie_players: List[Player]):
        # no more kicker to tie break
        if not tie_players[0].kickers:
            return tie_players

        highest_kicker_card_map: dict[int, List[Player]] = defaultdict(list)
        highest_kicker_value = float("-inf")

        for i in range(len(tie_players)):
            player_highest_kicker_card = tie_players[i].kickers[-1]
            highest_kicker_card_map[player_highest_kicker_card.value].append(
                tie_players[i]
            )
            tie_players[i].kickers.pop()
            highest_kicker_value = max(
                highest_kicker_value, player_highest_kicker_card.value
            )

        # still haven't figured out winner
        if len(highest_kicker_card_map[highest_kicker_value]) > 1:
            return self._find_tie_break_kicker_winners(tie_players)

        return tie_players

    def _find_tie_break_winners(self, tie_players: List[Player]) -> List[Player]:
        """
        all tie players should have the same number of main cards for potential
        winning hand
        """
        logging.info(f"tie players {to_string(tie_players)}")
        main_cards_count = len(tie_players[0].main_cards)
        for _ in range(main_cards_count):
            cur_max_card = max([player.main_cards[-1] for player in tie_players])
            remove_idx = []
            for idx, player in enumerate(tie_players):
                if (
                    player.main_cards[-1].get_high_card_value()
                    < cur_max_card.get_high_card_value()
                ):
                    remove_idx.append(idx)
                else:
                    player.main_cards.pop()
            for idx in remove_idx:
                del tie_players[idx]
            if len(tie_players) == 1:
                return tie_players

        return self._find_tie_break_kicker_winners(tie_players)

    def dealing_to_board(self, dealing_type: CardDealAmount):
        self._deal_card(f"burn 1 for {dealing_type}", CardDealAmount.BURN)
        cards_dealt = self._deal_card(f"{dealing_type}", dealing_type)
        self.board.extend(cards_dealt)

    def get_board(self):
        if self._debug:
            logging.info(f"board cards - {[str(c) for c in self.board]}")
        return self.board

    def find_winners(self) -> List[Player]:
        logging.info("finding hand winner(s)")
        self._evaluating_player_hands()
        score_player_map = defaultdict(list)
        max_score = HandResult.HIGH_CARD.value
        for player in self.players.values():
            player_score = player.hand_result.value
            score_player_map[player_score].append(player)
            max_score = max(max_score, player_score)

        # tie breaking
        if len(score_player_map[max_score]) > 1:
            return self._find_tie_break_winners(score_player_map[max_score])

        # only 1 winner in hand
        return score_player_map[max_score]
