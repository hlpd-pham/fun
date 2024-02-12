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

    def get_high_card_value(self):
        return 14 if self.value == 1 else self.value

    def __eq__(self, other):
        if not isinstance(other, Card):
            # Don't attempt to compare against unrelated types
            return NotImplemented
        return self.suite == other.suite and self.value == other.value

    def __lt__(self, other):
        if not isinstance(other, Card):
            # Don't attempt to compare against unrelated types
            return NotImplemented
        return self.value < other.value

    def __le__(self, other):
        return self < other or self == other

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.get_face_card_value()}, {self.suite})"
