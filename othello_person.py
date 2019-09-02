import numpy as np
import random
import time
import sys
import socket
import threading

# macro
from variable import NONE, WHITE, BLACK, SENTINEL, NONE_STONE, WHITE_STONE, BLACK_STONE, DIRECTIONS, CELLS
from method import int2tuple, tuple2int, decode_result, encode_result

# global method
from board import is_valid_move, valid_moves, count_color, the_end, print_board

# class
from board import Board

# global variable
B = None
C = None
M = None

HOST = "localhost"
PORT = int(sys.argv[1])
CLIENT = None

REFEREE = None
PLAYER1 = None
PLAYER2 = None
REF = True
PLY1 = False
PLY2 = False

#TODO: ENVを環境として必要なglobal変数を格納する
START = True
END = False
ENV = []


def client():
    global START, END
    global REF, PLY1, PLY2
    global B, C, M

    global CLIENT
    CLIENT.connect((HOST, PORT))

    while True:
        message = ""
        message = int(CLIENT.recv(1024).decode("UTF-8"))

        if message < 0:
            break
        # 1手目
        elif message == 0:
            mystone = B.random_choice()
            B.move(mystone)
            message = str(tuple2int(mystone))
            CLIENT.send(message.encode("UTF-8"))
        # 2手目以降
        elif message < 100:
            opstone = int2tuple(message)
            B.move(opstone)
            print_board(B.board, B.color, B.mycolor)

            if the_end(B.board, B.color):
                pass
            else:
                mystone = B.random_choice()
                B.move(mystone)
                message = str(tuple2int(mystone))
                CLIENT.send(message.encode("UTF-8"))
        # 勝利
        elif message < 10000:
            (_, b, w) = decode_result(message)
            print("Win!\n")
            print("black", b, " vs ", w, "white\n")
            print_board(B.board, B.color, B.mycolor)
            CLIENT.close()
            break
        # 敗北
        elif message < 20000:
            (_, b, w) = decode_result(message)
            print("Lose!\n")
            print("black", b, " vs ", w, "white\n")
            print_board(B.board, B.color, B.mycolor)
            CLIENT.close()
            break
        # 引き分け
        elif message < 30000:
            (_, b, w) = decode_result(message)
            print("Draw!\n")
            print(b, " vs ", w, "\n")
            print_board(B.board, B.color, B.mycolor)
            CLIENT.close()
            break
        else:
            print("???\n")
            break
    CLIENT.close()


def initialize():
    global B, C, M
    B = Board()
    C = B.color
    M = (0, 0)

    global HOST, PORT, CLIENT
    HOST = "localhost"
    PORT = int(sys.argv[1])
    CLIENT = socket.socket()


def terminate():
    print("terminate!\n")


def main():
    initialize()
    client()


main()
