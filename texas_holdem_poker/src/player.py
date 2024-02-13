from typing import List

from card import Card
import uuid

from game_evaluator import HandResult
from utils.strings import to_string


class Player:
    def __init__(self, cards: List[Card] = []):
        self.id = uuid.uuid4()
        self.cards = cards
        self.hand_result: HandResult = HandResult.HIGH_CARD

    def __str__(self):
        return f'Player(id:{self.id}, cards:{to_string(self.cards)}, hand_result: {self.hand_result}'
