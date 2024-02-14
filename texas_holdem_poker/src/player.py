import uuid
from typing import List

from card import Card
from game_evaluator import HandResult
from utils.strings import to_string


class Player:
    def __init__(self, cards: List[Card] = []):
        self.id = uuid.uuid4()
        self.cards = cards
        self.hand_result: HandResult = HandResult.HIGH_CARD
        self.main_cards: List[Card] = []
        self.kickers: List[Card] = []

    def __str__(self):
        return f"Player(id:{self.id}\n\tcards:{to_string(self.cards)}\n\thand_result: {self.hand_result}\n\tbest_five: {to_string(self.main_cards)})\n\tkickers: {to_string(self.kickers)}\n"
