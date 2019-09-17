# general purpose

NONE = 0
WHITE = 1
BLACK = 2
SENTINEL = 3

NONE_STONE = ' '
WHITE_STONE = 'o'
BLACK_STONE = 'x'

DIRECTIONS = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
CELLS = [(i,j) for i in range(1,9) for j in range(1,9)]

# protocol
# TODO: hoge
