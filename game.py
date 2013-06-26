from random import shuffle

class Game:
    
    # Number used to indicate no block is forced
    ANY = 9

    # All straight lines in a 3x3 block
    LINES = ((0, 1, 2), (3, 4, 5),
             (6, 7, 8), (0, 4, 8),
             (2, 4, 6), (0, 3, 6),
             (1, 4, 7), (2, 5, 8))

    # List of players involved in a game
    players = []

    def playGame(self, player1, player2):
        """
        Given two players, play a game to completion.
        
        Player 1 will always go first.
        """
        self.players = [player1, player2]
        #shuffle(players)

        game = self.getBoard()
        next_player = 0

        while(not self.gameOver(game)):
            choice = self.players[next_player].playTurn(game)
            #print game["forced"]
            game["array"][choice] = next_player + 1
            game["forced"] = self.ANY
            for i in range(9):
                if game["array"][(choice % 9) * 9 + i] == 0:
                    game["forced"] = choice % 9
            next_player = 1 - next_player
            #self.printBoard(game)
            #raw_input("")

    def getBoard(self):
        """
        Return a Game Board dict representing a new game.
        
            game["forced"] indicates which block is necessary, or 9 if any.
            game["array"] is 81 elements, with each section of 9 indicating a singe TicTacToe board
            game["outer"] indicates progress on each outer set
        """
        return {"forced": self.ANY, 
                "array": [0 for x in range(81)],
                "outer": [0 for x in range(9)]}

    def gameOver(self, game):
        """
        Given a game board, check if the game is over.
        
        This method also takes responsibility for notifying players of wins and losses.
        """
        # Iterate over all of the inner games, to detect a win

        for i in range(9):
            if game["outer"][i] == 0:
                for line in self.LINES:
                    match = 3
                    for elem in line:
                        match &= game["array"][(9*i)+elem]
                    if not game["outer"][i]:
                        game["outer"][i] = match
                        #if match:
                            #print "Player "+str(match)+" took "+str(i)
                            #print line

        # Iterate over the outer game to detect game over

        for i in range(9):
            for line in self.LINES:
                match = 3
                for elem in line:
                    match &= game["outer"][elem]
                if match != 0:
                    #print "Game Over!"
                    #print str(match) + " wins!"
                    self.players[match-1].notifyWin()
                    self.players[2-match].notifyLose()
                    #print line
                    return True
        
        # Make sure we aren't out of squares

        hasBlank = False
        for i in range(81):
            if game["array"][i] == 0:
                hasBlank = True
        if not hasBlank:
            print "Tie"
            return True

        return False

    def printBoard(self, game):
        """Print out a given board in a human-readable fashion"""
        for row in range(3):
            for i in range(3):
                for x in (0, 1, 2, 9, 10, 11, 18, 19, 20):
                    print game["array"][(27*row)+(3*i)+x],
                print

        print game["outer"]
