"""
    maze creation - version 0

A. creation algorithm
    1. No contiguous block of 4 cells can all be open paths
    2. iow, this is not allowed:
        . .
        . .
    3. Any time that can occur, a wall must be placed in the block, resulting in one of these 4 possibilities:
        # .     . #     . .     . .
        . .     . .     # .     . #
    4. When maze creator moves from cell A to B, that creates two blocks, one to either side of the direction of movement.
        p11   B   p21
        p12   A   p22
    5. The two coordinates on either side are a "matched pair".  If the maze creator moves into one of the pair the other
        must become a wall.

B. maze coordinates
    1. Coordinates are specified with option base 0.
    2. Coordinates are given in "row major" notation.
    3. "x" designates columns, incrementing from left to right.
    4. "y" designates rows, incrementing from top to bottom.

    An example 3x3 grid:
        - coordinates expressed as "(row, col)" ... or "(y,x)"
            (0,0)   (0,1)   (0,2)
            (1,0)   (1,1)   (1,2)
            (2,0)   (2,1)   (2,2)

"""
from random import shuffle

# dims
X = 8   # columns
Y = 8   # rows

"""
col, row
x, y
upper lh - bottom rh
"""

PATH = []
WALLS = []
MATCHED_PAIRS = []


def isOOB(p):
    y, x = p
    if x < 0 or x == X or y < 0 or y == Y:
        return 1


def new_coords(p, dir):
    y, x = p
    if dir == 'N':
        y -= 1
    elif dir == 'S':
        y += 1
    elif dir == 'E':
        x += 1
    else:
        x -= 1
    return y, x


def isWall(p):
    if p in WALLS:
        return 1


def inPath(p):
    if p in PATH:
        return 1

def get_Matched_Pairs(p, dir):
    y, x = p
    if dir == "N":
        y11 = y
        x11 = x - 1
        y12 = y + 1
        x12 = x - 1
        y21 = y
        x21 = x + 1
        y22 = y + 1
        x22 = x + 1

    elif dir == "S":
        y11 = y - 1
        x11 = x - 1
        y12 = y
        x12 = x - 1
        y21 = y - 1
        x21 = x + 1
        y22 = y
        x22 = x + 1

    elif dir == "E":
        y11 = y - 1
        x11 = x - 1
        y12 = y - 1
        x12 = x
        y21 = y + 1
        x21 = x - 1
        y22 = y + 1
        x22 = x

    else:
        y11 = y - 1
        x11 = x
        y12 = y - 1
        #x12 = x - 1
        x12 = x + 1
        y21 = y + 1
        x21 = x
        y22 = y + 1
        x22 = x + 1

    p11 = (y11, x11)
    p12 = (y12, x12)
    p21 = (y21, x21)
    p22 = (y22, x22)

    return [(p11, p12), (p21, p22)]

#END = (7,7)
def isEnd(p):
    y, x = p
    # if on last col and at least halfway down to last row, or vice versa
    # This should be ok if always starting in upper lh corner
    if (y == Y-1 and x >= (X-1)/2) or (y >= (Y-1)/2 and x == X-1):
        return 1

def advance(p):
    PATH.append(p)
    if isEnd(p):
        print ('Done with maze')
        return 1

    # choose one of the four dirs in random order
    dirs = ['N', 'S', 'E', 'W']
    shuffle(dirs)

    for dir in dirs:
        next_position = new_coords(p, dir)
        if not isOOB(next_position) and not isWall(next_position) and not inPath(next_position):
            walls_ADD = []
            mp_REMOVE = []

            # if you move into one of a pair, the other has to become a wall
            for pair in MATCHED_PAIRS:
                for coord in pair:
                    if next_position == coord:
                        mp_REMOVE.append(pair)        # Save for rollback
                        walls_ADD.append(coord)         # Save for rollback

            # reversible state update #1
            for pair in mp_REMOVE:
                idx = MATCHED_PAIRS.index(pair)
                del MATCHED_PAIRS[idx]
            for coord in walls_ADD:
                WALLS.append(coord)


            mp_NEW_list = get_Matched_Pairs(next_position, dir)  # this will have two pairs
            mp_ADD = []   # these are the ones confirmed to be added

            for pair in mp_NEW_list:
                if pair not in MATCHED_PAIRS:        # if pair is already in the list don't add it
                    p1, p2, = pair
                    if not isOOB(p1):                               # if one is OOB, the other is too... don't add the pair
                        if not p1 in WALLS and not p2 in WALLS:     # if one is already a wall, don't add the pair
                            if not p1 in PATH and not p2 in PATH:   # if one is already in path, don't add the pair
                                mp_ADD.append((p1,p2))

            # reversible state update #2
            for pair in mp_ADD:
                MATCHED_PAIRS.append(pair)
                # not adding walls at this point
                # (you have to "moved in" to a OOTO pair for walls to be added)

            if advance(next_position):
                return 1

            # if didn't advance, rollback
            for pair in mp_REMOVE:
                MATCHED_PAIRS.append(pair)
            for coord in walls_ADD:
                idx = WALLS.index(coord)
                del WALLS[idx]
            for pair in mp_ADD:
                idx = MATCHED_PAIRS.index(pair)
                del MATCHED_PAIRS[idx]

    # tried all 4 directions and was blocked, rolling back path
    idx = PATH.index(p)
    del PATH[idx]


START = (0,0)
if advance(START):
    print ("successfully finished creating the maze, part 1")
else:
    print ("exhausted all possibilities and was unable to complete the maze")

print ("Path")
print (PATH)





