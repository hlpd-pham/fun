from aenum import Enum, NoAlias


class CardDealAmount(Enum):
    _settings_ = NoAlias

    PLAYER = 2
    BURN = 1
    FLOP = 3
    TURN = 1
    RIVER = 1


class Suite(Enum):
    _settings_ = NoAlias

    HEART = 1
    DIAMOND = 1
    CLUB = 1
    SPADE = 1


class Card:
    def __init__(self, value: int = 1, suite: Suite = Suite.SPADE):
        self.value: int = value
        self.suite: Suite = suite

    def get_face_card_value(self):
        special_values = {
            1: "Ace",
            11: "Jack",
            12: "Queen",
            13: "King",
        }
        return special_values.get(self.value, self.value)

    def get_card_value_suite(self):
        return self.value, self.suite

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.get_face_card_value()}, {self.suite})"
