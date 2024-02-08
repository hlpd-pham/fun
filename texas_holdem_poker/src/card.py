from aenum import Enum, NoAlias

class CardDealAmount(Enum):
    _settings_ = NoAlias

    PLAYER = 2
    BURN = 1
    FLOP = 3
    TURN = 1
    RIVER = 1


class Suite(Enum):
    HEART = 1
    DIAMOND = 2
    CLUB = 3
    SPADE = 4


class Card:
    def __init__(self, suite: Suite = Suite.SPADE, value: int = 1):
        self.suite = suite
        self.value = value


    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.get_face_card_value()}, {self.suite})"


    def get_face_card_value(self):
        special_values = { 1: 'Ace', 11: 'Jack', 12: 'Queen', 13: 'King', }
        return special_values.get(self.value, self.value)


