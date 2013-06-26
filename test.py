from game import Game
from intelplayer import IntelPlayer
from randomplayer import RandomPlayer

game = Game()

p1 = IntelPlayer()
p2 = RandomPlayer()

p1wins = 0
p2wins = 0

for i in range(500000):
    game.playGame(p1, p2)
