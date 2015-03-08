"""
Pranjal Mittal

Partially random tests. Not all test units are random but most are.
"""

import random
import unittest
import dominion as d
from cardnames import *

common_kingdom_cards = [adventurer, ambassador, baron, council_room, cutpurse,
                                embargo, feast, gardens, great_hall, mine]

pranjal_kingdom_cards = [adventurer, ambassador, baron, council_room, cutpurse,
                                embargo, feast, remodel, smithy, village]

all_kingdom_cards = [adventurer, ambassador, baron, council_room, cutpurse,
                     embargo, feast, gardens, great_hall, mine,
                     remodel, smithy, village]

###################### TESTS FOR TOP LEVEL API FUNCTIONS ########################
#################################################################################

class TestInitializeGame(unittest.TestCase):

    def test_random_numPlayers(self):

        # Running 10 tests
        for t in xrange(10):
            # 2 is valid number of players
            numPlayers = random.randint(0,5)
            g = d.initializeGame(numPlayers, [adventurer, ambassador, smithy, council_room, cutpurse,
                                    embargo, feast, gardens, great_hall, mine], 0)
            if numPlayers in [2, 3, 4]:
                self.assertEqual(g, 0, "Failed for numPlayers=%d"%(numPlayers,))
            else:
                self.assertEqual(g, 1, "Failed for numPlayers=%d"%(numPlayers,))

    def test_random_no_kindgomcards(self):

        for t in xrange(10):
            sample_size = random.randint(9,12)
            kingdom_cards = random.sample(all_kingdom_cards, sample_size)

            g = d.initializeGame(2, kingdom_cards , 0)
            if sample_size == 10:
                self.assertEqual(g, 0)
            else:
                self.assertEqual(g, -1)

    def test_initial_supply(self):
        g = d.initializeGame(2, common_kingdom_cards, 0)

        valid_supply = [10, 8, 8, 8, 46, 40, 30, 10, 10, 10, 10, 10, 10, 10, 8, 8, 10, -1, -1, -1]
        self.assertSequenceEqual(g.supplyCount, valid_supply, "Invalid supply: %s"%(str(g.supplyCount),))


class TestBuyCard(unittest.TestCase):

    def test_buycard_not_enough_coins(self):

        for t in xrange(10):
            g = d.initializeGame(2, common_kingdom_cards, 0)
            coins = g.coins
            # Just after game is initialized. Any of the players cannot have more than 5 cards in hand.
            # Adventurer costs 6. So buyCard should fail.
            self.assertLessEqual(g.coins, 6, "Player %d has more coins than expected"%(g.whoseTurn,))

            non_buyable_cards = [c for c, cost in CARD_COST.items() if cost > coins]
            card = random.choice([])
            r = d.buyCard(adventurer, g)
            self.assertEqual(r, -1, "Player was able to buy adventurer costing 6 with only %d coins"%(g.coins))

    def test_if_buyable_cards_can_be_bought(self):

        for t in xrange(10):
            g = d.initializeGame(2, common_kingdom_cards, 0)
            coins = g.coins
            buyable_cards = [c for c, cost in CARD_COST.items() if cost <= coins]
            random_buyable_card = random.choice(buyable_cards)
            if random_buyable_card:
                r = d.buyCard(self.random_buyable_card, g)
                self.assertEqual(r, 0)


class TestNumHandCards(unittest.TestCase):

    def test_num_hand_cards_after_initialize(self):
        # Number of cards in hand should always be 5 irrespective of seed and number of players.
        # And also irrespective of whose turn it is.
        for t in xrange(10):
            seed = random.randint(0, 10)
            numPlayers = random.randint(0,5)

            g = d.initializeGame(numPlayers, common_kingdom_cards, seed)

            # Checking hand size for random player
            g.whoseTurn = random.randint(0, numPlayers)

            r = d.numHandCards(g)
            self.assertEqual(r, 5, "Failed for numPlayers=%d"%(numPlayers,))


class TestHandCard(unittest.TestCase):

    def test_hand_card(self):
        # If initialized with seed = 0, card at index pos 0 must be copper
        g = d.initializeGame(2, common_kingdom_cards, 0)
        r = d.handCard(0, g)
        self.assertEqual(r, 4, "handCard did not work as expected")


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

    def test_after_adding_a_card_random_times(self):
        all_cards = CARD_COST.keys()

        for t in xrange(10):
            g = d.initializeGame(2, common_kingdom_cards, 0)

            valid_cards = [card for card in all_cards if supplyCount[card] > 0]
            random_valid_card = random.choice(valid_cards)

            initial_count = d.fullDeckCount(g.whoseTurn, random_valid_card, g)

            ntimes = random.randint(1, supplyCount[random_valid_card]+1)

            for time in range(ntimes):
                g.deck[g.whoseTurn].append(random_valid_card)

            r = d.fullDeckCount(g.whoseTurn, random_valid_card, g)
            self.assertEqual(r, ntimes + initial_count)

    def tearDown(self):
        del self.g


class TestPlayCard(unittest.TestCase):

    #XXX: Play card not randomized yet. Each card has a different test.
    # How to test a random card then?

    def setUp(self):
        self.g = d.initializeGame(2, common_kingdom_cards, 0)
        self.P = self.g.whoseTurn        # Current player

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

    def test_play_garden(self):
        g = self.g
        # Add card to hand of current player by magic.
        g.hand[g.whoseTurn].append(gardens)

        len_hand = len(g.hand[g.whoseTurn])

        r = d.playCard(len_hand-1, None, None, None, g)
        self.assertEqual(r, -1, "Garden cannot be played")


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

    def test_num_hand_cards_after_random_turns(self):

        g = d.initializeGame(2, common_kingdom_cards, 0)
        random_turns = random.randint(0, 10)
        for t in xrange(random_turns):
            r = d.whoseTurn(g)
            if random_turns%2 == 0:
                self.assertEqual(r, 0, "After even end turns it should be player 0's turn for 2 players")
            else:
                self.assertEqual(r, 1)


class TestEndTurn(unittest.TestCase):

    def test_check_player_changes(self):

        for t in xrange(10):
            numPlayers = random.randint(2, 4)
            g = d.initializeGame(numPlayers, common_kingdom_cards, 0)

            # Initially player is 0
            self.assertEqual(g.whoseTurn, 0, "It should be Player 0's turn just after initializing game")

            r = d.endTurn(g)
            self.assertEqual(r, 0, "endTurn did not complete successfully")

            # If end turn ran succesfully, player must have changed
            self.assertEqual(g.whoseTurn, 1, "endTurn did not complete successfully")

            if numPlayers > 2:
                r = d.endTurn(g)
                self.assertEqual(r, 0, "endTurn did not complete successfully")
                self.assertEqual(g.whoseTurn, 2, "endTurn did not complete successfully")

            if numPlayers > 3:
                r = d.endTurn(g)
                self.assertEqual(r, 0, "endTurn did not complete successfully")
                self.assertEqual(g.whoseTurn, 3, "endTurn did not complete successfully")

                r = d.endTurn(g)
                self.assertEqual(r, 0, "endTurn did not complete successfully")
                self.assertEqual(g.whoseTurn, 4, "endTurn did not complete successfully")


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
        self.assertEqual(r, 0)

    def test_isgameover_after_province_over(self):
        g = self.g

        # Magically changing supplyCount
        g.supplyCount = [10, 8, 8, 0, 46, 40, 30, 10, 10, 10, 10, 10, 10, 10, 8, 8, 10, -1, -1, -1]
        r = d.isGameOver(g)
        self.assertEqual(r, 1, "Game should be over when provinces are over")

    def test_isgameover_random_three_stacks_over(self):

        for t in xrange(10):
            g = d.initializeGame(2, common_kingdom_cards, 0)
            d.endTurn(g)

            g.supplyCount = [10, 8, 8, 8, 46, 40, 0, 10, 10, 10, 0, 10, 10, 10, 0, 8, 10, -1, -1, -1]

            three_stacks = random.sample(len(g.supplyCount), 3)

            # Making any 3 stacks over
            for stack in three_stacks:
                g.supplyCount[stack] = 0

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