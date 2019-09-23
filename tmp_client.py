import random
import sys
import time
import socket

# configuration
from othello_configuration import *
from othello_configuration_editable import *

# window
from othello_window import *

# class
from othello_board import *

# algorithm
from othello_ai import *
from othello_ai_editable import *

# global variable
HOST = None
PORT = None
CLIENT = None

BOARD = None
TIME = None
FLAG = None


def main():
    client()


def client():
    global CLIENT
    global BOARD
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
                BOARD.color = BLACK
                BOARD.mycolor = BLACK
                print_board(BOARD.board, BOARD.color, BOARD.mycolor)
                
                mystone = AI(BOARD)
                mystone = tuple2int(mystone)
                message_s = write_message([55, mystone])
                send_message(message_s)
            # gamestart, second
            elif message[0] == 32:
                BOARD.color = BLACK
                BOARD.mycolor = WHITE
                print_board(BOARD.board, BOARD.color, BOARD.mycolor)
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
                print_board(BOARD.board, BOARD.color, BOARD.mycolor)
                break
            # on going
            elif message[0] == 51:
                mystone = int2tuple(message[1])
                BOARD.move(mystone)
                print_board(BOARD.board, BOARD.color, BOARD.mycolor)
            elif message[0] == 52:
                mystone = int2tuple(message[1])
                BOARD.move(mystone)
                print_board(BOARD.board, BOARD.color, BOARD.mycolor)
                message_s = write_message([56, message[1]])
                send_message(message_s)
            elif message[0] == 53:
                opstone = int2tuple(message[1])
                BOARD.move(opstone)
                print_board(BOARD.board, BOARD.color, BOARD.mycolor)
            elif message[0] == 54:
                opstone = int2tuple(message[1])
                BOARD.move(opstone)
                print_board(BOARD.board, BOARD.color, BOARD.mycolor)

                mystone = AI(BOARD)
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
    message = str(array[0])
    if array[0] == 55 or array[0] == 56 or array[0] == 57:
        message += str(array[1]) + "0000"
    return message


def initialize_match():
    global HOST, PORT, CLIENT
    global FLAG

    FLAG = False
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    CLIENT = socket.socket()
    CLIENT.connect((HOST, PORT))


def initialize_game():
    global BOARD
    global TIME
    TIME = TIMELIMIT
    BOARD = Board()


def terminate_match():
    pass
    

def terminate_game():
    pass


if __name__ == "__main__":
    main()
