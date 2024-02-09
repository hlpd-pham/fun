from typing import List
from unittest.mock import patch

import pytest

from card import Card, CardDealAmount, Suite
from game import Game

# Mock cards to be used in tests
mock_card_options = [
    Card(Suite.HEART, 1),
    Card(Suite.SPADE, 1),
    Card(Suite.DIAMOND, 1),
    Card(Suite.CLUB, 1),
    Card(Suite.HEART, 2),
    Card(Suite.SPADE, 2),
    Card(Suite.DIAMOND, 2),
    Card(Suite.CLUB, 2),
]

mock_cards_call_count = 0


def mock_cards(*_, **__):
    global mock_cards_call_count
    ret = [Card(Suite.DIAMOND, 2), Card(Suite.CLUB, 2)]
    match mock_cards_call_count:
        case 0:
            ret = mock_card_options[:2] # deal to player
        case 1:
            ret = mock_card_options[2:3] # burn for flop
        case 2:
            ret = mock_card_options[3:6] # flop
        case _:
            pass
    mock_cards_call_count += 1
    return ret


@pytest.fixture
def game() -> Game:
    """Fixture to create a Game instance for tests."""
    with patch("random.sample", side_effect=mock_cards):
        game = Game(num_players=1, debug=True)
        return game


def test_game_init():
    game_obj = Game(num_players=1, debug=True)
    assert len(game_obj.players) == 1
    assert len(game_obj.deck) == 50
    assert len(game_obj.get_board()) == 0
    assert game_obj._debug


def test_dealing_to_board_flop(game: Game):
    with patch("random.sample", side_effect=mock_cards):
        game.dealing_to_board(CardDealAmount.FLOP)  # Flop mock
        assert len(game.get_board()) == 3  # Expect 3 cards on the board after flop
        assert game.get_board() == mock_card_options[3:6]


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
