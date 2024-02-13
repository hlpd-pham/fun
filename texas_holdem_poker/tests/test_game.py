import logging
from unittest.mock import patch

import pytest

from card import Card, CardDealAmount, Suite
from game import Game, HandResult

from .fixtures.game_mock_data import mock_card_options


class TestGame:

    def make_mock_cards(self, num_players=1):
        def mock_cards(*args, **kwargs):
            ret = []
            cards_for_players = 2 * num_players
            match self.call_count:
                case 0:
                    ret = mock_card_options[:cards_for_players]  # deal to player
                case 1:
                    ret = mock_card_options[
                        cards_for_players : cards_for_players + 1
                    ]  # burn for flop
                case 2:
                    ret = mock_card_options[
                        cards_for_players + 1 : cards_for_players + 4
                    ]  # flop
                case 3:
                    ret = mock_card_options[
                        cards_for_players + 4 : cards_for_players + 5
                    ]  # burn for turn
                case 4:
                    ret = mock_card_options[
                        cards_for_players + 5 : cards_for_players + 6
                    ]  # turn
                case 5:
                    ret = mock_card_options[
                        cards_for_players + 6 : cards_for_players + 7
                    ]  # burn for river
                case 6:
                    ret = mock_card_options[
                        cards_for_players + 7 : cards_for_players + 8
                    ]  # river
                case _:
                    ret = []
            self.call_count += 1
            return ret

        return mock_cards

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        # Setup phase
        logging.info("Setup before each test")
        self.call_count = 0
        with patch("random.sample", side_effect=self.make_mock_cards()):
            self.game_instance: Game = Game(num_players=1, debug=True)

        # The yield keyword pauses the fixture here, allowing the test to run with the setup completed
        yield

        # Teardown phase - after yield
        logging.info("Teardown after each test")

    def test_game_init(self):
        """expect initialization states with 1 player"""
        assert len(self.game_instance.players) == 1
        assert len(self.game_instance.deck) == 50
        assert len(self.game_instance.get_board()) == 0
        assert self.game_instance._debug

    def test_game_init_bad_input(self):
        with pytest.raises(ValueError, match="Invalid number of players: "):
            self.game_instance: Game = Game(num_players=-1)

    def test_dealing_to_board_flop(self):
        with patch("random.sample", side_effect=self.make_mock_cards()):
            """expects 3 cards on board after flop"""
            self.game_instance.dealing_to_board(CardDealAmount.FLOP)
            assert (
                len(self.game_instance.get_board()) == 3
            )  # Expect 3 cards on the board after flop
            assert self.game_instance.get_board() == mock_card_options[3:6]

    def test_dealing_to_board_turn(self):
        with patch("random.sample", side_effect=self.make_mock_cards()):
            """expects 4 cards on board after turn"""
            self.game_instance.dealing_to_board(CardDealAmount.FLOP)
            self.game_instance.dealing_to_board(CardDealAmount.TURN)
            assert (
                len(self.game_instance.get_board()) == 4
            )  # Expect 4 cards on the board after turn
            assert (
                self.game_instance.get_board()
                == mock_card_options[3:6] + mock_card_options[7:8]
            )

    def test_dealing_to_board_river(self):
        with patch("random.sample", side_effect=self.make_mock_cards()):
            """expects 5 cards on board after river"""
            self.game_instance.dealing_to_board(CardDealAmount.FLOP)
            self.game_instance.dealing_to_board(CardDealAmount.TURN)
            self.game_instance.dealing_to_board(CardDealAmount.RIVER)
            assert (
                len(self.game_instance.get_board()) == 5
            )  # Expect 5 cards on the board after river
            assert (
                self.game_instance.get_board()
                == mock_card_options[3:6]
                + mock_card_options[7:8]
                + mock_card_options[9:10]
            )

    def test_evaluating_hand_bad_input(self):
        with pytest.raises(
            ValueError, match="there must be 7 cards in hand for evaluation"
        ):
            self.game_instance.evaluate_hand([])

    def test_evaluating_hand_bad_input_duplicate_cards(self):
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
            self.game_instance.evaluate_hand(hand_cards)

    def test_evaluating_hand_1_pair(self):
        hand_cards = [
            Card(4, Suite.DIAMOND),
            Card(4, Suite.SPADE),
            Card(7, Suite.HEART),
            Card(9, Suite.CLUB),
            Card(10, Suite.SPADE),
            Card(11, Suite.SPADE),
            Card(1, Suite.CLUB),
        ]
        hand_result, _ = self.game_instance.evaluate_hand(hand_cards)
        assert hand_result == HandResult.PAIR

    def test_evaluating_hand_2_pairs(self):
        hand_cards = [
            Card(4, Suite.DIAMOND),
            Card(4, Suite.SPADE),
            Card(7, Suite.HEART),
            Card(7, Suite.CLUB),
            Card(10, Suite.SPADE),
            Card(11, Suite.SPADE),
            Card(1, Suite.CLUB),
        ]
        hand_result, _ = self.game_instance.evaluate_hand(hand_cards)
        assert hand_result == HandResult.TWO_PAIRS

    def test_evaluating_hand_trips(self):
        hand_cards = [
            Card(4, Suite.DIAMOND),
            Card(4, Suite.SPADE),
            Card(4, Suite.CLUB),
            Card(7, Suite.CLUB),
            Card(10, Suite.SPADE),
            Card(11, Suite.SPADE),
            Card(1, Suite.CLUB),
        ]
        hand_result, _ = self.game_instance.evaluate_hand(hand_cards)
        assert hand_result == HandResult.THREE_OF_A_KIND

    def test_evaluating_hand_straight(self):
        hand_cards = [
            Card(1, Suite.DIAMOND),
            Card(2, Suite.SPADE),
            Card(3, Suite.CLUB),
            Card(4, Suite.CLUB),
            Card(5, Suite.SPADE),
            Card(11, Suite.SPADE),
            Card(1, Suite.CLUB),
        ]
        hand_result, _ = self.game_instance.evaluate_hand(hand_cards)
        assert hand_result == HandResult.STRAIGHT

    def test_evaluating_hand_flush(self):
        hand_cards = [
            Card(1, Suite.DIAMOND),
            Card(2, Suite.SPADE),
            Card(3, Suite.CLUB),
            Card(4, Suite.CLUB),
            Card(5, Suite.CLUB),
            Card(11, Suite.CLUB),
            Card(1, Suite.CLUB),
        ]
        hand_result, _ = self.game_instance.evaluate_hand(hand_cards)
        assert hand_result == HandResult.FLUSH

    def test_evaluating_hand_full_house(self):
        hand_cards = [
            Card(1, Suite.DIAMOND),
            Card(3, Suite.SPADE),
            Card(3, Suite.CLUB),
            Card(3, Suite.DIAMOND),
            Card(5, Suite.CLUB),
            Card(11, Suite.CLUB),
            Card(1, Suite.CLUB),
        ]
        hand_result, _ = self.game_instance.evaluate_hand(hand_cards)
        assert hand_result == HandResult.FULL_HOUSE

    def test_evaluating_hand_four_of_a_kind(self):
        hand_cards = [
            Card(1, Suite.DIAMOND),
            Card(1, Suite.SPADE),
            Card(1, Suite.CLUB),
            Card(3, Suite.DIAMOND),
            Card(5, Suite.CLUB),
            Card(11, Suite.CLUB),
            Card(1, Suite.HEART),
        ]
        hand_result, _ = self.game_instance.evaluate_hand(hand_cards)
        assert hand_result == HandResult.FOUR_OF_A_KIND

    def test_evaluating_hand_straight_flush(self):
        hand_cards = [
            Card(1, Suite.DIAMOND),
            Card(2, Suite.DIAMOND),
            Card(3, Suite.DIAMOND),
            Card(4, Suite.DIAMOND),
            Card(5, Suite.DIAMOND),
            Card(11, Suite.CLUB),
            Card(1, Suite.CLUB),
        ]
        hand_result, _ = self.game_instance.evaluate_hand(hand_cards)
        assert hand_result == HandResult.STRAIGHT_FLUSH

    def test_evaluating_hand_royal(self):
        hand_cards = [
            Card(1, Suite.DIAMOND),
            Card(10, Suite.DIAMOND),
            Card(11, Suite.DIAMOND),
            Card(12, Suite.DIAMOND),
            Card(13, Suite.DIAMOND),
            Card(11, Suite.CLUB),
            Card(1, Suite.CLUB),
        ]
        hand_result, _ = self.game_instance.evaluate_hand(hand_cards)
        assert hand_result == HandResult.ROYAL_FLUSH
