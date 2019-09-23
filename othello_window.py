import time
import curses

from othello_variable import *
from othello_board import *

WINDOW = None
STRING = None

# 
#    Player1  x -- o  Player2
#          *  2 -- 2
#           +--------+
#           |        |
#           |        |
#           |        |
#           |   ox   |
#           |   xo   |
#           |        |
#           |        |
#           |        |
#           +--------+
# 

def make(p1, p2, p1_color, p2_color, board, color):
    black = str(count_color(board, BLACK))
    white = str(count_color(board, WHITE))
    string = "\n"
    
    if p1_color == BLACK and p2_color == WHITE:
        string += p1.rjust(NAMESPACE) + "  x -- o  " + p2.ljust(NAMESPACE) + "\n"
    elif p1_color == WHITE and p2_color == BLACK:
        string += p1.rjust(NAMESPACE) + "  o -- x  " + p2.ljust(NAMESPACE) + "\n"

    if color == BLACK:
        black = "*".rjust(NAMESPACE) + black.rjust(COLORSPACE)
    elif color == WHITE:
        white = white.ljust(COLORSPACE) + "*".ljust(NAMESPACE)

    if p1_color == BLACK and p2_color == WHITE:
        string += black + " -- " + white + "\n"
    elif p1_color == WHITE and p2_color == BLACK:
        string += white + " -- " + "\n"

    for i in range(10):
        line = ""
        for j in range(10):
            if (i,j) in [(0,0),(0,9),(9,0),(9,9)]:
                line += "+"
            elif i in [0,9]:
                line += "-"
            elif j in [0,9]:
                line += "|"
            else:
                if board[i][j] == BLACK:
                    line += "x"
                elif board[i][j] == WHITE:
                    line += "o"
                else:
                    line += " "
        string += line.center(WIDTH) + "\n"
    
    return string


def initialize_window():
    global WINDOW
    global STRING
    WINDOW = curses.initscr()
    curses.noecho()
    curses.cbreak()
    STRING = ""


def write_on_string():
    global STRING
    board = init_board()
    color = init_color()
    STRING = make("Player1", "Player2", BLACK, WHITE, board, color)


def write_on_window():
    global WINDOW
    global STRING
    if WINDOW is None:
        print("none!")
        return
    WINDOW.addstr(STRING)
    WINDOW.refresh()


def clear_window():
    global WINDOW
    WINDOW.clear()
    WINDOW.refresh()


def terminate_window():
    global WINDOW
    global STRING
    curses.nocbreak()
    curses.echo()
    curses.endwin()
    STRING = ""


# def othello_window(window):
#     window.addstr("hoge")
#     window.refresh()
#     time.sleep(1)
#     window.erase()
#     window.refresh()
#     time.sleep(1)

# def main():
#     global WINDOW
#     global STRING
#     # curses.wrapper(othello_window)
#     initialize_window()
#     write_on_string()
#     write_on_window()
#     time.sleep(3)
#     clear_window()
#     time.sleep(1)
#     terminate_window()

# if __name__ == "__main__":
#     main()
