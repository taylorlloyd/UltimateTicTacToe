from random import shuffle

class Game:
    
    ANY = 9
    LINES = ((0, 1, 2), (3, 4, 5),
             (6, 7, 8), (0, 4, 8),
             (2, 4, 6))

    def playGame(self, player1, player2):
        """Given two players, play a game to completion."""
        players = [player1, player2]
        shuffle(players)

        game = getBoard()
        next_player = 0

        while(not gameOver(game)):
            game["array"][players[next_player].playTurn(game)] = next_player + 1
            next_player = 1 - next_player

    def getBoard(self):
        """Return a Game Board dict representing a new game."""
        return {"forced": self.ANY, 
                "array": [0 for x in range(81)],
                "outer": [0 for x in range(9)]}

    def gameOver(self, game):
        """Given a game board, check if the game is over."""
        # Iterate over all of the inner games, to detect a win

        for i in range(9):
            if game["outer"][i] == 0:
                for line in LINES:
                    match = 3
                    for elem in line:
                        match &= game["array"][i+elem]
                    game["outer"][i] = match

        # Iterate over the outer game to detect game over

        for i in range(9):
            for line in LINES:
                match = 3
                for elem in line:
                    match &= game["outer"][elem]
                if match != 0:
                    print "Game Over!"
                    print str(players[match - 1]) + " wins!"

    def printBoard(self, game):
        """Print out a given board in a human-readable fashion"""
        for i in range(81):
            print game["array"][i],
            if (i + 1) % 3 == 0:
                print " ",
            if (i + 1) % 9 == 0:
                print
            if (i + 1) % 27 == 0:
                print
