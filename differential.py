from mydominion import dominion as d1
from classmate_dominion import dominion as d2
from mydominion.cardnames import *

common_kingdom_cards = [adventurer, ambassador, baron, council_room, cutpurse,
                        embargo, feast, gardens, great_hall, mine]
g1 = d1.initializeGame(2, common_kingdom_cards, 0)
g2 = d2.initializeGame(2, common_kingdom_cards, 0)
