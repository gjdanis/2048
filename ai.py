from game import *

import math

def aimove(b):
    """
    Evaluate the utility of each of the four possible moves
    we can make on b

    Args: b (list) root board to score

    Returns: list
    """

    def fitness(b):
        """
        Returns the heuristic value of b

        Snake refers to the "snake line pattern" (http://tinyurl.com/l9bstk6)
        Here we only evaluate one direction; we award more points if high valued tiles
        occur along this path. We penalize the board for not having
        the highest valued tile in the lower left corner

        Args: b (list) board to score

        Returns: float
        """

        if not move_exists(b):
            return -float("inf")
        
        snake = []
        for i, col in enumerate(zip(*b)):
            snake.extend(reversed(col) if i % 2 == 0 else col)

        m = max(snake)
        return sum(x/10**n for n, x in enumerate(snake)) - \
               math.pow((b[3][0] != m)*abs(b[3][0] - m), 2)

    def search(b, d, move=False):
        """
        Performs expectimax search on a given configuration to
        specified depth (d).

        Algorithm details:
           - if the AI needs to move, make each child move,
             recurse, return the maximum fitness value
           - if it is not the AI's turn, form all
             possible child spawns, and return their weighted average 
             as that node's evaluation

        Args:
            b (list) board to search
            d (int) depth to serach to
            move (bool) whether or not it's our (AI player's) move to make

        Returns: float
        """

        if d == 0 or (move and not move_exists(b)):
            return fitness(b)

        alpha = fitness(b)
        if move:
            for _, action in MERGE_FUNCTIONS.items():
                child = action(b)
                alpha = max(alpha, search(child, d-1))
        else:
            alpha = 0
            zeros = [(i,j) for i, j in itertools.product(range(4), range(4)) if b[i][j] == 0]
            for i, j in zeros:
                c1 = [[x for x in row] for row in b]
                c2 = [[x for x in row] for row in b]
                c1[i][j] = 2
                c2[i][j] = 4
                alpha += (.9*search(c1, d-1, True)/len(zeros) +
                          .1*search(c2, d-1, True)/len(zeros))
        return alpha

    results = []
    for direction, action in MERGE_FUNCTIONS.items():
        result = direction, search(action(b), 4)
        results.append(result)
    return results
         
def aiplay(game):
    """
    Runs a game instance playing the move that determined
    by aimove.

    Args: game (Game) to play

    Returns: void
    """
    b = game.board

    while True:
        print(str(game) + '\n')
        direction = max(aimove(game.board), key = lambda x: x[1])[0]

        if not game.play_move(direction):
            m = max(x for row in b for x in row)
            print('game over...best was {0}'.format(m))
            print(game)
            break 

