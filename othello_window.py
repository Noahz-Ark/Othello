import time
import curses

from othello_board import BLACK, WHITE
from othello_board import count

WINDOW = None
# STRING = None

NAMESPACE = 10
COLORSPACE = 3
BARSPACE = 4
WIDTH = (NAMESPACE + COLORSPACE) * 2 + BARSPACE

class Error(Exception):
    pass

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

def make(p1_name, p2_name, p1_color, p2_color, board, color):
    black = str(count(board, BLACK))
    white = str(count(board, WHITE))
    string = "\n"
    
    if p1_color == BLACK and p2_color == WHITE:
        string += p1_name.rjust(NAMESPACE) + "  x -- o  " + p2_name.ljust(NAMESPACE) + "\n"
    elif p1_color == WHITE and p2_color == BLACK:
        string += p1_name.rjust(NAMESPACE) + "  o -- x  " + p2_name.ljust(NAMESPACE) + "\n"

    if color == p1_color:
        if color == BLACK:
            p1 = "*".rjust(NAMESPACE) + black.rjust(COLORSPACE)
            p2 = white.ljust(COLORSPACE) + "".ljust(NAMESPACE)
        elif color == WHITE:
            p1 = "*".rjust(NAMESPACE) + white.rjust(COLORSPACE)
            p2 = black.ljust(COLORSPACE) + "".ljust(NAMESPACE)
        string += p1 + " -- " + p2 + "\n"
    elif color == p2_color:
        if color == BLACK:
            p1 = "".rjust(NAMESPACE) + white.rjust(COLORSPACE)
            p2 = black.ljust(COLORSPACE) + "*".ljust(NAMESPACE)
        elif color == WHITE:
            p1 = "".rjust(NAMESPACE) + black.rjust(COLORSPACE)
            p2 = white.ljust(COLORSPACE) + "*".ljust(NAMESPACE)
        string += p1 + " -- " + p2 + "\n"
    else:
        if p1_color == BLACK and p2_color == WHITE:
            string += black.rjust(NAMESPACE+COLORSPACE) + " -- " + white.ljust(NAMESPACE+COLORSPACE) + "\n"
        elif p1_color == WHITE and p2_color == BLACK:
            string += white.rjust(NAMESPACE+COLORSPACE) + " -- " + black.ljust(NAMESPACE+COLORSPACE) + "\n"

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


def display_board(p1_name, p2_name, p1_color, p2_color, color, board):
    black = str(count(board, BLACK))
    white = str(count(board, WHITE))
    string = "\n"
    
    if p1_color == BLACK and p2_color == WHITE:
        string += p1_name.rjust(NAMESPACE) + "  x -- o  " + p2_name.ljust(NAMESPACE) + "\n"
    elif p1_color == WHITE and p2_color == BLACK:
        string += p1_name.rjust(NAMESPACE) + "  o -- x  " + p2_name.ljust(NAMESPACE) + "\n"

    if color == p1_color:
        if color == BLACK:
            p1 = "*".rjust(NAMESPACE) + black.rjust(COLORSPACE)
            p2 = white.ljust(COLORSPACE) + "".ljust(NAMESPACE)
        elif color == WHITE:
            p1 = "*".rjust(NAMESPACE) + white.rjust(COLORSPACE)
            p2 = black.ljust(COLORSPACE) + "".ljust(NAMESPACE)
        string += p1 + " -- " + p2 + "\n"
    elif color == p2_color:
        if color == BLACK:
            p1 = "".rjust(NAMESPACE) + white.rjust(COLORSPACE)
            p2 = black.ljust(COLORSPACE) + "*".ljust(NAMESPACE)
        elif color == WHITE:
            p1 = "".rjust(NAMESPACE) + black.rjust(COLORSPACE)
            p2 = white.ljust(COLORSPACE) + "*".ljust(NAMESPACE)
        string += p1 + " -- " + p2 + "\n"
    else:
        if p1_color == BLACK and p2_color == WHITE:
            string += black.rjust(NAMESPACE+COLORSPACE) + " -- " + white.ljust(NAMESPACE+COLORSPACE) + "\n"
        elif p1_color == WHITE and p2_color == BLACK:
            string += white.rjust(NAMESPACE+COLORSPACE) + " -- " + black.ljust(NAMESPACE+COLORSPACE) + "\n"

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

    string += "\n"

    try:
        WINDOW.clear()
        WINDOW.addstr(string)
        WINDOW.refresh()
    except:
        terminate_window()
        raise Error

#
#  player1(WIN) 50 -- 14 (LOSE)player2
#
def display_gameresult(p1_name, p2_name, p1_count, p2_count):
    string = "\n"
    cnt1 = str(p1_count)
    cnt2 = str(p2_count)
    if p1_count > p2_count:
        string += p1_name + "(WIN) " + cnt1 + " -- " + cnt2 + " (LOSE)" + p2_name + "\n"
    elif p1_count < p2_count:
        string += p1_name + "(LOSE) " + cnt1 + " -- " + cnt2 + " (WIN)" + p2_name + "\n"
    else:
        string += p1_name + "(TIE) " + cnt1 + " -- " + cnt2 + " (TIE)" + p2_name + "\n"
    string += "\n"

    try:
        WINDOW.clear()
        WINDOW.addstr(string)
        WINDOW.refresh()
    except:
        terminate_window()
        raise Error

# TODO: 表示に必要な関数を作成する(必要事項を引数として文字列を返す)
# 結果を格納する方法を考える
#
#          player1    --    player2
#   1st:      WIN  34 -- 30 LOSE
#   2nd:     LOSE  30 -- 34 WIN
#  ......
# 100th:      TIE  32 -- 32 TIE
# ---------------------------------
# total:      WIN  60 -- 20 LOSE
#
def display_matchresult(p1_name, p2_name):
    pass





    


def write_on_string(board, color):
    global STRING
    # board = init_board()
    # color = init_color()
    STRING = make("Player1", "Player2", BLACK, WHITE, board, color)


def write_on_window():
    global WINDOW
    global STRING
    if WINDOW is None:
        print("none!")
        return
    try:
        WINDOW.addstr(STRING)
        WINDOW.refresh()
    except:
        terminate_window()
        raise Error


def clear_window():
    global WINDOW
    try:
        WINDOW.clear()
        WINDOW.refresh()
    except:
        terminate_window()
        raise Error


def terminate_window():
    # global WINDOW
    # global STRING
    curses.nocbreak()
    curses.echo()
    curses.endwin()
    # STRING = ""


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
