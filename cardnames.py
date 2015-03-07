"""
Pranjal Mittal
"""

curse        =  0
estate       =  1
duchy        =  2
province     =  3
copper       =  4
silver       =  5
gold         =  6
adventurer   =  7
ambassador   =  8
baron        =  9
council_room =  10
cutpurse     =  11
embargo      =  12
feast        =  13
gardens      =  14
great_hall   =  15
mine         =  16

# Optional cards
                        # minion       =  17
                        # outpost      =  18
remodel      =  17      # remodel      =  19
                        # salvager     =  20
                        # sea_hag      =  21
smithy       =  18      # smithy       =  22
                        # steward      =  23
                        # treasure_map =  24
                        # tribute      =  25
village      =  19      # village      =  26

first_card = curse
last_card = village

allowed_kingdomcard_set = set({adventurer, ambassador, baron, council_room, cutpurse,
                             embargo, feast, gardens, great_hall, mine, mine,
                             remodel, smithy, village})

from collections import OrderedDict

CARD_NAMES = OrderedDict([(0, 'curse'), (1, 'estate'), (2, 'duchy'), (3, 'province'),           # Victory cards

    (4, 'copper'), (5, 'silver'), (6, 'gold'),                                                  # Treasure cards

    (7, 'adventurer'), (8, 'ambassador'), (9, 'baron'), (10, 'council_room'), (11, 'cutpurse'), # Kingdom cards
    (12, 'embargo'), (13, 'feast'), (14, 'gardens'), (15, 'great_hall'), (16, 'mine'),

    (17, 'remodel'), (18, 'smithy'), (19, 'village')]
)


NCARDS = 20

CARD_COST = {
  curse:        0,
  estate:       2,
  duchy:        5,
  province:     8,
  copper:       0,
  silver:       3,
  gold:         6,
  adventurer:   6,
  ambassador:   3,
  baron:        4,
  council_room: 5,
  cutpurse:     4,
  embargo:      2,
  feast:        4,
  gardens:      4,
  great_hall:   3,
  mine:         5,
  remodel:      4,
  smithy:       4,
  village:      3,
}

"""
# Order here differes from the order in the cardnames, but doesn't matter
# since dictionary is unordered anyway.
CARD_COST = {
  curse: 0,
  estate: 2,
  duchy: 5,
  province: 8,
  copper: 0,
  silver: 3,
  gold: 6,
  adventurer: 6,
  council_room: 5,
  feast: 4,
  gardens: 4,
  mine: 5,
  remodel: 4,
  smithy: 4,
  village: 3,
  baron: 4,
  great_hall: 3,
  minion: 5,
  steward: 3,
  tribute: 5,
  ambassador: 3,
  cutpurse: 4,
  embargo: 2,
  outpost: 5,
  salvager: 4,
  sea_hag: 4,
  treasure_map: 4,
}


CARD_NAMES = OrderedDict([(0, 'curse'), (1, 'estate'), (2, 'duchy'), (3, 'province'),

    (4, 'copper'), (5, 'silver'), (6, 'gold'),

    (7, 'adventurer'), (8, 'ambassador'), (9, 'baron'), (10, 'council_room'), (11, 'cutpurse'),
    (12, 'embargo'), (13, 'feast'), (14, 'gardens'), (15, 'great_hall'), (16, 'mine'),

    (17, 'minion'), (18, 'outpost'), (19, 'remodel'), (20, 'salvager'), (21, 'sea_hag'),
    (22, 'smithy'), (23, 'steward'), (24, 'treasure_map'), (25, 'tribute'), (26, 'village')]
)
"""