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
PLAYER_COLOR = {}

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
                PLY2 = False
                REF = False
                START = False
                PLAYER_COLOR["black"] = PLAYER1
                PLAYER_COLOR["white"] = PLAYER2
                PLAYER1.send("0".encode("UTF-8"))
            else:
                PLY1 = False
                PLY2 = True
                REF = False
                START = False
                PLAYER_COLOR["black"] = PLAYER2
                PLAYER_COLOR["white"] = PLAYER1
                PLAYER2.send("0".encode("UTF-8"))
        elif END:
            b, w = (count_color(B.board, BLACK), count_color(B.board, WHITE))
            if b > w:
                message = str(encode_result((0, b, w)))
                PLAYER_COLOR["black"].send(message.encode("UTF-8"))
                message = str(encode_result((1, b, w)))
                PLAYER_COLOR["white"].send(message.encode("UTF-8"))
            elif b < w:
                message = str(encode_result((0, b, w)))
                PLAYER_COLOR["black"].send(message.encode("UTF-8"))
                message = str(encode_result((1, b, w)))
                PLAYER_COLOR["white"].send(message.encode("UTF-8"))
            else:
                message = str(encode_result((2, b, w)))
                PLAYER_COLOR["black"].send(message.encode("UTF-8"))
                message = str(encode_result((2, b, w)))
                PLAYER_COLOR["white"].send(message.encode("UTF-8"))
            break
        else:
            # FIXME: valid_colorでPASSに対応できるようにする
            # FIXME: 送信するメッセージの体裁を変更する
            # FIXME: 2playersに送信するが、最上位の0/1で自分の番かどうか決める
            if the_end(B.board, B.color):
                END = True
                continue
            if not(REF) or (not(PLY1) and not(PLY2)):
                continue
            if PLY1:
                print_board(B.board, B.color, B.mycolor)
                if is_valid_move(B.board, B.color, M):
                    B.move(M)
                    REF = False
                    PLY1 = False
                    PLY2 = True
                    message = str(tuple2int(M))
                    PLAYER2.send(message.encode("UTF-8"))
                else:
                    b, w = (count_color(B.board, BLACK), count_color(B.board, WHITE))
                    message = str(encode_result((0, b, w)))
                    PLAYER2.send(message.encode("UTF-8"))
                    message = str(encode_result((1, b, w)))
                    PLAYER1.send(message.encode("UTF-8"))
                    break
            elif PLY2:
                print_board(B.board, B.color, B.mycolor)
                if is_valid_move(B.board, B.color, M):
                    B.move(M)
                    REF = False
                    PLY2 = False
                    PLY1 = True
                    message = str(tuple2int(M))
                    PLAYER1.send(message.encode("UTF-8"))
                else:
                    b, w = (count_color(B.board, BLACK), count_color(B.board, WHITE))
                    message = str(encode_result((0, b, w)))
                    PLAYER1.send(message.encode("UTF-8"))
                    message = str(encode_result((1, b, w)))
                    PLAYER2.send(message.encode("UTF-8"))
                    break
            else:
                print("???\n")
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
        if REF or not(PLY1):
            continue
        message = ""
        message = PLAYER1.recv(1024).decode("UTF-8")
        if message:
            M = int2tuple(int(message))
            REF = True


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
        if REF or not(PLY2):
            continue
        message = ""
        message = PLAYER2.recv(1024).decode("UTF-8")
        if message:
            M = int2tuple(int(message))
            REF = True


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
