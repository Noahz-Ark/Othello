import random
import sys
import time
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
    global FLAG

    initialize_match()
    message_r = receive_message()
    message = read_message(message_r)
    if message[0] == 10:
        print("match start")

    while True:
        initialize_game()

        while True:
            message_r = receive_message()
            print("message_r: ", message_r)
            if message_r == 0:
                return
            message = read_message(message_r)

            # matchend
            if message[0] == 20:
                FLAG = True
                break

            # gamestart, first
            elif message[0] == 31:
                B.color = BLACK
                B.mycolor = BLACK
                print_board(B.board, B.color, B.mycolor)
                # TODO:
                mystone = B.random_choice()
                ####
                mystone = tuple2int(mystone)
                message_s = write_message([55, mystone])
                send_message(message_s)
            # gamestart, second
            elif message[0] == 32:
                B.color = BLACK
                B.mycolor = WHITE
                print_board(B.board, B.color, B.mycolor)
                mystone = 99
                message_s = write_message([57, mystone])
                send_message(message_s)

            # gameend
            if message[0] == 41 or message[0] == 42:
                (wel, b, w) = (message[1], message[2], message[3])
                if wel == 1:
                    print("Win!\n")
                elif wel == 2:
                    print("Lose\n")
                else:
                    print("Even\n")
                print("black", b, " vs ", w, "white\n")
                print_board(B.board, B.color, B.mycolor)
                break
            # on going
            elif message[0] == 51:
                mystone = int2tuple(message[1])
                B.move(mystone)
                print_board(B.board, B.color, B.mycolor)
            elif message[0] == 52:
                mystone = int2tuple(message[1])
                B.move(mystone)
                print_board(B.board, B.color, B.mycolor)
                message_s = write_message([56, message[1]])
                send_message(message_s)
            elif message[0] == 53:
                opstone = int2tuple(message[1])
                B.move(opstone)
                print_board(B.board, B.color, B.mycolor)
            elif message[0] == 54:
                opstone = int2tuple(message[1])
                B.move(opstone)
                print_board(B.board, B.color, B.mycolor)
                # TODO:
                mystone = B.random_choice()
                ####
                mystone = tuple2int(mystone)
                message_s = write_message([55, mystone])
                send_message(message_s)

        if FLAG:
            break
        terminate_game()

    terminate_match()


def receive_message():
    global CLIENT
    message_r = ""
    message_r = CLIENT.recv(1024).decode("UTF-8")

    if message_r == "":
        print("disconnected...")
        return 0
    else:
        try:
            message = int(message_r)
            return message
        except:
            return -1


def send_message(message):
    global CLIENT
    message_s = message.encode("UTF-8")
    CLIENT.send(message_s)


def read_message(abcdefgh):
    array = []
    ab = abcdefgh // 1000000
    array.append(ab)
    if ab == 41 or ab == 42:
        cdefgh = abcdefgh % 1000000
        c = cdefgh // 100000
        defgh = cdefgh % 100000
        de = defgh // 1000
        fgh = defgh % 1000
        fg = fgh // 10
        array.extend([c, de, fg])
    elif ab == 51 or ab == 52 or ab == 53 or ab == 54:
        cdefgh = abcdefgh % 1000000
        cd = cdefgh // 10000
        array.append(cd)
    return array


def write_message(array):
    return str(array[0]) + str(array[1]) + "0000"


def initialize_match():
    global HOST, PORT, CLIENT
    global FLAG

    FLAG = False

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    CLIENT = socket.socket()
    CLIENT.connect((HOST, PORT))


def initialize_game():
    global B, C, M
    global TIME

    print("initialize game!")

    TIME = TIMELIMIT

    B = Board()
    C = B.color
    M = 0


def terminate_match():
    pass
    

def terminate_game():
    pass

main()
