import itertools
from card import Card, Suite

CARD_VALUES = range(1, 13)
ALL_CARDS = [Card(comb[0], comb[1]) for comb in list(itertools.product(list(Suite.__members__.values()), CARD_VALUES))]
