from board import Board
from board import valid_moves, the_end

def random_playout():
    b = Board()
    n = 0
    print(valid_moves(b.board, b.color))
    # print_board(b.board, b.color, b.mycolor)
    while True:
        n += 1
        if n > 100:
            # print_board(b.board, b.color, b.mycolor)
            break
        if the_end(b.board, b.color):
            # print_board(b.board, b.color, b.mycolor)
            break
        else:
            m = b.random_choice()
            print(m)
            b.move(m)
            # print_board(b.board, b.color, b.mycolor)
            print(valid_moves(b.board, b.color))
            print()