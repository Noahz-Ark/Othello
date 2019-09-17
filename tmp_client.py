import random
import sys
import socket

# macro
from variable import *
from method import *
from setting import *

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
REF = None
PLY1 = None
PLY2 = None

TIME = None


def main():
    client()


def client():
    global CLIENT
    global B, C, M

    initialize_match()
    message = ""
    message = CLIENT.recv(1024).decode("UTF-8")
    validate_message(message)

    while True:
        initialize_game()

        while True:



    while True:
        message = ""
        message = CLIENT.recv(1024).decode("UTF-8")
        print("server1", message)
        if message == "":
            print("Connection disconnected...")
        # end if
        message = int(message)

        if message < 0:
            break

        # first (not my turn)
        elif message == 0:
            B.color = BLACK
            B.mycolor = WHITE
            print_board(B.board, B.color, B.mycolor)
            message = str(message)
            CLIENT.send(message.encode("UTF-8"))

        # first (my turn)
        elif message == 1:
            B.color = BLACK
            B.mycolor = BLACK
            print_board(B.board, B.color, B.mycolor)
            # TODO: change here
            mystone = B.random_choice()
            ####################
            B.move(mystone)
            message = str(tuple2int(mystone) + 100)
            M = tuple2int(mystone)
            CLIENT.send(message.encode("UTF-8"))

        # not first (not my turn)
        elif message < 100:
            if M != message:
                opstone = int2tuple(message)
                B.move(opstone)
            print_board(B.board, B.color, B.mycolor)
            if not the_end(B.board, B.color):
                message = str(message)
                CLIENT.send(message.encode("UTF-8"))

        # not first (my turn)
        elif message < 200:
            message = message % 100
            opstone = int2tuple(message)
            B.move(opstone)
            print_board(B.board, B.color, B.mycolor)

            if not the_end(B.board, B.color):
                # TODO: change here
                mystone = B.random_choice()
                ####################
                B.move(mystone)
                message = str(tuple2int(mystone) + 100)
                M = tuple2int(mystone)
                CLIENT.send(message.encode("UTF-8"))
        # win
        elif message < 20000:
            (_, b, w) = decode_result(message)
            print("Win!\n")
            print("black", b, " vs ", w, "white\n")
            print_board(B.board, B.color, B.mycolor)
            CLIENT.close()
            break
        # lose
        elif message < 30000:
            (_, b, w) = decode_result(message)
            print("Lose!\n")
            print("black", b, " vs ", w, "white\n")
            print_board(B.board, B.color, B.mycolor)
            CLIENT.close()
            break
        # draw
        elif message < 40000:
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


def validate_message(m):
    global CLIENT
    if m == "":
        print("Disconnected...")
        return
    else:
        try:
            message = int(m)
            message_val = message/1000000
            if message_val == 0:
                print("error")
            elif message_val == 10:
                print("match start")
            elif message_val == 20:
                print("match end")
            elif message_val == 31:
                print("game start, first")
            elif message_val == 32:
                print("game start, second")
            elif message_val == 41:
                print("game end(normally)")
            elif message_val == 42:
                print("game end(abnormally)")
            elif message_val == 51:
                print("next message will be 4********")
            elif message_val == 52:
                print("next message will be 5********")
            elif message_val == 53:
                print("next message will be 4********")
            elif message_val == 54:
                print("next message will be 5********")
            else:
                pass
        except:
            pass




def initialize_match():
    global HOST, PORT, CLIENT

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    CLIENT = socket.socket()
    CLIENT.connect((HOST, PORT))


def initialize_game():
    global B, C, M
    global TIME

    TIME = TIMELIMIT

    B = Board()
    C = B.color
    M = 0


def terminate_match():
    pass
    

def terminate_game():
    pass

main()
