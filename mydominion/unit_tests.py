"""
Pranjal Mittal
"""

import random
import unittest
import dominion as d
from cardnames import *

common_kingdom_cards = [adventurer, ambassador, baron, council_room, cutpurse,
                                embargo, feast, gardens, great_hall, mine]

pranjal_kingdom_cards = [adventurer, ambassador, baron, council_room, cutpurse,
                                embargo, feast, remodel, smithy, village]


############################## USEFUL FUNCTIONS ################################

def count_cards(card, player, which_pile, g):
    """
    Counts the number of time a card occurs in a players pile.
    :which_pile: "deck", "discard" or "hand".
    """
    ctr = 0
    if which_pile == "deck":
        for c in g.deck[player]:
            if c == card:
                ctr += 1

    if which_pile == "hand":
        for c in g.hand[player]:
            if c == card:
                ctr += 1

    if which_pile == "discard":
        for c in g.discard[player]:
            if c == card:
                ctr += 1

    return ctr

###################### TESTS FOR TOP LEVEL API FUNCTIONS ########################
#################################################################################

class TestInitializeGame(unittest.TestCase):

    def test_numplayers_valid(self):
        # 2 is valid number of players
        g = d.initializeGame(2, [adventurer, ambassador, smithy, council_room, cutpurse,
                                embargo, feast, gardens, great_hall, mine], 0)
        self.assertNotEqual(g, 0, "Initialize game did not work correctly for 2 players.")

    def test_numplayers_less_than_min(self):
        g = d.initializeGame(1, [adventurer, ambassador, smithy, council_room, cutpurse,
                                embargo, feast, gardens, great_hall, mine], 0)
        self.assertEqual(g, -1, "Initialize game should not return 0 for 1 player but it did")

    def test_numplayers_more_than_max(self):
        g = d.initializeGame(5, [adventurer, ambassador, smithy, council_room, cutpurse,
                                embargo, feast, gardens, great_hall, mine], 0)
        self.assertEqual(g, -1, "Initialize game should not work with 5 players")

    def test_more_than_10_kindgomcards(self):
        g = d.initializeGame(2, [adventurer, ambassador, smithy, council_room, cutpurse,
                                embargo, feast, gardens, great_hall, mine, village], 0)
        self.assertEqual(g, -1, "More than 10 kingdom cards present")

    def test_less_than_10_kindgomcards(self):
        g = d.initializeGame(2, [adventurer, ambassador, smithy, council_room, cutpurse,
                                embargo, feast, gardens, great_hall], 0)
        self.assertEqual(g, -1, "Less than 10 kinddom cards present")

    def test_initial_supply(self):
        g = d.initializeGame(2, common_kingdom_cards, 0)

        valid_supply = [10, 8, 8, 8, 46, 40, 30, 10, 10, 10, 10, 10, 10, 10, 8, 8, 10, -1, -1, -1]
        self.assertSequenceEqual(g.supplyCount, valid_supply, "Invalid supply: %s"%(str(g.supplyCount),))


class TestBuyCard(unittest.TestCase):

    def setUp(self):
        g = d.initializeGame(2, common_kingdom_cards, 0)
        coins = g.coins

        self.buyable_cards = []
        for card, cost in CARD_COST.items():
            if cost <= coins and g.supplyCount[card]>0:
                self.buyable_cards.append(card)
        self.random_buyable_card = random.choice(self.buyable_cards)

        self.non_budget_cards = []
        for card, cost in CARD_COST.items():
            if cost > coins:
                self.non_budget_cards.append(card)

        self.budget_but_no_supply_cards = []
        for card, cost in CARD_COST.items():
            if (cost <= coins) and (g.supplyCount[card]<=0):
                self.budget_but_no_supply_cards.append(card)

        self.non_buyable_cards = []
        for card, cost in CARD_COST.items():
            if cost > coins or g.supplyCount[card]<=0:
                self.non_buyable_cards.append(card)
        self.random_non_buyable_card = random.choice(self.budget_but_no_supply_cards)

        self.g = g

    def test_buycard_not_enough_coins(self):
        g = self.g
        # Just after game is initialized. Any of the players cannot have more than 5 cards in hand.
        # Adventurer costs 6. So buyCard should fail.
        self.assertLessEqual(g.coins, 6, "Player %d has more coins than expected"%(g.whoseTurn,))
        r = d.buyCard(adventurer, g)
        self.assertEqual(r, -1, "Player was able to buy adventurer costing 6 with only %d coins"%(g.coins))

    def test_if_buyable_cards_can_be_bought(self):
        g = self.g
        coins = g.coins

        r = d.buyCard(self.random_buyable_card, g)
        self.assertEqual(r, 0, "User was not able to buy card %s with %d coins"%(CARD_NAMES[self.random_buyable_card], coins))

    def test_coins_are_consumed_on_buying(self):
        """
        Coins equal to cost of card bought must be consumed
        """
        g = self.g
        coins = g.coins

        r = d.buyCard(self.random_buyable_card, g)
        remaining_coins = g.coins

        self.assertEqual(coins-remaining_coins, CARD_COST[self.random_buyable_card], "Coins consumed not same as cost of card bought")

    def tearDown(self):
        del self.g


class TestNumHandCards(unittest.TestCase):

    def test_num_hand_cards_after_initialize(self):
        g = d.initializeGame(2, common_kingdom_cards, 0)
        r = d.numHandCards(g)
        self.assertEqual(r, 5, "After initialize game there should be 5 cards in hand")


class TestHandCard(unittest.TestCase):

    def test_hand_card(self):
        # If initialized with seed = 0, card at index pos 0 must be copper
        g = d.initializeGame(2, common_kingdom_cards, 0)
        r = d.handCard(0, g)
        self.assertEqual(r, 4, "handCard did not work as expected")


class TestSupplyCount(unittest.TestCase):

    def test_initial_2player_supply(self):
        g = d.initializeGame(2, common_kingdom_cards, 0)

        valid_supply = [10, 8, 8, 8, 46, 40, 30, 10, 10, 10, 10, 10, 10, 10, 8, 8, 10, -1, -1, -1]
        self.assertSequenceEqual(g.supplyCount, valid_supply, "Invalid supply: %s"%(str(g.supplyCount),))


class TestFullDeckCount(unittest.TestCase):
    """
    Here deck = hand + discard + deck
    """
    def setUp(self):
        self.g = d.initializeGame(2, common_kingdom_cards, 0)

    def test_init_coppers(self):
        g = self.g
        r = d.fullDeckCount(g.whoseTurn, copper, g)
        self.assertEqual(r, 7, "There should be 7 coppers in the beginning")

    def test_init_estates(self):
        g = self.g
        r = d.fullDeckCount(g.whoseTurn, estate, g)
        self.assertEqual(r, 3, "There should be 3 estates in the beginning")

    def test_init_smithy(self):
        g = self.g
        r = d.fullDeckCount(g.whoseTurn, smithy, g)
        self.assertEqual(r, 0, "There should be 0 smithy's in the beginning")

    def test_after_adding_card(self):
        g = self.g

        r = d.fullDeckCount(g.whoseTurn, gardens, g)
        self.assertEqual(r, 0, "There should be 0 garden now since nothing added so far")

        g.deck[g.whoseTurn].append(gardens)
        r = d.fullDeckCount(g.whoseTurn, gardens, g)
        self.assertEqual(r, 1, "There should be 1 garden now since it has been added")

    def tearDown(self):
        del self.g


class TestPlayCard(unittest.TestCase):

    def setUp(self):
        self.g = d.initializeGame(2, common_kingdom_cards, 0)
        self.P = self.g.whoseTurn        # Current player

    def test_play_without_actions(self):
        g = self.g
        g.numActions = 0
        g.hand[self.P].append(council_room)
        len_hand = len(g.hand[self.P])
        r = d.playCard(len_hand-1, None, None, None, g)
        self.assertEqual(r, -1, "playCard call should have failed without available actions")

    def test_adventurer(self):
        """
        Assumes the deck + discard will have atleast 2 treasure cards (Doesn't test this condition.)
        """
        g = self.g
        # Lets add adventurer to hand of current player by magic.
        g.hand[self.P].append(adventurer)

        len_hand = len(g.hand[self.P])
        coins = g.coins

        # Play the last card in hand which is adventurer
        r = d.playCard(len_hand-1, None, None, None, g)
        self.assertEqual(r, 0, "playCard call failed for adventurer")

        updated_len_hand = len(g.hand[self.P])
        updated_coins = g.coins

        self.assertEqual(updated_len_hand-len_hand, 1, "Hand size should increase by one overall")

        # Sum of last 2 treasure cards
        self.assertGreaterEqual(updated_coins-coins, 2, "Increase in coins cannot be less than 2")

    def test_ambassador(self):
        """
        choice1 = handPos
        choice2 = numner of cards to return to supply
        """
        g = self.g
        # Adding test card to hand by magic
        g.hand[self.P].append(ambassador)

        len_hand = len(g.hand[self.P])
        coins = g.coins

        # Play the test card
        r = d.playCard(len_hand-1, 0, 3, None, g)     # Should not allow returning more than 2 cards
        self.assertEqual(r, -1, "playCard call should have failed but didn't")

        # Play the test card
        r = d.playCard(len_hand-1, 0, 1, None, g)     # One card of that type will always be there in hand
        self.assertEqual(r, 0, "playCard call failed for ambassador")

    def test_baron(self):
        """
        #XXX: Currently failing
        @choice1: boolean for discard of estate
        """
        # Initializing with seed 2 gives an estate in hand
        g = d.initializeGame(2, common_kingdom_cards, 2)

        estate_present = False
        for c in g.hand[g.whoseTurn]:
            if c == estate:
                estate_present = True
                break

        assert estate_present

        # Adding test card to hand by magic
        g.hand[self.P].append(baron)

        len_hand = len(g.hand[self.P])
        coins = g.coins

        # Play the test card
        r = d.playCard(len_hand-1, 1, None, None, g)
        self.assertEqual(r, 0, "Baron should not fail as there was an estate in hand")

    def test_council_room(self):
        g = self.g

        # Add card to hand of current player by magic.
        g.hand[g.whoseTurn].append(council_room)

        r = d.council_room_test(g.whoseTurn, g, len(g.hand[self.P])-1)
        self.assertEqual(r, 0, "Council room failed")


    def test_cutpurse(self):
        """
        Each other player discards a Copper card (if any).
        """
        g = self.g

        coppers_in_hand = count_cards(copper, 1, "hand", g)

        # For seed 0 and 2 players, player 1 has 4 coppers after init game
        self.assertEqual(coppers_in_hand, 4)

        # Add card to hand of current player by magic.
        g.hand[g.whoseTurn].append(cutpurse)

        len_hand = len(g.hand[self.P])
        coins = g.coins

        r = d.playCard(len_hand-1, 1, None, None, g)
        self.assertEqual(r, 0, "Cutpurse failed")
        g.hand[1]
        coppers_in_hand = count_cards(copper, 1, "hand", g)
        self.assertEqual(coppers_in_hand, 3)


    def test_embargo(self):
        """
        +2 coins, Place an embargo token on the supply pile
        """
        g = d.initializeGame(2, common_kingdom_cards, 0)

        # Add card to hand of current player by magic.
        g.hand[g.whoseTurn].append(embargo)

        len_hand = len(g.hand[self.P])
        coins = g.coins

        # arbitrary_card should be in pile
        arbitrary_card = baron

        assert(arbitrary_card in common_kingdom_cards)

        # Initially 0 embargo on arbitrary_card

        self.assertEqual(g.embargoTokens[baron], 0)
        r = d.playCard(len_hand-1, baron, None, None, g)
        self.assertEqual(r, 0)
        # There should be 1 embargo on baron
        self.assertEqual(g.embargoTokens[baron], 1)

    def test_feast(self):
        g = d.initializeGame(2, common_kingdom_cards, 0)

        # Add card to hand of current player by magic.
        g.hand[g.whoseTurn].append(feast)
        len_hand = len(g.hand[self.P])

        # arbitrary_card should be in pile
        expensive_card = adventurer
        r = d.playCard(len_hand-1, expensive_card, None, None, g)
        self.assertEqual(r, -1)

        g = d.initializeGame(2, common_kingdom_cards, 0)
        g.hand[g.whoseTurn].append(feast)
        buyable_card = feast

        r = d.playCard(len_hand-1, buyable_card, None, None, g)
        self.assertEqual(r, 0)

    def test_gardens(self):
        g = self.g
        # Add card to hand of current player by magic.
        g.hand[g.whoseTurn].append(gardens)
        len_hand = len(g.hand[g.whoseTurn])

        r = d.playCard(len_hand-1, None, None, None, g)
        self.assertEqual(r, -1, "Garden cannot be played")

    def test_great_hall(self):
        g = self.g
        # Add card to hand of current player by magic.
        g.hand[g.whoseTurn].append(great_hall)
        len_hand = len(g.hand[g.whoseTurn])
        old_actions = g.numActions

        r = d.playCard(len_hand-1, None, None, None, g)
        self.assertEqual(r, 0)
        updated_len_hand = len(g.hand[g.whoseTurn])

        # Hand size should remain same +1 card -1 great_hall went to discard
        self.assertEqual(updated_len_hand-len_hand, 0)

        # Number of actions should not change
        self.assertEqual(g.numActions, old_actions)

    def test_mine(self):
        """
        choice1 is hand# of money to trash, choice2 is supply# of
        money to put in hand
        """
        g = self.g
        # Add card to hand of current player by magic.
        g.hand[g.whoseTurn].append(mine)
        len_hand = len(g.hand[g.whoseTurn])

        for handPos, card in enumerate(g.hand[g.whoseTurn]):
            if card == copper:
                choice1 = handPos

        r = d.playCard(len_hand-1, choice1, gold, None, g)
        self.assertEqual(r, -1, "Shouldn't be able to covert copper to gold")

        r = d.playCard(len_hand-1, choice1, silver, None, g)
        self.assertEqual(r, 0, "Should be able to convert copper to silver")

        updated_len_hand = len(g.hand[g.whoseTurn])
        # Hand size should reduce by 1, 1 mine consumed to convert a treasure to another treasure
        self.assertEqual(updated_len_hand-len_hand, -1)


    def test_play_smithy(self):
        g = self.g
        # Lets add smithy to hand of current player by magic.
        g.hand[g.whoseTurn].append(smithy)

        len_hand = len(g.hand[g.whoseTurn])
        len_deck_plus_discard = len(g.deck[g.whoseTurn]) + len(g.discard[g.whoseTurn])

        r = d.playCard(len_hand-1, None, None, None, g)
        self.assertEqual(r, 0, "Error in playCard call")

        # Using smithy should update hand length by 2 (+3 - smithy went to discard)
        # Deck + discard should reduce by 3 (-3 cards + smithy went to discard)
        updated_len_hand = len(g.hand[g.whoseTurn])
        updated_len_deck_plus_discard = len(g.deck[g.whoseTurn]) + len(g.discard[g.whoseTurn])

        self.assertEqual(updated_len_hand-len_hand, 2, "Hand size did not increase by 2 on using smithy")
        self.assertEqual(len_deck_plus_discard-updated_len_deck_plus_discard, 2, "Deck+Discard size did not reduce by 2")

    def tearDown(self):
        del self.g


class TestWhoseTurn(unittest.TestCase):

    def test_num_hand_cards_after_initialize(self):
        g = d.initializeGame(2, common_kingdom_cards, 0)
        r = d.whoseTurn(g)
        self.assertEqual(r, 0, "After game is initialzed it should be player 0's turn")


class TestEndTurn(unittest.TestCase):

    def setUp(self):
        self.g = d.initializeGame(2, common_kingdom_cards, 0)

    def test_check_player_changes(self):
        g = self.g

        # Initially player is 0
        self.assertEqual(g.whoseTurn, 0, "It should be Player 0's turn just after initializing game")

        r = d.endTurn(g)
        self.assertEqual(r, 0, "endTurn did not complete successfully")

        # If end turn ran succesfully, player must have changed
        self.assertEqual(g.whoseTurn, 1, "endTurn did not complete successfully")

    def tearDown(self):
        del self.g


class TestIsGameOver(unittest.TestCase):
    """
    The game ends under two conditions: when the stack of Province cards has been exhausted,
    or when any three other stacks in the Supply have been exhausted. 

    isGameOver returns 1 when game is over else returns 0
    """
    def setUp(self):
        self.g = d.initializeGame(2, common_kingdom_cards, 0)

    def test_game_not_over_yet(self):
        g = self.g

        # Magically changing supplyCount
        g.supplyCount = [10, 8, 8, 8, 46, 40, 0, 10, 10, 10, 10, 10, 10, 10, 8, 8, 10, -1, -1, -1]
        r = d.isGameOver(g)
        self.assertEqual(r, 0, "Game should be over when provinces are over")

    def test_isgameover_after_province_over(self):
        g = self.g

        # Magically changing supplyCount
        g.supplyCount = [10, 8, 8, 0, 46, 40, 30, 10, 10, 10, 10, 10, 10, 10, 8, 8, 10, -1, -1, -1]
        r = d.isGameOver(g)
        self.assertEqual(r, 1, "Game should be over when provinces are over")

    def test_isgameover_three_stacks_over(self):
        g = self.g
        d.endTurn(g)

        # Magically changing supplyCount
        g.supplyCount = [10, 8, 8, 8, 46, 40, 0, 10, 10, 10, 0, 10, 10, 10, 0, 8, 10, -1, -1, -1]
        r = d.isGameOver(g)
        self.assertEqual(r, 1, "Game should be over when any 3 stacks are over")

    def tearDown(self):
        del self.g


class TestScoreFor(unittest.TestCase):
    """
    Testing by adding different cards to deck, hand and discard
    so that most cases are covered
    """

    def setUp(self):
        self.g = d.initializeGame(2, common_kingdom_cards, 0)

    def test_score_after_gameinit(self):
        g = self.g
        r = d.scoreFor(g.whoseTurn, g)
        self.assertEqual(r, 3, "Some problem in scoresFor call at game initilaization")

    def test_with_deck_province(self):
        g = self.g

        # Magically giving victory card to user
        g.discard[g.whoseTurn].append(province)
        g.supplyCount[province] -= 1
        # Now player should have 1 province and 3 estates

        r = d.scoreFor(g.whoseTurn, g)
        self.assertEqual(r, 9, "Some problem in scoresFor call")

    def test_with_hand_curse(self):
        g = self.g

        # Magically giving card to user
        for j in xrange(4):
            g.hand[g.whoseTurn].append(curse)
        g.supplyCount[curse] -= 4

        # Now player should have 4 curses and 3 estates = -1 score
        r = d.scoreFor(g.whoseTurn, g)
        self.assertEqual(r, -1, "Some problem in scoresFor call")

    def test_with_deck_gardens(self):
        g = self.g

        # Magically giving card to user
        for j in xrange(2):
            # This time appending to deck instead of hand
            g.deck[g.whoseTurn].append(gardens)
        g.supplyCount[gardens] -= 2

        # Now player should have 2 gardens, 3 estates and total 12 cards
        r = d.scoreFor(g.whoseTurn, g)
        #print r
        self.assertEqual(r, 5, "Some problem in scoresFor with gardens")


class TestGetWinners(unittest.TestCase):
    """
    Gets the score of each player at the end of the game and sees if there are any winners.
    Note: Winners can be evaluated anytime. It is not necessary for isGameOver to be true.
    """
    def setUp(self):
        self.g = d.initializeGame(2, common_kingdom_cards, 0)

    def test_init_winners(self):
        g = self.g
        players = []        # This should be modified by getWinners function
        r = d.getWinners(players, g)
        self.assertSequenceEqual(players, [0, 1], "Some problem with judging winners")


####################### TESTS FOR LOWER LEVEL  FUNCTIONS ########################
# TODO

if __name__ == '__main__':
    unittest.main()