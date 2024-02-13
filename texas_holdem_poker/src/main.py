import logging

from card import CardDealAmount
from game import Game
from utils.strings import to_string

logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    filemode="w",
    format="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s",
)


def run():
    game = Game(num_players=3, debug=True)

    for deal_type in [CardDealAmount.FLOP, CardDealAmount.TURN, CardDealAmount.RIVER]:
        print(deal_type)
        game.dealing_to_board(deal_type)

    print(to_string(game.get_board()))

    print(f"evaluating hands")
    for idx, p in enumerate(game.players):
        print(
            f"player {idx}: {to_string(p)} - {to_string(game.evaluate_hand(p + game.get_board()))}"
        )


run()
