"""
Tic Tac Toe Player
"""

import math

from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # in the initial game state, X gets the first move
    if board == initial_state():
        return X
    
    # if the board is terminal there's nothing to do here
    if terminal(board):
        return None
    
    # count Xs and Os to determine next turn
    if flatten(board).count(X) > flatten(board).count(O):
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # action_set is a set of tuples (i,j), where i = row and j = column
    action_set = set()
    
    # iterate through cells while getting coordinates
    i = 0
    for row in board:
        j = 0
        for cell in row:
            # if you find an empty cell record its coordinates and add to tuple
            if cell == EMPTY:
                action_set.add((i,j))
            j += 1
        i += 1
    
    return action_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # make a deepcopy of the board since you can't modify the og board
    new_board = deepcopy(board)

    # in new_board, set cell at action's coordinates to current player's symbol if cell is empty
    if board[action[0]][action[1]] == EMPTY:
        new_board[action[0]][action[1]] = player(board)
        return new_board
    # if action is not valid for board, raise an exception
    else:
        raise ValueError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    """
    what are the winning conditions?
    - three moves in a row horizontally, vertically or diagonally
    - how to identify programatically?
        - go through the cells
        - when you find one that is not EMPTY, (and is an eligible cell?), check the following
        - if it is the same as the previous, check the next one
        - what about when you have to substract? such as running into an X in board[0][2]
    """
    # in order to potentially save time, return None if there are less than three Xs
    if flatten(board).count(X) < 3:
        return None

    # horizontal winning conditions
    if board[0][0] == board[0][1] == board[0][2] != EMPTY:
        return board[0][0]
    elif board[1][0] == board[1][1] == board[1][2] != EMPTY:
        return board[1][0]
    elif board[2][0] == board[2][1] == board[2][2] != EMPTY:
        return board[2][0]

    # vertical winning conditions
    if board[0][0] == board[1][0] == board[2][0] != EMPTY:
        return board[0][0]
    elif board[0][1] == board[1][1] == board[2][1] != EMPTY:
        return board[0][1]
    elif board[0][2] == board[1][2] == board[2][2] != EMPTY:
        return board[0][2]

    # diagonal winning conditions
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # if there's a winner, it's terminal
    if winner(board) == X or winner(board) == O:
        return True
    # return True if there are no more moves to be made
    elif flatten(board).count(EMPTY) == 0:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    options = {}
    # use this toggle for testing ab pruning and non ab pruning minimaxes
    use_ab_pruning = True

    if not use_ab_pruning:
        # call appropriate function for player
        if player(board) == X:
            # get max value from all immediate actions
            for action in actions(board):
                options[action] = min_value(result(board, action))
            # return the action with the best outcome
            return max(options, key=options.get)
        elif player(board) == O:
            # get min value from all immediate actions
            for action in actions(board):
                options[action] = max_value(result(board, action))
            # return the action with the best outcome
            return min(options, key=options.get)
    else:
        # ALPHA BETA PRUNING TEST
        for action in actions(board):
            options[action] = minimaxab(result(board, action))
        if player(board) == X:
            return max(options, key=options.get)
        else:
            return min(options, key=options.get)


# utility function to flatten board
def flatten(board):
    return [i for x in board for i in x]


# taken from class slides
def max_value(board):
    if (terminal(board)):
        return utility(board)
    v = float("-inf")
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


# taken from class slides
def min_value(board):
    if (terminal(board)):
        return utility(board)
    v = float("inf")
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


# testing alpha beta pruning
# got this algorithm from https://www.whitman.edu/Documents/Academics/Mathematics/2019/Felstiner-Guichard.pdf
def minimaxab(board, alpha=float("-inf"), beta=float("inf")):
    if terminal(board):
        return utility(board)
    elif player(board) == X:
        best = float("-inf")
        for action in actions(board):
            val = minimaxab(result(board, action), alpha, beta)
            best = max(val, best)
            alpha = max(best, alpha)
            if alpha >= beta:
                break
        return best
    else:
        best = float("inf")
        for action in actions(board):
            # the source paper does not use alpha and beta here
            val = minimaxab(result(board, action), alpha, beta)
            best = min(val, best)
            beta = min(best, beta)
            if alpha >= beta:
                break
        return best