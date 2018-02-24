# Mark Trinquero
# Human Player (based on user input)

from time import time, sleep
from random import randint
import isolation

class HumanPlayer():
    def move(self, game, legal_moves, time_left):
        print('\t'.join(['[%d] %s'%(i,str(move)) for i,move in enumerate(legal_moves)] ))
        valid_choice = False
        while not valid_choice:
            try:
                index = int(raw_input('Select move index:'))
                valid_choice = 0 <= index < len(legal_moves)
                if not valid_choice:
                    print('Illegal move! Try again.')
            except ValueError:
                print('Invalid index! Try again.')
        return legal_moves[index]


## Game Setup
if __name__ == '__main__':
    from isolation import Board