from random import randint
from player import Player

class RandomPlayer(Player):
    """Implements a totally random, rule abiding player"""
    
    def playTurn(self, game):
        if game["forced"] < 9:
            random = randint(0 + (9*game["forced"]), 8 + (9*game["forced"]))
            while game["array"][random] != 0:
                random = randint(0 + (9*game["forced"]), 8 + (9*game["forced"]))
            return random

        random = randint(0, 80)
        while game["array"][random] != 0:
            random = randint(0, 80)
        return random
