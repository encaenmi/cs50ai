from tictactoe import initial_state, player, actions, result, winner, terminal, utility, minimax, flatten, max_value, min_value

X = "X"
O = "O"
EMPTY = None

# TODO
# player(board) DONE
# actions(board) DONE
# result(board) DONE
# winner(board) DONE
# terminal(board) DONE
# utility(board) DONE
# minimax(board) IN REVIEW
# flatten(board) DONE
# max_value(board) DONE
# min_value(board) DONE

# in fail_board, all options except (2,0) should evaluate to 1
fail_board = [[X, EMPTY, EMPTY],
        [X, O, EMPTY],
        [EMPTY , EMPTY, EMPTY]]

test_board = [[X, EMPTY, EMPTY],
        [X, O, EMPTY],
        [EMPTY , EMPTY, EMPTY]]


#print(f"max: {max_value(test_board)}, min: {min_value(test_board)}")

print(minimax(test_board))