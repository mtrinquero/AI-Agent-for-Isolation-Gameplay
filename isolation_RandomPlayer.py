# Mark Trinquero
# Random Player (for initial testing)

from time import time, sleep
from random import randint
import isolation

class RandomPlayer():
    # player that chooses a move randomly (testing / inital setup)
    def move(self, game, legal_moves, time_left):
        if not legal_moves: return (-1,-1)
        return legal_moves[randint(0,len(legal_moves)-1)]


## Gameplay setup
if __name__ == '__main__':
    from isolation import Board
