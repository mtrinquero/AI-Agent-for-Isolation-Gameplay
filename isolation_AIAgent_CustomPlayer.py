# Mark Trinquero
# Custom AI Agent for isolation gameplay
# Utilizes depth-limited minimax algorithm with alpha-beta pruning

from time import time, sleep
from random import randint
import isolation


class OpenMoveEvalFn():
    # number of availiable moves for current player
    def score(self, game):
        return len(game.get_legal_moves())

# Custom Eval Function: uses opponents and your moves
# class CustomEvalFn():
#     def score(self, game):
#         my_moves = len(game.get_legal_moves())
#         thier_moves = len(game.get_opponent_moves())
#         custome_moves = my_moves - thier_moves
#         return custome_moves


# CUSTOM AI AGENT: depth-limited minimax algorithm with alpha-beta pruning
class CustomPlayer():
    def __init__(self, search_depth=3, eval_fn=OpenMoveEvalFn()):
        self.eval_fn = eval_fn
        self.search_depth = search_depth
        self.helper = False
        self.states = {}
        self.time_left = None

    def move(self, game, legal_moves, time_left):
        #curr_time_millis = lambda : int(round(time() * 1000))
        #move_start = curr_time_millis()
        #curr_time_left = lambda : time_left - (curr_time_millis() - move_start)
        self.time_left = time_left
        # Assist AI Agent with optimal moves during early gameplay (move 0, move 1)
        if game.move_count == 0:
            print 'player one power move made'
            return game.height / 2, game.width / 2 # SELECT CENTER SQUARE IF OPEN
        # if agent is player 2
        if game.move_count == 1:
            print 'player two power move made'
            if (2,2) in legal_moves:
                best_move = (2,2) # SELECT CENTER SQUARE IF OPEN
                return best_move
            else:   # If center square has already been played, select next best power move
                if (0,3) in legal_moves:
                    best_move = (0,3)
                    return best_move # power spot 1 of 8
                elif (1,4) in legal_moves:
                    best_move = (1,4)
                    return best_move # power spot 2 of 8
                elif (3,4) in legal_moves:
                    best_move = (3,4)
                    return best_move # power spot 3 of 8
                elif (4,3) in legal_moves:
                    best_move = (4,3)
                    return best_move # power spot 4 of 8
                elif (4,1) in legal_moves:
                    best_move = (4,1)
                    return best_move # power spot 5 of 8
                elif (3,0) in legal_moves:
                    best_move = (3,0)
                    return best_move # power spot 6 of 8
                elif (1,0) in legal_moves:
                    best_move = (1,0)
                    return best_move # power spot 7 of 8
                elif (0,1) in legal_moves:
                    best_move = (0,1)
                    return best_move # power spot 8 of 8
                else:
                    print "ERROR IN POWER MOVES"

        if game.move_count == 2:
            self.helper = self.move_helper(game)
        if self.helper:
            return self.get_move(game)
        # select optimal move for remaining gameplay
        # best_move, utility, time_expired = self.minimax(game, depth=self.search_depth, maximizing_player=True)
        best_move, utility = self.alphabeta_deepening(game)
        return best_move


    # get utility value at provided game state
    def utility(self, game):
        if game.is_winner(self):
            return float("inf")
        if game.is_opponent_winner(self):
            return float("-inf")
        return self.eval_fn.score(game)

    # check to see if current state is a terminal game state
    def is_terminal_state(self, game):
        if game.is_winner(self) or game.is_opponent_winner(self):
            return True
        return False

    def get_opponent_last_move(self, game):
        legal_moves = game.get_legal_moves()
        if len(legal_moves) == 0:
            return False
        next_move = game.forecast_move(legal_moves[0])
        opponent = next_move.get_active_player()
        return game.get_last_move_for_player(opponent)

    def get_move(self, game):
        opponent_last_move = self.get_opponent_last_move(game)
        move = (game.height - opponent_last_move[0] - 1, game.width - opponent_last_move[1] - 1)
        # DEBUGGING 
        # print 'MOVING TO:'
        # print str(move)
        return move

    # check for reflection moves first
    def move_helper(self, game):
        reflection_moves = [(0,0), (0,2), (0,4), (1,1), (1,2), (1,3), (2,0), (2,1), (2,3), (2,4), (3,1), (3,2), (3,3),(4,0), (4,2), (4,4)]
        opponent_last_move = self.get_opponent_last_move(game)
        if opponent_last_move in reflection_moves:
            return True
        return False

    # MIMIMAX ALGO
    def minimax(self, game, depth=float("inf"), maximizing_player=True):
        if maximizing_player:
            best_val = -float("inf")
        else:  # minimizing player
            best_val = float("inf")
        best_move = (-1, -1)
        time_expired = self.time_left() < 15

        if time_expired:
            return best_move, best_val, True
        if self.is_terminal_state(game):
            return best_move, self.utility(game), False

        possible_moves = game.get_legal_moves()
        if len(possible_moves) > 0:
            best_move = possible_moves[0]

        for possible_move in possible_moves:
            if depth == 1:
                current_val = self.utility(game.forecast_move(possible_move)) 
            else:
                next_move, current_val, time_expired = self.minimax(game.forecast_move(possible_move), depth - 1, not maximizing_player)
            if time_expired:
                return best_move, best_val, time_expired
            if (maximizing_player and current_val > best_val) or (not maximizing_player and current_val < best_val):
                best_move = possible_move
                best_val = current_val
        return best_move, best_val, time_expired



    # MINIMAX ALGO WITH DEEPING
    def minimax_deepening(self, game, max_depth=float("inf"), maximizing_player=True):
        deeper = 1
        best_move = (-1, -1)
        if maximizing_player:
            best_val = -float("inf")
        else:
            best_val = float("inf")

        while deeper <= max_depth:
            move, val, time_expired = self.minimax(game, deeper, maximizing_player)
            if time_expired or deeper > game.height * game.width - game.move_count:
                print 'Time has expired' 
                print 'current depth'
                print str(deeper - 1)
                return best_move, best_val
            else:
                best_move = move
                best_val = val
                deeper += 1

        print 'Evaluated to max depth of ' + str(max_depth) + '.'
        return best_move, best_val


    # ALPHA BETA PRUNING FOR IMPROVEMENT OF AI AGENT GAMEPLAY
    def alphabeta(self, game, depth=float("inf"), alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        if maximizing_player:
            best_val = -float("inf")
        else:
            best_val = float("inf")
        best_move = (-1, -1)
        time_expired = self.time_left() < 15

        if time_expired:
            return best_move, best_val, True
        if self.is_terminal_state(game):
            return best_move, self.utility(game), False

        possible_moves = game.get_legal_moves()
        if len(possible_moves) > 0:
            best_move = possible_moves[0]

        for possible_move in possible_moves:
            if depth == 1:
                current_val = self.utility(game.forecast_move(possible_move))
            else:
                next_move, current_val, time_expired = self.alphabeta(game.forecast_move(possible_move), depth - 1, alpha, beta, not maximizing_player)

            if time_expired:
                return best_move, best_val, time_expired

            if (maximizing_player and current_val >= beta) or (not maximizing_player and current_val <= alpha):
                return possible_move, current_val, time_expired

            if maximizing_player:
                alpha = max(alpha, current_val)
            else:
                beta = min(beta, current_val)

            if (maximizing_player and current_val > best_val) or (not maximizing_player and current_val < best_val):
                best_move = possible_move
                best_val = current_val

        return best_move, best_val, time_expired




    # ALPHA BETA DEEPENING IMPROVEMENT
    def alphabeta_deepening(self, game, max_depth=float("inf"), alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        deeper = 1
        best_move = (-1, -1)
        if maximizing_player:
            best_val = -float("inf")
        else:
            best_val = float("inf")
        while deeper <= max_depth:
            move, val, time_expired = self.alphabeta(game, deeper, alpha, beta, maximizing_player)
            if time_expired or deeper > game.height * game.width - game.move_count:
                print 'Time has expired' 
                print 'current depth'
                print str(deeper - 1)
                return best_move, best_val
            else:
                best_move = move
                best_val = val
                deeper += 1
        return best_move, best_val




## Gameplay setup and testing (confirm agent preforms better than random player)
if __name__ == '__main__':
    from isolation import Board
    r = RandomPlayer()
    h = CustomPlayer()
    game = Board(h,r)
    game.play_isolation()



