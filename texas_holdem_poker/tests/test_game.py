from typing import List
from unittest.mock import patch

import pytest

from card import Card, CardDealAmount, Suite
from game import Game

# Mock cards to be used in tests
mock_cards = [
    Card(Suite.HEART, 2),
    Card(Suite.SPADE, 3),
    Card(Suite.DIAMOND, 4),
]


@pytest.fixture
def game() -> Game:
    """Fixture to create a Game instance for tests."""
    game = Game(num_players=1, debug=True)
    return game


def test_game_init(game: Game):
    assert len(game.players) == 1
    assert len(game.deck) == 50
    assert len(game.get_board()) == 0
    assert game._debug


def test_dealing_to_board_flop(game: Game):
    with patch("random.sample", return_value=mock_cards[:2]):
        game.dealing_to_board(CardDealAmount.FLOP)  # Flop mock
        assert len(game.board) == 3  # Expect 3 cards on the board after flop


# def test_dealing_to_board_turn(game):
#     with patch("random.sample", return_value=mock_cards[1:2]):
#         game.dealing_to_board(CardDealAmount.BURN)  # Burn card mock
#         game.dealing_to_board(CardDealAmount.TURN)  # Turn mock
#         assert len(game.board) == 1  # Expect 1 card on the board after turn
#         assert game.board[0] == mock_cards[1]  # Second card in mock list
#
#
# def test_dealing_to_board_river(game):
#     with patch("random.sample", return_value=mock_cards[2:3]):
#         game.dealing_to_board(CardDealAmount.BURN)  # Burn card mock
#         game.dealing_to_board(CardDealAmount.RIVER)  # River mock
#         assert len(game.board) == 1  # Expect 1 card on the board after river
#         assert game.board[0] == mock_cards[2]  # Third card in mock list
