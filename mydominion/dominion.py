"""
Pranjal Mittal

Useful points about the code:
* supply positions and card types are same. For example, card estate (value 1)
  is at supplyPos = 1. So, estate = supplyPos = 1
"""

from cardnames import *
from math import floor
import random
from copy import deepcopy

# Setting DEBUG to False by default
DEBUG = False

MAX_PLAYERS = 4
MAX_DECK = 500
MAX_HAND = 500


class Game():
    def __init__(self, numPlayers):
        self.numPlayers = numPlayers
        self.supplyCount = [-1] * NCARDS
        self.embargoTokens = [-1] * NCARDS
    
        self.outpostPlayed = 0
        self.outpostTurn = 0
        self.whoseTurn = 0
        self.phase = 0
    
        # Play area variables
        self.numActions = 0  # Starts at 1 each turn
        self.coins = 0       # Number of coins played
        self.numBuys = 0     # Starts at 1 each turn
    
        # Each player has a deck, discard and hand
        # http://stackoverflow.com/questions/12791501/python-initializing-a-list-of-lists
        self.deck = [[] for i in  xrange(MAX_PLAYERS)]
        self.discard = [[] for i in  xrange(MAX_PLAYERS)]
        self.hand = [[] for i in  xrange(MAX_PLAYERS)]
    
        self.playedCards = [-1] * MAX_DECK
        self.playedCardCount = 0

# Game object which maintains game state is kept as a global varaiable.
g = None


##################### UTILITY FUNCTIONS AND STRUCTURES ###################
##########################################################################

def drawCard(player, g):
    """
    Take one card from the **deck** and put it into hand for @player

    :param g:
    @player: An integer which tells teh player number
    @g: Game object
    """
    # Case 1: Deck is empty
    if (len(g.deck[player]) <= 0):

        # Step 1: Move discard pile to deck and shuffle it.
        g.deck[player] = deepcopy(g.discard[player])
        g.discard[player] = []

        # Shufffle the deck of the player
        shuffle(player, g)  # Shuffle the deck up and make it so that we can draw
       
        # Step 2 Draw Card

        # If the deck still has 0 cards, return -1
        if (len(g.deck[player]) == 0):
            return -1

        g.hand[player].append(g.deck[player].pop())   # Add card to hand

    # Case 2: Deck is not empty
    else:
        g.hand[player].append(g.deck[player].pop())   # Add card to hand

    return 0


def gainCard(supplyPos, g, toFlag, player):
    """
    @player gains a card from **supply** to one of the of follo.
    (to which of these depends on @toFlag)
    :param g:
    * to discard (Most common)            :@toFlag = 0
    * to hand (Some cards like Mine)      :@toFlag = 1
    * to deck (Less common, beauraucrat)  :@toFlag = 2
    """
    # Note: supplyPos is number of the chosen card from the supply.
  
    # Check if supply pile is empty (0) or card is not used in game (-1)
    if (g.supplyCount[supplyPos] < 1):
        return -1

    # Added card for [whoseTurn] current player:
    # toFlag = 0 : add to discard
    # toFlag = 1 : add to deck
    # toFlag = 2 : add to hand

    if (toFlag == 1):
        g.deck[player].append(supplyPos)

    elif (toFlag == 2):
        g.hand[player].append(supplyPos)

    else:
        g.discard[player].append(supplyPos)
  
    # Decrease number in supply pile
    g.supplyCount[supplyPos] -= 1
   
    return 0



def discardCard(handPos, g, player=None, toFlag=0):
    """
    Discard a card from the **hand** to discard pile or trash pile
    for current player.

    :param g:
    @toFlag: If 0, discard to discard pile
             If 1, discard to trash
    """
    if not player:
        player = g.whoseTurn
    try:
        card = g.hand[player][handPos]

        if toFlag == 0:
            g.discard[player].append(card)

        del g.hand[player][handPos]
    except:
        return -1
    return 0


def updateCoins(player, g, bonus=0):
    """
    Reads the current hand of the player and calculates
    net playable coins.

    :param g:
    @player: Integer which represents the player
    @g: The game object
    @bonus: This is 0 unless passed
    """
    # Reset coin count
    g.coins = 0

    # Add coins for each Treasure card in player's hand
    for card in g.hand[player]:
        if (card == copper):
            g.coins += 1

        elif (card == silver):
            g.coins += 2

        elif (card == gold):
            g.coins += 3

    # Add bonus
    g.coins += bonus
    return 0

def isGameOver(g):
    """
    Returns 1 if the game is over, else returns 0
    """
    # If stack of Province cards is empty, the game ends
    if (g.supplyCount[province] == 0):
        return 1

    # If atleast three supply piles are at 0, the game ends
    j = 0
    for i in range(last_card):
        if (g.supplyCount[i] == 0):
            j+= 1

    if (j >= 3):
        return 1

    return 0


def get_scores(g):
    """
    Get score for each player. Returns tuple containing,
    player_scores and highScore.
    """
    currentPlayer = g.whoseTurn
    player_scores = []

    # Get score for each player
    for i in range(g.numPlayers):
        player_scores.append(scoreFor(i, g))

    highScore = max(player_scores)

    # Add 1 to player score for players who had less turns
    currentPlayer = g.whoseTurn
    for i in range(g.numPlayers):
        if ( player_scores[i] == highScore and i > currentPlayer):
            player_scores[i] += 1

    highScore = max(player_scores)
    return (tuple(player_scores), highScore)


################## SECONDARY UTILITY FUNCTIONS ###################
##################################################################

def getCost(card_number):
    """
    Returns the cost of the @card.
    @card: Is an integer representing the card
    """
    return CARD_COST[card_number]

def supplyCount(card, g):
    return g.supplyCount[card]


################### API FUNCTIONS ######################
########################################################

def shuffle(player, g):
    """
    Shuffles the deck for the player @player
    :param g:
    """
    if (len(g.deck[player]) == 0):
        # If the player has no cards in his deck
        return -1

    # Sort cards in deck to ensure determinism
    g.deck[player].sort()
    #XXX: Why are we doing a sort?

    # Shuffle function in python does in place shuffling
    random.shuffle(g.deck[player])

    return 0

def initializeGame(numPlayers, kingdomCards, randomSeed):
    """
    Responsible for initializing all supplies, and shuffling deck and
    drawing starting hands for all players.  Check that 10 cards selected
    are in fact (different) kingdom cards, and that numPlayers is valid. 

    @numPlayers: int
    @kingdomCards: List of 10 kingdomCards
    @randomSeed: Useful for shuffling
    """

    if numPlayers < 2 or numPlayers > MAX_PLAYERS:
        return -1

    kingdomcard_set = set(kingdomCards)
    if not len(set(kingdomCards)) == 10:
        if DEBUG:
            print("All cards must be distinct")
        return -1

    if not kingdomcard_set.issubset(allowed_kingdomcard_set):
        if DEBUG:
            print("One or more of kingdom cards passed are not implemented")
        return -1

    random.seed(randomSeed)
    g = Game(numPlayers)

    ##################################################
    ### Set supplies
    ##################################################

    # Set number of Curse cards
    if (numPlayers == 2):
        g.supplyCount[curse] = 10
    elif (numPlayers == 3):
        g.supplyCount[curse] = 20
    else:
        g.supplyCount[curse] = 30

    # Set number of Victory cards
    if (numPlayers == 2):
      g.supplyCount[estate] = 8
      g.supplyCount[duchy] = 8
      g.supplyCount[province] = 8
    else:
      g.supplyCount[estate] = 12
      g.supplyCount[duchy] = 12
      g.supplyCount[province] = 12

    # Set number of Treasure cards
    g.supplyCount[copper] = 60 - (7 * numPlayers)
    g.supplyCount[silver] = 40
    g.supplyCount[gold] = 30

    # Set number of Kingdom cards
    for i in range(adventurer, last_card+1):
        for j in range(10):
            if (kingdomCards[j] == i):
                # Check if card is a 'Victory' Kingdom card
                if (kingdomCards[j] == great_hall or kingdomCards[j] == gardens):
                    if (numPlayers == 2):
                        g.supplyCount[i] = 8
                    else:
                        g.supplyCount[i] = 12
                else:
                    g.supplyCount[i] = 10

                break
            else:
                g.supplyCount[i] = -1

    ##################################################
    ### Initialze deck, hand, etc for each player
    ##################################################

    # Initilize each players hand to empty
    # Initial deck of each player has 3 estates and 7 coppers
    for p in range(numPlayers):

        # Initialize hand size to 0
        g.hand[p] = []

        for j in range(3):
            g.deck[p].append(estate)

        for j in range(3, 10):
            g.deck[p].append(copper)

    # Shuffle the deck of each player now
    for i in range(numPlayers):
        if (shuffle(i, g) < 0):
            return -1

    # Set embargo tokens to 0 for all supply piles
    for i in range(NCARDS):
        g.embargoTokens[i] = 0

    for i in range(numPlayers):
        # Draw 5 cards in hand for all players
        for it in range(5):
            drawCard(i, g)

    ##################################################
    ### Initialze first player's turn
    ##################################################

    # Initialize first player's turn
    g.outpostPlayed = 0
    g.phase = 0
    g.numActions = 1
    g.numBuys = 1
    g.playedCardCount = 0
    g.whoseTurn = 0


    # When the game is initlized we are sure that there are no action cards.
    # So we directly go to buy phase
    updateCoins(g.whoseTurn, g, 0)

    return g


def playCard(handPos, choice1, choice2, choice3, g):
    """
    Play card at position handPos from the current player's hand.
    (g.whoseTurn returns the current_player)
    
    If any card is added to hand after playing this card coins are updated.
    """
    coin_bonus = 0     # tracks coins gain from actions

    #  Check if it is the right phase
    if (g.phase != 0):
        return -1

    # Check if player has enough actions
    if (g.numActions < 1):
        return -1

    # Get card played
    current_player = g.whoseTurn
    card = g.hand[current_player][handPos]

    if DEBUG:
        print("Player %d is playing %s"%(g.whoseTurn, CARD_NAMES[card]))

    # If selected card is not an action then don't allow playing card
    if (card < adventurer or card > last_card):
        return -1
        # garden is still a card which is not playable but not excluded yet.

    #XXX: This is an important function
    if (cardEffect(card, choice1, choice2, choice3, g, handPos, coin_bonus) < 0):
        return -1

    # reduce number of actions
    g.numActions -= 1

    # update coins (Treasure cards may be added with card draws)
    updateCoins(g.whoseTurn, g, coin_bonus)

    return 0


def buyCard(supplyPos, g):
    """
    Let current player buy a card from supply.
    :param g:
    @supplyPos: The player will choose a supply position to buy the card from.
    """
    who = g.whoseTurn

    if (g.numBuys < 1):
        if (DEBUG):
            print("You do not have any buys left")
        return -1
 
    elif (g.supplyCount[supplyPos] < 1):
        if (DEBUG):
            print("There are not any of that type of card left")
        return -1

    elif (g.coins < CARD_COST[supplyPos]):
        if (DEBUG):
            print("Player %d does not have enough money to buy *%s*. You have %d coins."%(g.whoseTurn, CARD_NAMES[supplyPos], g.coins))
        return -1

    else:
        g.phase = 1
        gainCard(supplyPos, g, 0, who)  # card goes in discard, this might be wrong.. (2 means goes into hand, 0 goes into discard)

        # Coins used up equal to the cost of the card being bought
        g.coins -= CARD_COST[supplyPos]
        g.numBuys -= 1

        if (DEBUG):
            print("Player %d bought *%s* for %d coins. You now have %d buys and %d coins."%(g.whoseTurn, CARD_NAMES[supplyPos], CARD_COST[supplyPos], g.numBuys, g.coins))

    return 0


def numHandCards(g):
    """
    Outputs integer containing number of cards current player
    has in hand.
    :param g:
    """
    return len(g.hand[g.whoseTurn])


def handCard(handPos, g):
    """
    Enum value of card in player's hand 
    """
    currentPlayer = g.whoseTurn
    return g.hand[currentPlayer][handPos]


def supplyCount(card):
    """
    How many of given card are left in supply
    """
    return g.supplyCount[card]


def fullDeckCount(player, card, g):
    """
    Counts the number of copies of a card a player has.
    Here deck = hand + discard + deck
    """
    count = 0

    for c in g.deck[player]:
        if (c == card):
            count+= 1

    for c in g.hand[player]:
        if (c == card):
            count+= 1

    for c in g.discard[player]:
        if (c == card):
            count+= 1

    return count


def count_all_player_cards(player, g):
    """
    hand + discard + deck of a player
    """
    count = 0

    for c in g.deck[player]:
            count+= 1

    for c in g.hand[player]:
            count+= 1

    for c in g.discard[player]:
            count+= 1

    return count


def whoseTurn(g):
    """
    Returns the player number whose turn is active
    :param g:
    """
    return g.whoseTurn


def endTurn(g):
    """
    Ends the turn of the active player. Puts all cards in hand to discard pile.
    :param g:
    """
    currentPlayer = g.whoseTurn

    # Discard hand (Put hand to discard pile)
    hand_count = len(g.hand[currentPlayer])
    for c in g.hand[currentPlayer]:
        g.discard[currentPlayer].append(c)   # Discard
    g.hand[currentPlayer] = []              # Reset hand

    # Draw 5 cards as the new hand of this player.
    for k in range(5):
        drawCard(g.whoseTurn, g)

    # Code for determining the player
    if (currentPlayer < (g.numPlayers - 1)):
        g.whoseTurn = currentPlayer + 1     # Still safe to increment

    else:
        g.whoseTurn = 0     # Max player has been reached, loop back around to player 1


    g.outpostPlayed = 0
    g.phase = 0
    g.numActions = 1
    g.coins = 0
    g.numBuys = 1
    g.playedCardCount = 0

    # Update playable money
    updateCoins(g.whoseTurn, g, 0)

    if DEBUG:
        # Print new hand after turn ends
        print "------------------------"
        # Print the hand of next player
        D.hand(g)
    return 0


def isGameOver(g):
    """
    Returns 1 if the game is over else returns 0.
    """
    # If stack of Province cards is empty, the game ends
    if (g.supplyCount[province] == 0):
        return 1

    # If atleast three supply piles are at 0, the game ends
    j = 0
    for i in range(last_card):
        if (g.supplyCount[i] == 0):
            j+= 1

    if (j >= 3):
        return 1

    return 0


def scoreFor(player, g):
    """
    Negative here does not mean invalid; scores may be negative,
    -9999 means invalid input
    """
    score = 0
    # score from hand
    for i in range(0, len(g.hand[player])):

        if (g.hand[player][i] == curse):
            score = score - 1

        if (g.hand[player][i] == estate):
            score = score + 1

        if (g.hand[player][i] == duchy):
            score = score + 3

        if (g.hand[player][i] == province):
            score = score + 6

        if (g.hand[player][i] == great_hall):
            score = score + 1

        if (g.hand[player][i] == gardens):
            score += (fullDeckCount(player, gardens, g) * count_all_player_cards(player, g) / 10)

    # score from discard
    for i in range(0, len(g.discard[player])):

        if (g.discard[player][i] == curse):
            score = score - 1

        if (g.discard[player][i] == estate):
            score = score + 1

        if (g.discard[player][i] == duchy):
            score = score + 3

        if (g.discard[player][i] == province):
            score = score + 6

        if (g.discard[player][i] == great_hall):
            score = score + 1

        if (g.discard[player][i] == gardens):
            score += (fullDeckCount(player, gardens, g) * count_all_player_cards(player, g) / 10)

    # score from deck
    for i in range(0, len(g.deck[player])):

        if (g.deck[player][i] == curse):
            score = score - 1

        if (g.deck[player][i] == estate):
            score = score + 1

        if (g.deck[player][i] == duchy):
            score = score + 3

        if (g.deck[player][i] == province):
            score = score + 6

        if (g.deck[player][i] == great_hall):
            score = score + 1

        if (g.deck[player][i] == gardens):
            score += (count_all_player_cards(player, g) / 10)

    return score


def getWinners(players, g):
    """
    Gets the score of each player at the end of the game and sees if
    there are any winners.

    @player: The list passed in is modified to get player scores of each player.
    """
    player_scores, highScore = get_scores(g)
    player_scores = list(player_scores)
    # Set winners in array to 1 and rest to 0
    for i in range(g.numPlayers):
        if (player_scores[i] == highScore):
            players.append(1)
        else:
            players.append(0)

    return 0


################# CARD EFFECT FUNCTIONS AND IMPLEMENTATION #################
############################################################################

def cardEffect(card, choice1, choice2, choice3, g, handPos, bonus):
    """
    Carries out the effect of an action card played
    """
    currentPlayer = g.whoseTurn
    nextPlayer = currentPlayer + 1

    tributeRevealedCards = [-1, -1]
    temphand = []
    if (nextPlayer > (g.numPlayers - 1)):
        nextPlayer = 0

    if card == adventurer:
        """
        Reveal cards from your deck until you reveal 2 Treasure cards.
        Put those Treasure cards in your hand and discard the other revealed cards.
        """
        # discard adventurer from hand before adding new cards to hand
        discardCard(handPos, g, currentPlayer, 0)
        drawntreasure = 0

        while True:
            if drawntreasure == 2:
                break
            if not g.deck[currentPlayer]:  # If the deck is empty we need to take discard pile, shuffle it and add to deck
                shuffle(currentPlayer, g)
            else:
                card_from_deck = g.deck[currentPlayer].pop()
            if (card_from_deck == copper or card_from_deck == silver or card_from_deck == gold):
                # If the card is a treasure put it to hand
                g.hand[currentPlayer].append(card_from_deck)
                drawntreasure += 1
            else:
                # Put the card back in discard pile
                g.discard[currentPlayer].append(card_from_deck)

        return 0

    elif card == ambassador:
        """
        Reveal a card from your hand.
        Return up to 2 copies of it from your hand to the Supply.
        Then each other player gains a copy of it.

        @choice1 = hand#
        @choice2 = number to return to supply
        """
        j = 0    # Used to check if player has enough cards to discard

        if (choice2 > 2 or choice2 < 0):
            return -1

        if (choice1 == handPos):
            return -1

        for i in range(len(g.hand[currentPlayer])):
            if (i != handPos and i == g.hand[currentPlayer][choice1] and i != choice1):
                j += 1

        if (j < choice2):
            return -1

        if DEBUG:
            print("Player %d reveals card number: %d"%(currentPlayer, g.hand[currentPlayer][choice1]))

        # Increase supply count for choosen card by amount being discarded
        g.supplyCount[g.hand[currentPlayer][choice1]] += choice2

        # Each other player gains a copy of revealed card
        for i in range(g.numPlayers):
            if (i != currentPlayer):
                gainCard(g.hand[currentPlayer][choice1], g, 0, i)

        # Discard played card from hand
        discardCard(handPos, g, currentPlayer, 0)

        # Trash copies of cards returned to supply
        for j in range(choice2):
            for i in range (len(g.hand[currentPlayer])):
                if (g.hand[currentPlayer][i] == g.hand[currentPlayer][choice1]):
                    discardCard(i, g, currentPlayer, 1)
                    break
        return 0

    elif card == baron:
        """
        You may discard an Estate card. If you do, +4 coin credit. Otherwise, gain an Estate card.
        @choice1: hand# of estate
        """
        choice_card = g.hand[currentPlayer][choice1]
        g.numBuys+=1
        if choice_card == estate and choice_card in g.hand[g.whoseTurn]:
            discardCard(choice1, g, currentPlayer, 0)
            updateCoins(g.whoseTurn, g, 4)
        else:
            to_discard = 0
            gainCard(estate, g, to_discard, g.whoseTurn)

        return 0

    elif card == council_room:
        # +4 Cards +1 Buy
        council_room_test(currentPlayer, g, handPos)
        return 0

    if card == cutpurse:
        """
        Each other player discards a Copper card (if any).
        """
        for p in xrange(g.numPlayers):
            if p != g.whoseTurn:
                for hpos, card in enumerate(g.hand[p]):
                    if card == copper:
                        discardCard(hpos, g, p, 0)
                        break # Becase we want to discard only one copper from each player
        return 0

    elif card == embargo:
        """
        When a player buys a card, he gains a Curse card per Embargo token on that pile.
        choice1 = supply_pos#
        """
        # +2 Coins
        g.coins += 2
        choice_card = choice1  # Supply position and card values are on 1-1 mapping.

        # If the selected pile is not in play.
        if (g.supplyCount[choice_card] == -1):
            return -1

        discardCard(handPos, g, g.whoseTurn, 1)
        g.embargoTokens[choice_card] += 1
        return 0

    elif card == feast:
        """
        Trash this card. Gain a card costing up to (5)
        choice1 = supply# of card
        """
        if choice1 != handPos and getCost(choice1) <= 5:
            # Trash the feast
            trash_flag = 1
            r = discardCard(handPos, g, g.whoseTurn, trash_flag)
            if r != 0:
                return -1
            r = gainCard(choice1, g, 0, g.whoseTurn)
            if r != 0:
                return -1
        else:
            return -1
        return 0

    elif card == gardens:
        return -1

    elif card == great_hall:
        """
        +1 card, +1 action
        """
        drawCard(currentPlayer, g)
        g.numActions += 1
        discardCard(handPos, g, currentPlayer, 0)

        return 0

    elif card == mine:
        """
        Choice1 is hand# of money to trash, choice2 is supply# of
        money to put in hand
        """
        j = g.hand[currentPlayer][choice1]  # store card we will trash

        convert_card = g.hand[currentPlayer][choice1]
        # If not a treasure card
        if convert_card not in [copper, silver, gold]:
            return -1

        if choice2 not in [copper, silver, gold]:
            return -1

        if not (CARD_COST[choice2] <= CARD_COST[convert_card] + 3):
            return -1

        gainCard(choice2, g, 2, currentPlayer)

        # Discard card from hand
        discardCard(handPos, g, currentPlayer, 0)

        # Discard trashed card
        for i in range(len(g.hand[currentPlayer])):
            if (g.hand[currentPlayer][i] == j):
                discardCard(i, g, currentPlayer, 0)
                break

        return 0

    ################## OPTIONAL CARDS START HERE ##################
    elif card == remodel:
        return remodel_test(currentPlayer, g, handPos, choice1, choice2)

    elif card == smithy:
        # MY_CHOICE (PRANJAL)
        # +3 Cards
        for i in range(3):
            drawCard(currentPlayer, g)

        # discard smithy from hand since it has been played
        discardCard(handPos, g, currentPlayer, 0)
        return 0

    elif card == village:
        # MY_CHOICE (PRANJAL)
        village_test(currentPlayer, g, handPos)
        return 0

    return -1


def council_room_test(currentPlayer, g, handPos):
    for i in range(5):
        drawCard(currentPlayer, g)

    # +1 Buy
    g.numBuys+= 1

    # Each other player draws a card
    for i in range(g.numPlayers):
        if ( i != currentPlayer ):
            drawCard(i, g)

    # put played card in played card pile
    discardCard(handPos, g, currentPlayer, 0)
    return 0


def remodel_test(currentPlayer, g, handPos, choice1, choice2):
    """
    Trash a card from your hand. Gain a card costing up to (2) more than the trashed card.
    choice1 is hand# of card to remodel, choice2 is supply#
    """
    j = g.hand[currentPlayer][choice1]  # store card we will trash

    if ((getCost(g.hand[currentPlayer][choice1]) + 2) > getCost(choice2)):
        return 1

    gainCard(choice2, g, 0, currentPlayer)

    # Discard card from hand
    discardCard(handPos, g, currentPlayer, 0)

    # Discard trashed card
    for i in range(len(g.hand[currentPlayer])):
        if (g.hand[currentPlayer][i] == j):
            discardCard(i, g, currentPlayer, 0)
            break

    return 0


def village_test(currentPlayer, g, handPos):
    """
    +1 card, +2 actions
    """
    drawCard(currentPlayer, g)
    g.numActions = g.numActions + 2
    discardCard(handPos, g, currentPlayer, 0)

    return 0
