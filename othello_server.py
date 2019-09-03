import random
import sys
import socket
import threading


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
SERVER = None

REFEREE = None
PLAYER1 = None
PLAYER2 = None
COLOR_OF_PLAYER = {}
PLAYER_OF_COLOR = {}

REF = True
PLY1 = False
PLY2 = False

START = True
END = False


# referee
def server0():
    global START, END
    global REF, PLY1, PLY2
    global B, C, M
    global PLAYER1, PLAYER2, PLAYER_COLOR

    while (PLAYER1 is None) or (PLAYER2 is None):
        pass
    while True:
        if START:
            r = random.choice([True, False])
            if r:
                PLY1 = True
                PLY2 = True
                REF = False
                START = False
                PLAYER_OF_COLOR["black"] = PLAYER1
                PLAYER_OF_COLOR["white"] = PLAYER2
                COLOR_OF_PLAYER["player1"] = BLACK
                COLOR_OF_PLAYER["player2"] = WHITE
                PLAYER1.send("1".encode("UTF-8"))
                PLAYER2.send("0".encode("UTF-8"))
            else:
                PLY1 = True
                PLY2 = True
                REF = False
                START = False
                PLAYER_OF_COLOR["black"] = PLAYER2
                PLAYER_OF_COLOR["white"] = PLAYER1
                COLOR_OF_PLAYER["player2"] = BLACK
                COLOR_OF_PLAYER["player1"] = WHITE
                PLAYER1.send("0".encode("UTF-8"))
                PLAYER2.send("1".encode("UTF-8"))
            print_board(B.board, B.color, B.mycolor)
        elif END:
            b, w = (count_color(B.board, BLACK), count_color(B.board, WHITE))
            if b > w:
                message = str(encode_result((0, b, w)))
                PLAYER_OF_COLOR["black"].send(message.encode("UTF-8"))
                message = str(encode_result((1, b, w)))
                PLAYER_OF_COLOR["white"].send(message.encode("UTF-8"))
            elif b < w:
                message = str(encode_result((1, b, w)))
                PLAYER_OF_COLOR["black"].send(message.encode("UTF-8"))
                message = str(encode_result((0, b, w)))
                PLAYER_OF_COLOR["white"].send(message.encode("UTF-8"))
            else:
                message = str(encode_result((2, b, w)))
                PLAYER_OF_COLOR["black"].send(message.encode("UTF-8"))
                message = str(encode_result((2, b, w)))
                PLAYER_OF_COLOR["white"].send(message.encode("UTF-8"))
            break
        else:
            if the_end(B.board, B.color):
                END = True
                continue
            if PLY1 or PLY2:
                continue

            if is_valid_move(B.board, B.color, M):
                B.move(M)
                print_board(B.board, B.color, B.mycolor)
                if B.color == BLACK:
                    message = str(tuple2int(M) + 100)
                    PLAYER_OF_COLOR["black"].send(message.encode("UTF-8"))
                    message = str(tuple2int(M))
                    PLAYER_OF_COLOR["white"].send(message.encode("UTF-8"))
                if B.color == WHITE:
                    message = str(tuple2int(M))
                    PLAYER_OF_COLOR["black"].send(message.encode("UTF-8"))
                    message = str(tuple2int(M) + 100)
                    PLAYER_OF_COLOR["white"].send(message.encode("UTF-8"))
                REF = False
                PLY1 = True
                PLY2 = True
            else:
                b, w = (count_color(B.board, BLACK), count_color(B.board, WHITE))
                message = str(encode_result((0, b, w)))
                PLAYER_OF_COLOR["black"].send(message.encode("UTF-8"))
                message = str(encode_result((1, b, w)))
                PLAYER_OF_COLOR["white"].send(message.encode("UTF-8"))
                break


# player1
def server1():
    global START, END
    global REF, PLY1, PLY2
    global B, C, M

    global PLAYER1, PLAYER2
    PLAYER1, _ = SERVER.accept()
    while PLAYER2 is None:
        pass
    while True:
        if END:
            break
        if REF:
            continue
        message = ""
        message = PLAYER1.recv(1024).decode("UTF-8")
        print("server1", message)
        message = int(message)
        if message > 100:
            M = int2tuple(message - 100)
        PLY1 = False
            

# player2
def server2():
    global START, END
    global REF, PLY1, PLY2
    global B, C, M

    global PLAYER1, PLAYER2
    PLAYER2, _ = SERVER.accept()
    while PLAYER1 is None:
        pass
    while True:
        if END:
            break
        if REF:
            continue
        message = ""
        message = PLAYER2.recv(1024).decode("UTF-8")
        print("server2", message)
        message = int(message)
        if message > 100:
            M = int2tuple(message - 100)
        PLY2 = False


def initialize():
    global B, C, M
    global HOST, PORT, SERVER
    B = Board()
    C = B.color
    M = (0, 0)
    HOST = "localhost"
    PORT = int(sys.argv[1])
    SERVER = socket.socket()
    SERVER.bind((HOST, PORT))
    SERVER.listen()


def terminate():
    print("terminate!\n")


def main():
    initialize()
    referee = threading.Thread(target=server0)
    player1 = threading.Thread(target=server1)
    player2 = threading.Thread(target=server2)
    referee.start()
    player1.start()
    player2.start()
    referee.join()
    player1.join()
    player2.join()
    terminate()


main()
