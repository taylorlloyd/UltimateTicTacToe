

class Player:

    def playTurn(self, game):
        """
        Function to be overridden for players
        
        Takes a gameboard dict as argument, and returns an int indicating which place to take
        Players are responsible for verifying they are making legitimate moves.
        """

        print "Error: Generic Player playTurn"
        return 0

    def notifyWin(self):
        """
        Accepts notification of a game win.
        """
        return

    def notifyLose(self):
        """
        Accepts notification of a game loss.
        """
        return
