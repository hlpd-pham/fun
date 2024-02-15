import logging

import pytest

from game import Game
from tests.game.parse_utils import parse_cards, parse_players
from utils.strings import to_string

from .test_cases.one_pair_data import one_pair_1, one_pair_2
from .test_cases.two_pair_data import two_pair_1_winner


class TestGameTieBreak:

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        # Setup phase
        logging.info("TestGame setup")
        self.game_instance: Game = Game(num_players=0, debug=True)

        # The yield keyword pauses the fixture here, allowing the test to run with the setup completed
        yield

        # Teardown phase - after yield
        logging.info("TestGame teardown")

    def test_one_pair_winner_kicker(self):
        players = parse_players(one_pair_1["Players"])
        for idx, player in enumerate(players):
            self.game_instance.players[idx] = player
        self.game_instance.board = parse_cards(one_pair_1["Board"])
        self.game_instance.get_board()
        winners = self.game_instance.find_winners()
        winner_ids = [player.id for player in winners]
        assert winner_ids == one_pair_1["Winners"]

    def test_one_pair_winner_higher_pair(self):
        players = parse_players(one_pair_2["Players"])
        for idx, player in enumerate(players):
            self.game_instance.players[idx] = player
        self.game_instance.board = parse_cards(one_pair_2["Board"])
        self.game_instance.get_board()
        winners = self.game_instance.find_winners()
        winner_ids = [player.id for player in winners]
        assert winner_ids == one_pair_2["Winners"]

    def test_two_pair_highest_2nd_pair(self):
        players = parse_players(two_pair_1_winner["Players"])
        for idx, player in enumerate(players):
            self.game_instance.players[idx] = player
        self.game_instance.board = parse_cards(two_pair_1_winner["Board"])
        self.game_instance.get_board()
        winners = self.game_instance.find_winners()
        winner_ids = [player.id for player in winners]
        assert winner_ids == two_pair_1_winner["Winners"]
