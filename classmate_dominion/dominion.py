"""
Classmate onid: kollipal

Some errors: g.coin_bonus referenced even though it does not exisit.
"""

import random
DEBUG = True
MAX_PLAYERS = 4
MAX_DECK = 10
MAX_HAND = 10
MAX_CARDS = 27


curse = 0
estate = 1
duchy = 2
province = 3
copper = 4
silver = 5
gold = 6
adventurer = 7
ambassador = 8
baron = 9
council_room = 10
cutpurse = 11
embargo = 12
feast = 13
gardens = 14
great_hall = 15
mine = 16
minion = 17
outpost = 18
remodel = 19
salvager = 20
sea_hag = 21
smithy = 22
steward = 23
treasure_map = 24
tribute = 25
village = 26

class Game():
    numPlayers =2
    supplyCount = [-1] * MAX_CARDS
    embargoTokens = [-1] * MAX_CARDS
    outpostPlayed = 0
    outpostTurn = 0
    whoseTurn = 0
    phase = 0
    bonus = 0
    numActions = 0  
    coins = 0    
    numBuys = 0
    kingdomCards = []
    deck = {}
    deckCount = [0] * MAX_PLAYERS
    discard = {}
    discardCount = [0] * MAX_PLAYERS
    hand = {}
    handCount = [0] * MAX_PLAYERS
    playedCards = []
    playedCardCount = 0


def initializeGame(numPlayers, kingdomCards, randomSeed):
    game = Game()
    game.numPlayers = numPlayers
    if numPlayers > MAX_PLAYERS or numPlayers < 2:
        return -1
    random.seed(randomSeed)
    game.kingdomCards = kingdomCards
    if len(kingdomCards) > 10:
        return -1
    for i in range(10):
        if kingdomCards[i] not in [adventurer, ambassador, baron ,council_room ,cutpurse ,embargo ,feast ,gardens ,great_hall ,mine ,minion ,outpost ,remodel ,salvager ,sea_hag ,smithy ,steward ,treasure_map, tribute, village]:
            return -1;
    for i in range(10):
        for j in range(10):
            if j != i and kingdomCards[i] == kingdomCards[j]:
                return -1
    if (numPlayers == 2):
        game.supplyCount[curse] = 10
    elif (numPlayers == 3):
        game.supplyCount[curse] = 20
    else:
        game.supplyCount[curse] = 30
    if (numPlayers == 2):
      game.supplyCount[estate] = 8
      game.supplyCount[duchy] = 8
      game.supplyCount[province] = 8
    else:
      game.supplyCount[estate] = 12
      game.supplyCount[duchy] = 12
      game.supplyCount[province] = 12
    game.supplyCount[copper] = 60 - (7 * numPlayers)
    game.supplyCount[silver] = 40
    game.supplyCount[gold] = 30
    for i in range(adventurer,MAX_CARDS):
        for j in range(10):
            if (kingdomCards[j] == i):
                if (kingdomCards[j] == great_hall or kingdomCards[j] == gardens):
                    if (numPlayers == 2):
                        game.supplyCount[i] = 8
                    else:
                        game.supplyCount[i] = 12
                else:
                    game.supplyCount[i] = 10

                break
            else:
                game.supplyCount[i] = -1

    for i in range(numPlayers):
        game.deckCount[i] = 0
        game.deck[i] = []
        game.hand[i] = []
        game.discard[i] = []

        for j in range(3):
            game.deck[i].append(estate)
            game.deckCount[i] += 1
        for j in range(3, 10):
            game.deck[i].append(copper)
            game.deckCount[i] += 1
    for i in range(numPlayers):
        shuffle(i, game)
    for i in range(numPlayers):
        game.handCount[i] = 0
        game.discardCount[i] = 0
    for i in range(village):
        game.embargoTokens[i] = 0

    game.outpostPlayed = 0
    game.phase = 0
    game.numActions = 1
    game.numBuys = 1
    game.playedCardCount = 0
    game.whoseTurn = 0
    game.handCount[game.whoseTurn] = 0     
    for it in range(5):
        drawCard(game.whoseTurn, game)
    updateCoins(game.whoseTurn, game, 0)
    return game

def shuffle(player, g):
    if (g.deckCount[player] < 1):
        return -1
    g.deck[player].sort()
    random.shuffle(g.deck[player])
    return 0


def drawCard(player, g):
    if (g.deckCount[player] <= 0):
        g.deck[player] = g.discard[player]
        g.discard[player] = []
        g.deckCount[player] = g.discardCount[player]
        g.discardCount[player] = 0 
        shuffle(player, g) 
        g.discardCount[player] = 0
        count = g.handCount[player] 
        deckCounter = g.deckCount[player] 
        if (deckCounter == 0):
            return -1
        g.hand[player].append(g.deck[player][deckCounter - 1])
        g.deck[player].pop(deckCount[player]-1)
        g.deckCount[player] -= 1
        g.handCount[player] += 1
    else:
        count = g.handCount[player]     
        deckCounter = g.deckCount[player]       
        g.hand[player].append(g.deck[player][deckCounter - 1])
        g.deck[player].pop(g.deckCount[player]-1)
        g.deckCount[player] -= 1                            
        g.handCount[player] += 1   

    return 0

def updateCoins(player, g, bonus):
    g.coins = 0
    g.bonus+= bonus
    for card in g.hand[player]:
        if (card == copper):
            g.coins += 1

        elif (card == silver):
            g.coins += 2

        elif (card == gold):
            g.coins += 3
    g.coins += bonus
    return 0
def gainCard(supplyPos, g, toFlag, player):
    if g.supplyCount[supplyPos] < 1 :
        return -1
    if (toFlag == 1):
        g.deck[player].append(supplyPos)
        g.deckCount[player]+=1
        g.supplyCount[supplyPos]-=1
    elif (toFlag == 2):
        g.hand[ player ].append(supplyPos)
        g.handCount[player]+=1
        g.supplyCount[supplyPos]-=1
    else:
        g.discard[player].append(supplyPos)
        g.discardCount[player]+=1
        g.supplyCount[supplyPos]-=1
    return 0

def discardCard(handPos, currentPlayer, g, trashFlag):
    if handPos not in g.hand[currentPlayer]:
        return -1
    else:
        if (trashFlag == 0):
            g.playedCards.append(handPos)
            g.playedCardCount+=1
        elif (trashFlag == 2):
            g.discard[currentPlayer].append(handPos)
            g.discardCount[currentPlayer]+=1
        g.hand[currentPlayer].remove(handPos)
    return 0 ##fixCardHole(handPos, currentPlayer, g)

def buyCard(supplyPos, g):
    if (g.numBuys < 1):
        return -1
    elif (g.supplyCount[supplyPos] <1):
        return -1
    elif (g.coins < getCost(supplyPos)):
        return -1
    else:
        g.phase=1
        gainCard(supplyPos,g, 0, g.whoseTurn)  
        g.coins = (g.coins) - (getCost(supplyPos))
        g.numBuys-=1
        for i in range(g.embargoTokens[supplyPos]):
            gainCard(curse, g, 0, g.whoseTurn)
    return 0

def getCost(cardNumber):
    if cardNumber == curse: return 0
    if cardNumber == estate: return 2
    if cardNumber == duchy: return 5
    if cardNumber == province: return 8
    if cardNumber == copper: return 0
    if cardNumber == silver: return 3
    if cardNumber == gold: return 6
    if cardNumber == adventurer: return 6
    if cardNumber == ambassador: return 3
    if cardNumber == baron: return 4
    if cardNumber == council_room: return 5
    if cardNumber == cutpurse: return 4
    if cardNumber == embargo: return 2
    if cardNumber == feast: return 4
    if cardNumber == gardens: return 4
    if cardNumber == great_hall: return 3
    if cardNumber == mine: return 5
    if cardNumber == minion: return 5
    if cardNumber == outpost: return 5
    if cardNumber == remodel: return 4
    if cardNumber == salvager: return 4
    if cardNumber == sea_hag: return 4
    if cardNumber == smithy: return 4
    if cardNumber == steward: return 3
    if cardNumber == treasure_map: return 4
    if cardNumber == tribute: return 5
    if cardNumber == village: return 3
    else: return -1
def endTurn(g):
    currentPlayer = g.whoseTurn
    g.discard[currentPlayer].extend(g.hand[currentPlayer])
    g.discardCount[currentPlayer]+=1
    g.hand[currentPlayer] = []
    g.handCount[currentPlayer] = 0
    if currentPlayer < (g.numPlayers - 1):
        g.whoseTurn = currentPlayer + 1
    else:
        g.whoseTurn = 0
    g.outpostPlayed = 0
    g.phase = 0
    g.numActions = 1
    g.coins = 0
    g.numBuys = 1
    g.playedCards = []
    g.bonus = 0
    g.playedCardCount = 0
    g.handCount[g.whoseTurn] = 0
    for k in range(5):
        drawCard(g.whoseTurn, g)
    updateCoins(g.whoseTurn, g , 0)
    return 0
def playCard(handPos, choice1, choice2, choice3, g):
    card = g.hand[g.whoseTurn][handPos]
    if (g.phase != 0):
        return -1
    if (g.numActions < 1 ):
        return -1
    if card not in g.kingdomCards:
        return -1
    if card not in g.hand[g.whoseTurn]:
        return -1
    if ( cardEffect(card, choice1, choice2, choice3, g, handPos, g.bonus) < 0 ):
        return -1
    g.numActions-=1
    discardCard(card,g.whoseTurn,g,0)
    updateCoins(g.whoseTurn, g, g.bonus)
    return 0
def cardEffect(card, choice1, choice2, choice3, g, handPos, bonus):
    currentPlayer = g.whoseTurn
    nextPlayer = (g.whoseTurn+1)%g.numPlayers
    tributeRevealedCards = [-1, -1]
    temphand = []
    drawntreasure = 0
    if card == adventurer:
        while(drawntreasure<2):
            if (g.deckCount[currentPlayer] <1):
                    shuffle(currentPlayer, g)
            drawCard(currentPlayer, g)
            cardDrawn = g.hand[currentPlayer][g.handCount[currentPlayer]-1]
            if (cardDrawn == copper or cardDrawn == silver or cardDrawn == gold):
                drawntreasure+=1
            else:
                temphand.append(g.hand[currentPlayer].pop(g.handCount[currentPlayer]-1))
        discardCard(handPos, currentPlayer, g, 0)
        return 0
    elif card == ambassador:
        if g.hand[currentPlayer][choice1] not in g.hand[currentPlayer]:
            return -1
        for i in range(2):
            if g.hand[currentPlayer][choice1] in g.hand[currentPlayer]:
                g.hand[currentPlayer].remove(g.hand[currentPlayer][choice1])
                g.supplyCount[g.hand[currentPlayer][choice1]]+=1
        discardCard(handPos, currentPlayer, g, 0)
        return 0
    elif card == baron:
        g.numBuys+=1
        if (g.hand[currentPlayer][choice1] == estate) and (g.hand[currentPlayer][choice1] in g.hand[currentPlayer]):
            discardCard(g.hand[currentPlayer][choice1],currentPlayer,g,2)
            updateCoins(currentPlayer,g,4)
        else:
            gainCard(estate,g,0,currentPlayer)
        discardCard(handPos, currentPlayer, g, 0)
        return 0
    elif card == council_room:
        for i in range(4):
            drawCard(currentPlayer, g)
        g.numBuys+=1
        for i in range(g.numPlayers):
            if ( i != currentPlayer ):
                drawCard(i, g)
        discardCard(handPos, currentPlayer, g, 0)
        return 0
    elif card == cutpurse:
        updateCoins(currentPlayer, g, 2)
        for i in range(g.numPlayers):
            if (i != currentPlayer):
                if (copper in g.hand[i]):
                    discardCard(copper, i, g, 0)
        discardCard(handPos, currentPlayer, g, 0)
        return 0
    elif card == embargo:
        updateCoins(currentPlayer,g,2)
        if ( g.supplyCount[choice1] == -1 ):
            return -1
        g.embargoTokens[choice1]+=1
        discardCard(handPos, currentPlayer, g, 1)            
        return 0
    elif card == feast:
        if (supplyCount[choice1] <= 0):
            return -1
        elif (getCost(choice1) > 5):
            return -1
        elif (getCost(choice1) < 6):
            gainCard(choice1, g, 0, currentPlayer)
        discardCard(handPos, currentPlayer, g, 1)
        return 0
    elif card == gardens:
        return -1
    elif card == great_hall:
        drawCard(currentPlayer, state);
        g.numActions+=1
        discardCard(handPos, currentPlayer, g, 0)
        return 0
    elif card == mine:
        if (g.hand[currentPlayer][choice1] not in g.hand[currentPlayer]):
            return -1
        elif (g.hand[currentPlayer][choice1] < copper or g.hand[currentPlayer][choice1] > gold):
            return -1
        if (g.hand[currentPlayer][choice1] == copper and choice2 == silver):
            discardCard(copper,currentPlayer,g,1)
            gainCard(silver,g,2,currentPlayer)
            return 0
        elif (g.hand[currentPlayer][choice1] == copper and choice2 == gold):
            discardCard(copper,currentPlayer,g,1)
            gainCard(gold,g,2,currentPlayer)
            return 0
        elif (g.hand[currentPlayer][choice1] == copper and choice2 == copper):
            discardCard(copper,currentPlayer,g,1)
            gainCard(copper,g,2,currentPlayer)
            return 0
        elif (choice2 > gold or choice2 < copper):
            return -1
        elif( (getCost(g.hand[currentPlayer][choice1]) + 3) > getCost(choice2) ):
            return -1
        else:
            return -1
        discardCard(handPos, currentPlayer, g, 0)
        return 0
    elif card == minion:
        g.numActions+=1
        discardCard(handPos, currentPlayer,g, 0)
        if (choice1):
            updateCoins(currentPlayer,g,2)
        elif (choice2):
            while(g.handcount[currentPlayer] > 0):
                discardCard(handPos, currentPlayer, g, 0)
            for i in range(4):
                drawCard(currentPlayer, g)
            for i in range(g.numPlayers):
                if (i != currentPlayer):
                    if ( g.handCount[i] > 4 ):
                        while( g.handCount[i] > 0 ):
                            discardCard(handPos, i, g, 0)
                        for j in range(4):
                            drawCard(i, g)
        discardCard(handPos, currentPlayer, g, 0)
        return 0
    elif card == outpost:
        g.outpostPlayed+=1
        discardCard(handPos, currentPlayer, g, 0)
        return 0
    elif card == remodel:
        j = g.hand[currentPlayer][choice1]
        if ( (getCost(g.hand[currentPlayer][choice1]) + 2) < getCost(choice2) ):
            return -1
        else:
            gainCard(choice2, g, 0, currentPlayer)
            discardCard(handPos, currentPlayer, g, 1)
        discardCard(handPos, currentPlayer, g, 0)
        return 0
    elif card == salvager:
        g.numBuys+=1
        if (choice1):
            g.coins = g.coins + getCost( g.hand[currentPlayer][handPos] )
            discardCard(choice1, currentPlayer, g, 1)      
        discardCard(handPos, currentPlayer, g, 0)
        return 0
    elif card == sea_hag:
        for i in range(g.numPlayers):
            if (i != currentPlayer):
                drawCard(i,g)
                discardCard(g.hand[i][handCount[i]-1],i,g,2)
                gainCard(curse,g,1,i)
        discardCard(handPos, currentPlayer, g, 0)
        return 0 
    elif card == smithy:
        for i in range(3):
            drawCard(currentPlayer,g)
        discardCard(handPos,currentPlayer,g, 0)
        return 0
    elif card == steward:
        if (choice1 == 1):                     
            drawCard(currentPlayer, g)
            drawCard(currentPlayer, g)
        elif (choice1 == 2):
            g.coins = g.coins + 2
        else:
            discardCard(choice2, currentPlayer, g, 1)
            discardCard(choice3, currentPlayer, g, 1)
        discardCard(handPos, currentPlayer, g, 0)
        return 0
    elif card == treasure_map:
        index = -1
        for i in range(handCount[currentPlayer]):
            if (g.hand[currentPlayer][i] == treasure_map and i != handPos):
                index = i
                break
        if (index > -1):
            discardCard(handPos, currentPlayer, g, 1)
            discardCard(index, currentPlayer, g, 1)
            for i in range(4):
                gainCard(gold, g, 1, currentPlayer)
        discardCard(handPos, currentPlayer, g, 0)
        return 0
    elif card == village:
        drawCard(currentPlayer, g)
        g.numActions = g.numActions + 2
        discardCard(handPos, currentPlayer, g, 0)
        return 0

def isGameOver(g):
    j=0
    if (g.supplyCount[province] == 0):
        return 1
    for i in range(MAX_CARDS):
        if (g.supplyCount[i] == 0):
            j+=1
    if ( j >= 3):
        return 1
    return 0
def scoreFor (player, g):
    score = 0
    for i in range( g.handCount[player]):
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
            score = score + ( fullDeckCount(player, 0, state) / 10 )
    for i in range( g.discardCount[player]):
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
            score = score + ( fullDeckCount(player, 0, state) / 10 )
    for i in range( g.deckCount[player]):
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
            score = score + ( fullDeckCount(player, 0, state) / 10 )  
        return score
def getWinners(g):
    players =[0] * MAX_PLAYERS
    for i in range(MAX_PLAYERS):
        if (i >= g.numPlayers):
            players[i] = -9999
        else:
            players[i] = scoreFor (i, g)
    j = 0
    for i in range(MAX_PLAYERS):
        if (players[i] > players[j]):
            j = i
    highScore = players[j]
    currentPlayer = whoseTurn(g)
    for i in range(MAX_PLAYERS):
        if ( players[i] == highScore and i > currentPlayer ):
            players[i]+=1
    j = 0
    for i in range(MAX_PLAYERS):
        if ( players[i] > players[j] ):
            j = i
    highScore = players[j]
    for i in range(MAX_PLAYERS):
        if ( players[i] == highScore ):
            players[i] = 1
        else:
            players[i] = 0
    return players