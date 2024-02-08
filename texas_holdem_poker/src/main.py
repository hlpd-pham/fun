from card import CardDealAmount
from game import Game


def run():
    game = Game(num_players=3, debug=True)
    
    game.dealing_to_board(CardDealAmount.FLOP)
    game.dealing_to_board(CardDealAmount.TURN)
    game.dealing_to_board(CardDealAmount.RIVER)
    
    game.get_board()
run()
