import logging
from unittest.mock import patch

import pytest

from game import Game


class TestGameTieBreak:

    def make_mock_cards(self, num_players=2):
        ret = []
        _ = 2 * num_players
        return ret

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        # Setup phase
        logging.info("TestGame setup")
        self.call_count = 0
        with patch("random.sample", side_effect=self.make_mock_cards()):
            self.game_instance: Game = Game(num_players=1, debug=True)

        # The yield keyword pauses the fixture here, allowing the test to run with the setup completed
        yield

        # Teardown phase - after yield
        logging.info("TestGame teardown")
