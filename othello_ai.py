from othello_board import *
from othello_ai_editable import *

def random_choice(board):
    moves = valid_moves(board.board, board.color)
    return random.choice(moves)


def choose_move(moves):
    l = len(moves)
    while True:
        i = input()
        j = re.sub(r'\d+', '', i)
        if len(j) == 0:
            k = int(i) - 1
            if k in range(l):
                return moves[k]


def person_choice(board):
    moves = valid_moves(board.board, board.color)
    print_moves(moves)
    move = choose_move(moves)
    return move


# FIXME: minmaxになるように符号を考える
def _minmax(_board, _color, _init_color, _depth, _evalfun):
    if _depth == 1:
        return _evalfun(_board, _color)
    else:
        _moves = valid_moves(_board, _color)
        if _moves == []:
            if _init_color == _color:
                return 100
            else:
                return -100
        else:
            _evals = []
            for _m in _moves:
                _b = Board(_board, _color, _init_color)
                _b.move(_m)
                _evals.append(_minmax(_b.board, _b.color, _init_color, _depth-1, _evalfun))
            return max(_evals)


def minmax(board, color, depth, evalfun):
    moves = valid_moves(board, color)
    evals = {}
    for m in moves:
        evals[m] = _minmax(board, color, color, depth, evalfun)
    return max(evals)


def random_playout():
    b = Board()
    n = 0
    print(valid_moves(b.board, b.color))
    while True:
        n += 1
        if n > 100:
            break
        if the_end(b.board, b.color):
            break
        else:
            m = random_choice(b)
            print(m)
            b.move(m)
            print(valid_moves(b.board, b.color))
            print()


# expand
# calc
# update
def _montecarlo(_board, _color, _thr, _iter):
    # select_leaf (by UCB1)
    pass


# def montecarlo(board, color, thr, iter):
#     moves = valid_moves(board, color)
#     evals = {}
#     for m in moves:
#         evals[m] = _montecarlo(board, color, color, depth, evalfun, thr, iter)
#     return max(evals)

AI = None
if "AI_EDITABLE" in globals():
    try:
        way = AI_EDITABLE
        if type(way) == str:
            AI = globals()[way]
    except:
        AI = random_choice