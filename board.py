import random
import sys
import re

from variable import *
from method import *
# from ai import *

def init_board():
    b = [[(3 if i==0 or i==9 or j==0 or j==9 else 0) for i in range(10)] for j in range(10)]
    b[4][4] = 1; b[4][5] = 2; b[5][4] = 2; b[5][5] = 1
    return b

def init_color():
    return BLACK

def init_moves():
    return []

def copy_board(board):
    if board is None:
        return init_board()
    else:
        return [[board[i][j] for i in range(10)] for j in range(10)]

def copy_color(color):
    if color is None:
        return init_color()
    else:
        return color

def copy_moves(moves):
    if moves is None:
        return init_moves()
    else:
        return moves

def opposite_color(color):
    return 3 - color

def count_color(board, color):
    cnt = 0
    for cell in CELLS:
        (j,i) = cell
        if board[i][j] == color:
            cnt += 1
    return cnt

def count(board):
    return count_color(board, BLACK) + count_color(board, WHITE)

def flip_line(board, color, stone, direction):
    ocolor = opposite_color(color)
    (j,i) = stone
    (jj,ii) = direction
    line = []
    if board[i][j] == NONE:
        n = 1
        while True:
            s = board[i+n*ii][j+n*jj]
            if s == color:
                break
            elif s == ocolor:
                line.append((i+n*ii, j+n*jj))
                n += 1
            else:
                line = []
                break
    return line

def flip_lines(board, color, stone):
    lines = []
    for direction in DIRECTIONS:
        line = flip_line(board, color, stone, direction)
        lines += line
    return lines

def is_valid_move(board, color, stone):
    lines = flip_lines(board, color, stone)
    return bool(len(lines))

def valid_moves(board, color):
    moves = []
    for cell in CELLS:
        if is_valid_move(board, color, cell):
            moves.append(cell)
    return moves

def is_valid_color(board, color):
    if color == BLACK or color == WHITE:
        moves = valid_moves(board, color)
        return bool(len(moves))
    else:
        return False

def valid_color(board, color):
    ocolor = opposite_color(color)
    if is_valid_color(board, color):
        return color
    elif is_valid_color(board, ocolor):
        return ocolor
    else:
        return NONE

def the_start(board):
    cnt = count(board)
    return cnt in [4,5]

def the_end(board, color):
    return valid_color(board, color) == NONE

def board2bit(board, color):
    intlist = sum(board, [])
    bitlist = list(map((lambda x: 1 if x==color else 0), intlist))
    strlist = list(map(str, bitlist))
    strbit = "".join(strlist)
    bit = int(strbit)
    return bit

def bit2board(bit):
    strbit = str(bit)
    strlist = list(strbit)
    bitlist = list(map(int, strlist))
    board = [bitlist[8*i:8*(i+1)] for i in range(len(bitlist)//2)]
    return board    

def print_color(color):
    if color == BLACK:
        print(BLACK_STONE, end='')
    elif color == WHITE:
        print(WHITE_STONE, end='')
    else:
        print(NONE_STONE, end='')


def print_moves(moves):
    for (i,m) in enumerate(moves):
        print(i+1, ": ", m, " ")


def print_board(board, color, mycolor):
    print("color: ", end='')
    print_color(color)
    print()
    print("mycolor: ", end='')
    print_color(mycolor)
    print()
    for i in range(10):
        for j in range(10):
            if (i,j) in [(0,0),(0,9),(9,0),(9,9)]:
                print('+', end='')
            elif i in [0,9]:
                print('-', end='')
            elif j in [0,9]:
                print('|', end='')
            else:
                print_color(board[i][j])
        print()


def choose_move(moves):
    l = len(moves)
    while True:
        i = input()
        j = re.sub(r'\d+', '', i)
        if len(j) == 0:
            k = int(i) - 1
            if k in range(l):
                return moves[k]


class Board:
    def __init__(self, board=None, color=None, mycolor=None, moves=None):
        self.board = copy_board(board)
        self.color = copy_color(color)
        self.mycolor = copy_color(mycolor)
        self.moves = copy_moves(moves)

    def move(self, stone):
        (j,i) = stone
        if is_valid_move(self.board, self.color, stone):
            lines = flip_lines(self.board, self.color, stone)
            self.board[i][j] = self.color
            for l in lines:
                (i,j) = l
                self.board[i][j] = self.color
        ocolor = opposite_color(self.color)
        self.color = valid_color(self.board, ocolor)
        self.moves.append((i,j))
        
    def random_choice(self):
        moves = valid_moves(self.board, self.color)
        return random.choice(moves)

    def person_choice(self):
        moves = valid_moves(self.board, self.color)
        print_moves(moves)
        move = choose_move(moves)
        return move


    def decide(self):
        # return self.random_choice()
        return self.person_choice()
