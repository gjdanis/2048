import random
import itertools

def merge_right(b):
    """
    Merge the board right

    Args:
        b (list) two dimensional board to merge

    Returns: list

    >>> merge_right(test)
    [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    """

    def reverse(x):
        return list(reversed(x))
    
    t = map(reverse, b)
    return [reverse(x) for x in merge_left(t)]

def merge_up(b):
    """
    Merge the board upward. Note that zip(*t) is the
    transpose of b

    Args:
        b (list) two dimensional board to merge

    Returns: list

    >>> merge_up(test)
    [[2, 4, 8, 4], [0, 2, 2, 8], [0, 0, 0, 4], [0, 0, 0, 2]]
    """

    t = merge_left(zip(*b))
    return [list(x) for x in zip(*t)]

def merge_down(b):
    """
    Merge the board downward. Note that zip(*t) is the
    transpose of b

    Args:
        b (list) two dimensional board to merge

    Returns: list

    >>> merge_down(test)
    [[0, 0, 0, 4], [0, 0, 0, 8], [0, 2, 8, 4], [2, 4, 2, 2]]
    """
    
    t = merge_right(zip(*b))
    return [list(x) for x in zip(*t)]

def merge_left(b):
    """
    Merge the board left

    Args:
        b (list) two dimensional board to merge

    Returns: list
    """
    
    def merge(row, acc):
        """
        Recursive helper for merge_left. If we're finished with the list,
        nothing to do; return the accumulator. Otherwise, if we have
        more than one element, combine results of first from the left with right if
        they match. If there's only one element, no merge exists and we can just
        add it to the accumulator.

        Args:
            row (list) row in b we're trying to merge
            acc (list) current working merged row

        Returns: list
        """
        
        if not row:
            return acc

        x = row[0]
        if len(row) == 1:
            return acc + [x]

        return merge(row[2:], acc + [2*x]) if x == row[1] else merge(row[1:], acc + [x])

    board = []
    for row in b:
        merged = merge([x for x in row if x != 0], [])
        merged = merged + [0]*(len(row)-len(merged))
        board.append(merged)
    return board

def move_exists(b):
    """
    Check whether or not a move exists on the board

    Args:
        b (list) two dimensional board to merge

    Returns: list

    >>> b = [[1, 2, 3, 4], [5, 6, 7, 8]]
    >>> move_exists(b)
    False
    >>> move_exists(test)
    True
    """
    for row in b:
        for x, y in zip(row[:-1], row[1:]): 
            if x == y or x == 0 or y == 0: 
                return True
    return False

MERGE_FUNCTIONS = {
    'left': merge_left,
    'right': merge_right,
    'up': merge_up,
    'down': merge_down
}
    
class Game:
    """
    Models a game of 2048 see http://2048game.com/.

    The merge functions are exposed publically
    so that ai.py can make use of them when evaluating the potential
    utility of a move. They are immutable.

    Moving from a game instance advances the state of the game forard
    and cannot be undone.
    """

    def __init__(self):
        self.board = [[0]*4 for _ in range(4)]
        self.spawn(2)

    def require_playing(f):
        """
        Decorator to ensure that the game is not over

        Args:
            f (callable) function to wrap with require_playing

        Returns: callable
        """
        def inner(self, *args, **kwargs):
            if move_exists(self.board) or move_exists(zip(*self.board)):
                return f(self, *args, **kwargs)
            return False
        return inner

    @require_playing
    def play_move(self, direction):
        """
        Advances the game in the given direction

        Args:
            direction (string) move to play
        
        Returns: bool
        """
        
        self.board = MERGE_FUNCTIONS[direction](self.board)
        return self.spawn()

    @require_playing
    def spawn(self, k=1):
        """
        Add k random tiles to the board at open positions. Chance
        of spawining a 2 is 90%; chance of 4 is 10%

        Args:
            k (int) number of tiles to add (defaults to 1 tile)

        Returns: bool
        """

        rows, cols = list(range(4)), list(range(4))
        random.shuffle(rows)
        random.shuffle(cols)
        
        distribution = [2]*9 + [4]
        count = 0
        for i, j in itertools.product(rows, rows):
            if count == k: return True
            if self.board[i][j] != 0: continue
            
            self.board[i][j] = random.sample(distribution, 1)[0]
            count += 1
        return False

    def __str__(self):
        return str(self.board)

if __name__ == "__main__":
    import doctest
    doctest.testmod(extraglobs={'test': [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]})
