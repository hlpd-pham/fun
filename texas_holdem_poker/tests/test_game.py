import logging
from enum import Enum
from unittest.mock import patch

import pytest

from card import Card, CardDealAmount, Suite
from game import Game

from .fixtures.game_mock_data import mock_card_options


class MockCardType(Enum):
    START = 1
    FLOP = 2
    TURN = 3
    RIVER = 4


class TestGame:

    def make_mock_cards(self, mock_type: MockCardType):
        def mock_cards(*args, **kwargs):
            DEFAULT_RET = [Card(Suite.DIAMOND, 2), Card(Suite.CLUB, 2)]
            match mock_type:
                case MockCardType.FLOP:
                    ret = []
                    match self.call_count:
                        case 0:
                            ret = mock_card_options[:2]  # deal to player
                        case 1:
                            ret = mock_card_options[2:3]  # burn for flop
                        case 2:
                            ret = mock_card_options[3:6]  # flop
                        case _:
                            ret = DEFAULT_RET
                case _:
                    ret = DEFAULT_RET
            self.call_count += 1
            return ret

        return mock_cards

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        # Setup phase
        logging.info("Setup before each test")
        self.call_count = 0
        with patch(
            "random.sample", side_effect=self.make_mock_cards(MockCardType.START)
        ):
            self.game_instance = Game(num_players=1, debug=True)

        # The yield keyword pauses the fixture here, allowing the test to run with the setup completed
        yield

        # Teardown phase - after yield
        logging.info("Teardown after each test")
        # Here you can add any necessary cleanup logic. For this example, there's nothing specific to clean up,
        # but you might want to reset states, delete files, close connections, etc.

    def test_game_init(self):
        game_obj = Game(num_players=1, debug=True)
        assert len(game_obj.players) == 1
        assert len(game_obj.deck) == 50
        assert len(game_obj.get_board()) == 0
        assert game_obj._debug

    def test_dealing_to_board_flop(self):
        with patch(
            "random.sample", side_effect=self.make_mock_cards(MockCardType.FLOP)
        ):
            self.game_instance.dealing_to_board(CardDealAmount.FLOP)  # Flop mock
            assert (
                len(self.game_instance.get_board()) == 3
            )  # Expect 3 cards on the board after flop
            assert self.game_instance.get_board() == mock_card_options[3:6]
