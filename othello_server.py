import random
import time
import sys
import socket
import threading


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
SERVER = None

REFEREE = None
PLAYER1 = None
PLAYER2 = None
COLOR_OF_PLAYER = {"player1": None, "player2": None}
PLAYER_OF_COLOR = {"black": None, "player2": None}
SOCKET_OF_PLAYER = {"player1": None, "player2": None}

REF = None
PLY1 = None
PLY2 = None

START = None
END = None

MATCH = {"player1": None, "player2": None, "none": None}
TIME = {"player1": None, "player2": None}


# referee
def server0():
    global START, END
    global REF, PLY1, PLY2
    global B, C, M
    global PLAYER1, PLAYER2, PLAYER_OF_COLOR, COLOR_OF_PLAYER

    while True:
        #TODO: 初期化処理
        START = True
        END = False
        # PLAYER1 = None
        # PLAYER2 = None
        # REFEREE = None
        PLY1 = False
        PLY2 = False
        REF = True
        B = Board()
        TIME["player1"] = TIMELIMIT["player1"]
        TIME["player2"] = TIMELIMIT["player2"]
        ####
        while (PLAYER1 is None) or (PLAYER2 is None):
            pass
        # end while
        while True:
            if START:
                r = random.choice([True, False])
                PLY1 = True
                PLY2 = True
                REF = False
                START = False
                SOCKET_OF_PLAYER["player1"] = PLAYER1
                SOCKET_OF_PLAYER["player2"] = PLAYER2
                PLAYER_OF_COLOR["black"] = "player1" if r else "player2"
                PLAYER_OF_COLOR["white"] = "player2" if r else "player1"
                COLOR_OF_PLAYER["player1"] = "black" if r else "white"
                COLOR_OF_PLAYER["player2"] = "white" if r else "black"

                if r:
                    PLAYER1.send("1".encode("UTF-8"))
                    PLAYER2.send("0".encode("UTF-8"))
                else:
                    PLAYER1.send("0".encode("UTF-8"))
                    PLAYER2.send("1".encode("UTF-8"))
                # end else
                print_board(B.board, B.color, B.mycolor)
            elif END:
                b, w = (count_color(B.board, BLACK), count_color(B.board, WHITE))
                if b > w:
                    message = str(encode_result((1, b, w)))
                    SOCKET_OF_PLAYER[PLAYER_OF_COLOR["black"]].send(message.encode("UTF-8"))
                    message = str(encode_result((2, b, w)))
                    SOCKET_OF_PLAYER[PLAYER_OF_COLOR["white"]].send(message.encode("UTF-8"))
                    MATCH[PLAYER_OF_COLOR["black"]] += 1
                elif b < w:
                    message = str(encode_result((2, b, w)))
                    SOCKET_OF_PLAYER[PLAYER_OF_COLOR["black"]].send(message.encode("UTF-8"))
                    message = str(encode_result((1, b, w)))
                    SOCKET_OF_PLAYER[PLAYER_OF_COLOR["white"]].send(message.encode("UTF-8"))
                    MATCH[PLAYER_OF_COLOR["white"]] += 1
                else:
                    message = str(encode_result((3, b, w)))
                    SOCKET_OF_PLAYER[PLAYER_OF_COLOR["black"]].send(message.encode("UTF-8"))
                    message = str(encode_result((3, b, w)))
                    SOCKET_OF_PLAYER[PLAYER_OF_COLOR["white"]].send(message.encode("UTF-8"))
                    MATCH[PLAYER_OF_COLOR["none"]] += 1
                # end else
                break
            else:
                if PLY1 or PLY2:
                    continue
                if is_valid_move(B.board, B.color, M):
                    B.move(M)
                    print_board(B.board, B.color, B.mycolor)
                    if the_end(B.board, B.color):
                        message = str(tuple2int(M))
                        PLAYER1.send(message.encode("UTF-8"))
                        PLAYER2.send(message.encode("UTF-8"))
                        END = True
                    else:
                        if B.color == BLACK:
                            message = str(tuple2int(M) + 100)
                            SOCKET_OF_PLAYER[PLAYER_OF_COLOR["black"]].send(message.encode("UTF-8"))
                            message = str(tuple2int(M))
                            SOCKET_OF_PLAYER[PLAYER_OF_COLOR["white"]].send(message.encode("UTF-8"))
                        # end if
                        if B.color == WHITE:
                            message = str(tuple2int(M))
                            SOCKET_OF_PLAYER[PLAYER_OF_COLOR["black"]].send(message.encode("UTF-8"))
                            message = str(tuple2int(M) + 100)
                            SOCKET_OF_PLAYER[PLAYER_OF_COLOR["white"]].send(message.encode("UTF-8"))
                        # end if
                    # end if
                    REF = False
                    PLY1 = True
                    PLY2 = True
                else:
                    b, w = (count_color(B.board, BLACK), count_color(B.board, WHITE))
                    message = str(encode_result((0, b, w)))
                    SOCKET_OF_PLAYER[PLAYER_OF_COLOR["black"]].send(message.encode("UTF-8"))
                    message = str(encode_result((1, b, w)))
                    SOCKET_OF_PLAYER[PLAYER_OF_COLOR["white"]].send(message.encode("UTF-8"))
                    break
                # end if
            # end if
        # end while
        while PLAYER1 or PLAYER2:
            pass
        #TODO: 終了処理
        print("reached!")
        match = MATCH["player1"] + MATCH["player2"] + MATCH["none"]
        if match >= MATCHNUMBER:
            print("player1 wins %d times, player2 wins %d times (draw %d)." % (MATCH["player1"], MATCH["player2"], MATCH["none"]) )
            break
        ####
    # end while
# end def   


# player1
def server1():
    global START, END
    global REF, PLY1, PLY2
    global B, C, M

    global PLAYER1, PLAYER2
    while True:
        #TODO: 初期化処理
        # write here
        ####
        PLAYER1, _ = SERVER.accept()

        while PLAYER2 is None:
            print("player2 is None")
            time.sleep(1)
        # end while
        while True:
            if REF:
                continue
            # end if
            message = ""
            message = PLAYER1.recv(1024).decode("UTF-8")
            print("server1", message)
            if message == "":
                print("Connection disconnected...")
                PLAYER1 = None
                break
            # end if
            message = int(message)
            if message > 100:
                M = int2tuple(message - 100)
            # end if
            PLY1 = False
        # end while
        match = MATCH["player1"] + MATCH["player2"] + MATCH["none"]
        if match >= MATCHNUMBER:
            break
        # end if
    # end while
            

# player2
def server2():
    global START, END
    global REF, PLY1, PLY2
    global B, C, M

    global PLAYER1, PLAYER2
    while True:
        PLAYER2, _ = SERVER.accept()
        while PLAYER1 is None:
            print("player1 is None")
            time.sleep(1)
        # end if
        while True:
            if REF:
                continue
            # end if
            message = ""
            message = PLAYER2.recv(1024).decode("UTF-8")
            print("server2", message)
            if message == "":
                print("Connection disconnected...")
                PLAYER2 = None
                break
            # end if
            message = int(message)
            if message > 100:
                M = int2tuple(message - 100)
            # end if
            PLY2 = False
        # end while
        match = MATCH["player1"] + MATCH["player2"] + MATCH["none"]
        if match >= MATCHNUMBER:
            break
        # end if
    # end while


def initialize():
    global B, C, M
    global START, END
    global REF, PLY1, PLY2
    global MATCH
    global HOST, PORT, SERVER

    B = Board()
    C = B.color
    M = (0, 0)
    START = True
    END = False
    REF = True
    PLY1 = False
    PLY2 = False
    MATCH["player1"] = 0
    MATCH["player2"] = 0
    MATCH["none"] = 0
    HOST = "localhost"
    PORT = int(sys.argv[1])
    SERVER = socket.socket()
    SERVER.bind((HOST, PORT))
    SERVER.listen()


def terminate():
    global SERVER
    SERVER.close()
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
