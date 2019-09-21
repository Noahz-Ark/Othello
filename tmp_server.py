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
        initialize_game(0)

        while True:
            if (not(REF) and PLY1) or (not(REF) and PLY2):
                continue

            if GAMESTART:
                print("GAMESTART")
                (message1, message2) = ("31000000", "32000000") if R else ("32000000", "31000000")
                SOCKET_OF_PLAYER[PLAYER_OF_COLOR["black"]].send(message1.encode("UTF-8"))
                SOCKET_OF_PLAYER[PLAYER_OF_COLOR["white"]].send(message2.encode("UTF-8"))
                GAMESTART = False
                # REF = False
                PLY1 = True
                PLY2 = True
                # print_board(B.board, B.color, B.mycolor)
            elif GAMEEND:
                print("GAMEEND")
                (b, w) = (count_color(B.board, BLACK), count_color(B.board, WHITE))
                if b > w:
                    message1 = write_message([41, 1, b, w])
                    message2 = write_message([41, 2, b, w])
                    RESULT[PLAYER_OF_COLOR["black"]] += 1
                elif b < w:
                    message1 = write_message([41, 2, b, w])
                    message2 = write_message([41, 1, b, w])
                    RESULT[PLAYER_OF_COLOR["white"]] += 1
                else:
                    message1 = write_message([41, 3, b, w])
                    message2 = write_message([41, 3, b, w])
                    RESULT[PLAYER_OF_COLOR["none"]] += 1
                SOCKET_OF_PLAYER[PLAYER_OF_COLOR["black"]].send(message1.encode("UTF-8"))
                SOCKET_OF_PLAYER[PLAYER_OF_COLOR["white"]].send(message2.encode("UTF-8"))
                GAMEEND = False
                # REF = True
                PLY1 = True
                PLY2 = True
                print_board(B.board, B.color, B.mycolor)
                break
            else:
                if is_valid_move(B.board, B.color, M):
                    C = B.color
                    B.move(M)
                    if the_end(B.board, B.color):
                        if C == BLACK:
                            m = tuple2int(M)
                            message1 = write_message([51, m])
                            message2 = write_message([53, m])
                            print(message1, message2)
                            SOCKET_OF_PLAYER[PLAYER_OF_COLOR["black"]].send(message1.encode("UTF-8"))
                            SOCKET_OF_PLAYER[PLAYER_OF_COLOR["white"]].send(message2.encode("UTF-8"))
                        elif C == WHITE:
                            m = tuple2int(M)
                            message1 = write_message([53, m])
                            message2 = write_message([51, m])
                            print(message1, message2)
                            SOCKET_OF_PLAYER[PLAYER_OF_COLOR["black"]].send(message1.encode("UTF-8"))
                            SOCKET_OF_PLAYER[PLAYER_OF_COLOR["white"]].send(message2.encode("UTF-8"))
                        elif C == NONE:
                            pass
                        GAMEEND = True
                        REF = True

                    else:
                        if B.color == BLACK:
                            m = tuple2int(M)
                            message1 = write_message([52, m])
                            message2 = write_message([54, m])
                            print(message1, message2)
                            SOCKET_OF_PLAYER[PLAYER_OF_COLOR["black"]].send(message1.encode("UTF-8"))
                            SOCKET_OF_PLAYER[PLAYER_OF_COLOR["white"]].send(message2.encode("UTF-8"))
                        elif B.color == WHITE:
                            m = tuple2int(M)
                            message1 = write_message([54, m])
                            message2 = write_message([52, m])
                            print(message1, message2)
                            SOCKET_OF_PLAYER[PLAYER_OF_COLOR["black"]].send(message1.encode("UTF-8"))
                            SOCKET_OF_PLAYER[PLAYER_OF_COLOR["white"]].send(message2.encode("UTF-8"))
                        elif B.color == NONE:
                            pass

                    # REF = False
                    PLY1 = True
                    PLY2 = True
                    print_board(B.board, B.color, B.mycolor)
                else:
                    (b, w) = (count_color(B.board, BLACK), count_color(B.board, WHITE))
                    if B.color == BLACK:
                        message1 = write_message([42, 1, b, w])
                        message2 = write_message([42, 2, b, w])
                        RESULT[PLAYER_OF_COLOR["black"]] += 1
                    elif B.color == WHITE:
                        message1 = write_message([42, 2, b, w])
                        message2 = write_message([42, 1, b, w])
                        RESULT[PLAYER_OF_COLOR["white"]] += 1
                    else:
                        pass
                    SOCKET_OF_PLAYER[PLAYER_OF_COLOR["black"]].send(message1.encode("UTF-8"))
                    SOCKET_OF_PLAYER[PLAYER_OF_COLOR["white"]].send(message2.encode("UTF-8"))
                    break

        terminate_game(0)

        cnt = RESULT["player1"] + RESULT["player2"] + RESULT["none"]
        if cnt >= MATCHNUMBER:
            MATCHEND = True
            print("player1 wins %d times, player2 wins %d times (draw %d)." % (RESULT["player1"], RESULT["player2"], RESULT["none"]))
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
            if GAMEEND:
                break
            if not(PLY1):
                continue
            message1_r = ""
            message1_r = PLAYER1.recv(1024).decode("UTF-8")
            # print("server1", message1_r)

            # TODO: 通信をclientから切断されたらどうする？
            # 基本的にはこちらから切りたい
            if message1_r == "":
                print("Disconnected...")
                PLAYER1 = None
                break
            else:
                try:
                    message1_r = int(message1_r)
                    message1 = read_message(message1_r)
                    if message1[0] == 55:
                        M = int2tuple(message1[1])
                    elif message1[0] == 56:
                        pass
                    elif message1[0] == 57:
                        pass
                    else:
                        raise ValueError

                except:
                    import traceback
                    traceback.print_exc()

                    print("Error occurred!")
                    SERVER.close()
                    break

            PLY1 = False

        if MATCHEND:
            break
        
        terminate_game(1)
    
    terminate_match(1)


def player2_server():
    global HOST, PORT, SERVER, SOCKET_OF_PLAYER
    global REFEREE, PLAYER1, PLAYER2, REF, PLY1, PLY2
    global COLOR_OF_PLAYER, PLAYER_OF_COLOR
    global MATCHSTART, MATCHEND, GAMESTART, GAMEEND
    global R, RESULT, TIME
    global B, C, M

    initialize_match(2)

    while True:
        initialize_game(2)
        while True:
            if GAMEEND:
                break
            if not(PLY2):
                continue
            message2_r = ""
            message2_r = PLAYER2.recv(1024).decode("UTF-8")
            # print("server2", message2_r)

            if message2_r == "":
                print("Disconnected...")
                PLAYER2 = None
                break
            else:
                try:
                    message2_r = int(message2_r)
                    message2 = read_message(message2_r)
                    if message2[0] == 55:
                        M = int2tuple(message2[1])
                    elif message2[0] == 56:
                        pass
                    elif message2[0] == 57:
                        pass
                    else:
                        raise ValueError
                except:                    
                    import traceback
                    traceback.print_exc()
                    print("Error occurred!")
                    SERVER.close()
                    break

            PLY2 = False

        if MATCHEND:
            break

        terminate_game(2)
    
    terminate_match(2)


def read_message(abcdefgh):
    array = []
    ab = abcdefgh // 1000000
    cdefgh = abcdefgh % 1000000
    cd = cdefgh // 10000
    array.extend([ab, cd])
    return array


def write_message(array):
    message = str(array[0])
    if array[0] == 41 or array[0] == 42:
        message += str(array[1]) + format(array[2], '02d') + format(array[3], '02d') + "0"
    elif array[0] == 51 or array[0] == 52 or array[0] == 53 or array[0] == 54:
        message += str(array[1]) + "0000"
    return message


def initialize_match(n):
    global HOST, PORT, SERVER, SOCKET_OF_PLAYER
    global REFEREE, PLAYER1, PLAYER2, REF, PLY1, PLY2
    global COLOR_OF_PLAYER, PLAYER_OF_COLOR
    global MATCHSTART, MATCHEND, GAMESTART, GAMEEND
    global R, RESULT, TIME
    global B, C, M

    # referee
    if n == 0:
        HOST = "localhost"
        PORT = int(sys.argv[1])
        SERVER = socket.socket()
        SERVER.bind((HOST, PORT))
        SERVER.listen()

        REFEREE = "referee" # This variable has no meaning
        (RESULT["player1"], RESULT["player2"], RESULT["none"]) = (0, 0, 0)

        (MATCHSTART, MATCHEND) = (True, False)

    # player1
    elif n == 1:
        while not MATCHSTART:
            time.sleep(1)
            print("SERVER is None")
        PLAYER1, _ = SERVER.accept()
        SOCKET_OF_PLAYER["player1"] = PLAYER1

    # player2:
    elif n == 2:
        while not MATCHSTART:
            time.sleep(1)
            print("SERVER is None")
        PLAYER2, _ = SERVER.accept()
        SOCKET_OF_PLAYER["player2"] = PLAYER2
        print("PLAYER2 is here")

    while (REFEREE is None) or (PLAYER1 is None) or (PLAYER2 is None):
        time.sleep(1)
        if REFEREE is None:
            print("REFEREE is None")
        if PLAYER1 is None:
            print("PLAYER1 is None")
        if PLAYER2 is None:
            print("PLAYER2 is None")


def initialize_game(n):
    global HOST, PORT, SERVER, SOCKET_OF_PLAYER
    global REFEREE, PLAYER1, PLAYER2, REF, PLY1, PLY2
    global COLOR_OF_PLAYER, PLAYER_OF_COLOR
    global MATCHSTART, MATCHEND, GAMESTART, GAMEEND
    global R, RESULT, TIME
    global B, C, M

    # referee
    if n == 0:
        print("initialize game!")
        R = random.choice([True, False])
        PLAYER_OF_COLOR["black"] = "player1" if R else "player2"
        PLAYER_OF_COLOR["white"] = "player2" if R else "player1"
        COLOR_OF_PLAYER["player1"] = "black" if R else "white"
        COLOR_OF_PLAYER["player2"] = "white" if R else "black"

        (REF, PLY1, PLY2) = (False, False, False)
        (GAMESTART, GAMEEND) = (True, False)
        (TIME["player1"], TIME["player2"]) = (TIMELIMIT["player1"], TIMELIMIT["player2"])
        B = Board()
        C = B.color
        M = (0, 0)
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

main()
    
