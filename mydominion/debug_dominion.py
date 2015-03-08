################### DEBUGGING FUNCTIONS FOR DOMINION ##################
#######################################################################

class Debug():
    """
    Set of debugging functions to print game state properties
    in human readable form.
    """
    def hand(self, g, player=None):
        """
        Prints hand of @player, by default prints hand of current player.
        Proper card names are printed, like Copper, Estate, or whatever. Not just integers.
        :param g:
        """
        if not player:
            player = g.whoseTurn
        for card_no in g.hand[player]:
            print CARD_NAMES[card_no]

    def deck(self, g, player=None):
        """
        Prints deck of @player, by default prints deck of current player.
        Proper card names are printed.
        :param g:
        """
        if not player:
            player = g.whoseTurn
        for card_no in g.deck[player]:
            print CARD_NAMES[card_no]

    def supply(self):
        print "No. Card Name   \t SupplyCount \t Cost"
        print "--  ------------ \t ----------- \t ----"
        for i in range(NCARDS):
            print "%s %s \t %s \t %d"%(str(i).ljust(2), CARD_NAMES[i].ljust(12), str(g.supplyCount[i]).ljust(11), CARD_COST[i])


D = Debug()
