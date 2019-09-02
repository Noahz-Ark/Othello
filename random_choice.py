import random
import sys
import socket


# macro
from variable import *
from method import *


# global method
from board import is_valid_move, valid_moves, count_color, the_end, print_board


# class
from board import Board


# global variable
B = None
C = None
M = None

HOST = None
PORT = None
CLIENT = None

REFEREE = None
PLAYER1 = None
PLAYER2 = None
REF = True
PLY1 = False
PLY2 = False

START = True
END = False


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
        # first
        elif message == 0:
            print_board(B.board, B.color, B.mycolor)
            # TODO: change here
            mystone = B.random_choice()
            ####################
            B.move(mystone)
            message = str(tuple2int(mystone))
            CLIENT.send(message.encode("UTF-8"))
        # not first
        elif message < 100:
            opstone = int2tuple(message)
            B.move(opstone)
            print_board(B.board, B.color, B.mycolor)

            if the_end(B.board, B.color):
                pass
            else:
                # TODO: change here
                mystone = B.random_choice()
                ####################
                B.move(mystone)
                message = str(tuple2int(mystone))
                CLIENT.send(message.encode("UTF-8"))
        # win
        elif message < 10000:
            (_, b, w) = decode_result(message)
            print("Win!\n")
            print("black", b, " vs ", w, "white\n")
            print_board(B.board, B.color, B.mycolor)
            CLIENT.close()
            break
        # lose
        elif message < 20000:
            (_, b, w) = decode_result(message)
            print("Lose!\n")
            print("black", b, " vs ", w, "white\n")
            print_board(B.board, B.color, B.mycolor)
            CLIENT.close()
            break
        # draw
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
    global HOST, PORT, CLIENT
    B = Board()
    C = B.color
    M = (0, 0)
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    CLIENT = socket.socket()


def terminate():
    print("terminate!\n")


def main():
    initialize()
    client()


main()
