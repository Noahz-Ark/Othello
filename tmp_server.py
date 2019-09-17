# module
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

MATCHSTART = None
MATCHEND = None
GAMESTART = None
GAMEEND = None

R = None
RESULT = {"player1": None, "player2": None, "none": None}
TIME = {"player1": None, "player2": None}

B = None
C = None
M = None

def main():
    referee = threading.Thread(target=referee_server)
    player1 = threading.Thread(target=player1_server)
    player2 = threading.Thread(target=player2_server)
    referee.start()
    player1.start()
    player2.start()
    referee.join()
    player1.join()
    player2.join()

# referee
def referee_server():
    global HOST, PORT, SERVER, SOCKET_OF_PLAYER
    global REFEREE, PLAYER1, PLAYER2, REF, PLY1, PLY2
    global COLOR_OF_PLAYER, PLAYER_OF_COLOR
    global MATCHSTART, MATCHEND, GAMESTART, GAMEEND
    global R, RESULT, TIME
    global B, C, M

    initialize_match(0)
    (message1, message2) = ("10000000", "10000000")
    PLAYER1.send(message1.encode("UTF-8"))
    PLAYER2.send(message2.encode("UTF-8"))
    
    while True:
        initalize_game(0)

        while True:
            # TODO: 必要？
            if PLY1 or PLY2:
                continue

            if GAMESTART:
                (message1, message2) = ("31000000", "32000000") if R else ("32000000", "31000000")
                SOCKET_OF_PLAYER[COLOR_OF_PLAYER["black"]].send(message1.encode("UTF-8"))
                SOCKET_OF_PLAYER[COLOR_OF_PLAYER["white"]].send(message2.encode("UTF-8"))
                GAMESTART = False
                print_board(B.board, B.color, B.mycolor)
            elif GAMEEND:
                (b, w) = (count_color(B.board, BLACK), count_color(B.board, WHITE))
                (b, w) = (str(b), str(w))
                if b > w:
                    (message1, message2) = ("411%s%s0"%(b,w), "412%s%s0"%(b,w))
                    RESULT[PLAYER_OF_COLOR["black"]] += 1
                elif b < w:
                    (message1, message2) = ("412%s%s0"%(b,w), "411%s%s0"%(b,w))
                    RESULT[PLAYER_OF_COLOR["white"]] += 1
                else:
                    (message1, message2) = ("413%s%s0"%(b,w), "413%s%s0"%(b,w))
                    RESULT[PLAYER_OF_COLOR["none"]] += 1
                SOCKET_OF_PLAYER[PLAYER_OF_COLOR["black"]].send(message1.encode("UTF-8"))
                SOCKET_OF_PLAYER[PLAYER_OF_COLOR["white"]].send(message2.encode("UTF-8"))
                GAMEEND = False
                print_board(B.board, B.color, B.mycolor)
                break
            else:
                if is_valid_move(B.board, B.color, M):
                    B.move(M)
                    if the_end(B.board, B.color):
                        if B.color == BLACK:
                            m = str(M)
                            (message1, message2) = ("51%s0000"%(m), "53%s0000"%(m))
                            SOCKET_OF_PLAYER[PLAYER_OF_COLOR["black"]].send(message1.encode("UTF-8"))
                            SOCKET_OF_PLAYER[PLAYER_OF_COLOR["white"]].send(message2.encode("UTF-8"))
                        elif B.color == WHITE:
                            (message1, message2) = ("53%s0000"%(m), "51%s0000"%(m))
                            SOCKET_OF_PLAYER[PLAYER_OF_COLOR["black"]].send(message1.encode("UTF-8"))
                            SOCKET_OF_PLAYER[PLAYER_OF_COLOR["white"]].send(message2.encode("UTF-8"))
                        elif B.color == NONE:
                            pass
                        GAMEEND = True
                    else:
                        if B.color == BLACK:
                            m = str(M)
                            (message1, message2) = ("52%s0000"%(m), "54%s0000"%(m))
                            SOCKET_OF_PLAYER[PLAYER_OF_COLOR["black"]].send(message1.encode("UTF-8"))
                            SOCKET_OF_PLAYER[PLAYER_OF_COLOR["white"]].send(message2.encode("UTF-8"))
                        elif B.color == WHITE:
                            (message1, message2) = ("54%s0000"%(m), "52%s0000"%(m))
                            SOCKET_OF_PLAYER[PLAYER_OF_COLOR["black"]].send(message1.encode("UTF-8"))
                            SOCKET_OF_PLAYER[PLAYER_OF_COLOR["white"]].send(message2.encode("UTF-8"))
                        elif B.color == NONE:
                            pass

                    REF = False
                    PLY1 = True
                    PLY2 = True
                    print_board(B.board, B.color, B.mycolor)
                else:
                    (b, w) = (count_color(B.board, BLACK), count_color(B.board, WHITE))
                    (b, w) = (str(b), str(w))
                    if B.color == BLACK:
                        (message1, message2) = ("421%s%s0"%(b,w), "422%s%s0"%(b,w))
                    elif B.color == WHITE:
                        (message1, message2) = ("422%s%s0"%(b,w), "421%s%s0"%(b,w))
                    else:
                        pass
                    SOCKET_OF_PLAYER[PLAYER_OF_COLOR["black"]].send(message1.encode("UTF-8"))
                    SOCKET_OF_PLAYER[PLAYER_OF_COLOR["white"]].send(message2.encode("UTF-8"))
                    break

        (message1, message2) = ("20000000", "20000000")
        PLAYER1.send(message1.encode("UTF-8"))
        PLAYER2.send(message1.encode("UTF-8"))
        terminate_game(0)

        cnt = RESULT["player1"] + RESULT["player2"] + RESULT["none"]
        if cnt >= MATCHNUMBER:
            print("player1 wins %d times, player2 wins %d times (draw %d)." % (MATCH["player1"], RESULT["player2"], RESULT["none"]))
            break

    (message1, message2) = ("20000000", "20000000")
    PLAYER1.send(message1.encode("UTF-8"))
    PLAYER2.send(message1.encode("UTF-8"))
    terminate_match(0)

def player1_server():
    global HOST, PORT, SERVER, SOCKET_OF_PLAYER
    global REFEREE, PLAYER1, PLAYER2, REF, PLY1, PLY2
    global COLOR_OF_PLAYER, PLAYER_OF_COLOR
    global MATCHSTART, MATCHEND, GAMESTART, GAMEEND
    global R, RESULT, TIME
    global B, C, M

    initialize_match(1)

    while True:
        initialize_game(1)
        while True:
            #TODO: 必要？
            if not(PLY1) or REF:
                continue
            message1 = ""
            message1 = PLAYER1.recv(1024).decode("UTF-8")
            print("server1", message1)

            # TODO: 通信をclientから切断されたらどうする？
            if message1 == "":
                print("Disconnected...")
                PLAYER1 = None
                break
            else:
                try:
                    message1 = int(message1)
                    if message1/1000000 == 55:
                        message1 %= 1000000
                        message1 /= 10000
                        M = str(message1)
                        print(message1)
                    elif message1/1000000 == 56:
                        message1 %= 1000000
                        message1 /= 10000
                        print(message1)
                    else:
                        raise ValueError
                except:
                    print("Error occurred!")
                    SERVER.close()
                    break

            PLY1 = False
        
        terminate_game(1)
    
    terminate_match(1)


def player2_server():
    global HOST, PORT, SERVER, SOCKET_OF_PLAYER
    global REFEREE, PLAYER1, PLAYER2, REF, PLY1, PLY2
    global COLOR_OF_PLAYER, PLAYER_OF_COLOR
    global MATCHSTART, MATCHEND, GAMESTART, GAMEEND
    global R, RESULT, TIME
    global B, C, M

    initialize_match(1)

    while True:
        initialize_game(2)
        while True:
            #TODO: 必要？
            if not(PLY2) or REF:
                continue
            message2 = ""
            message2 = PLAYER2.recv(1024).decode("UTF-8")
            print("server2", message2)

            if message2 == "":
                print("Disconnected...")
                PLAYER2 = None
                break
            else:
                try:
                    message2 = int(message2)
                    if message2/1000000 == 55:
                        message2 %= 1000000
                        message2 /= 10000
                        M = str(message2)
                        print(message2)
                    elif message1/1000000 == 56:
                        message2 %= 1000000
                        message2 /= 10000
                        print(message2)
                    else:
                        raise ValueError
                except:
                    print("Error occurred!")
                    SERVER.close()
                    break

            PLY2 = False

        terminate_game(2)
    
    terminate_match(2)



def initialize_match(n):
    global HOST, PORT, SERVER, SOCKET_OF_PLAYER
    global REFEREE, PLAYER1, PLAYER2, REF, PLY1, PLY2
    global COLOR_OF_PLAYER, PLAYER_OF_COLOR
    global MATCHSTART, MATCHEND, GAMESTART, GAMEEND
    global R, RESULT, TIME
    global B, C, M

    # referee
    if n == 0:
        REFEREE = "referee" # This variable has no meaning
        (REF, PLY1, PLY2) = (True, False, False)
        (MATCHSTART, MATCHEND) = (True, False)

        R = random.choice([True, False])
        PLAYER_OF_COLOR["black"] = "player1" if R else "player2"
        PLAYER_OF_COLOR["white"] = "player2" if R else "player1"
        COLOR_OF_PLAYER["player1"] = "black" if R else "white"
        COLOR_OF_PLAYER["player2"] = "white" if R else "black"

        (RESULT["player1"], RESULT["player2"], RESULT["none"] = (0, 0, 0)

        HOST = "localhost"
        PORT = int(sys.argv[1])
        SERVER = socket.socket()
        SERVER.bind((HOST, PORT))
        SERVER.listen()

    # player1
    elif n == 1:
        PLAYER1, _ = SERVER.accept()
        SOCKET_OF_PLAYER["player1"] = PLAYER1

    # player2:
    elif n == 2:
        PLAYER2, _ = SERVER.accept()
        SOCKET_OF_PLAYER["player2"] = PLAYER2

    while (REFEREE is None) or (PLAYER1 is None) or (PLAYER2 is None):
        pass


def initialize_game(n):
    global HOST, PORT, SERVER, SOCKET_OF_PLAYER
    global REFEREE, PLAYER1, PLAYER2, REF, PLY1, PLY2
    global COLOR_OF_PLAYER, PLAYER_OF_COLOR
    global MATCHSTART, MATCHEND, GAMESTART, GAMEEND
    global R, RESULT, TIME
    global B, C, M

    # referee
    if n == 0:
        (GAMESTART, GAMEEND) = (True, False)
        (TIME["player1"], TIME["player2"]) = (TIMELIMIT["player1"], TIMELIMIT["player2"])
        B = Board()
        C = B.color
        M = 0
    # player1
    elif n == 1:
        pass
    # player2
    elif n == 2:
        pass


def terminate_match(n):
    global HOST, PORT, SERVER, SOCKET_OF_PLAYER
    global REFEREE, PLAYER1, PLAYER2, REF, PLY1, PLY2
    global COLOR_OF_PLAYER, PLAYER_OF_COLOR
    global MATCHSTART, MATCHEND, GAMESTART, GAMEEND
    global R, RESULT, TIME
    global B, C, M

    # referee
    if n == 0:
        pass
    # player1
    elif n == 1:
        pass
    # player2
    elif n == 2:
        pass


def terminate_game(n):
    global HOST, PORT, SERVER, SOCKET_OF_PLAYER
    global REFEREE, PLAYER1, PLAYER2, REF, PLY1, PLY2
    global COLOR_OF_PLAYER, PLAYER_OF_COLOR
    global MATCHSTART, MATCHEND, GAMESTART, GAMEEND
    global R, RESULT, TIME
    global B, C, M

    # referee
    if n == 0:
        pass
    # player1
    elif n == 1:
        pass
    # player2
    elif n == 2:
        pass
    







            








