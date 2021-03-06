"""
    v1 - add printing function
"""

from random import shuffle

# dims
X = 10   # columns
Y = 10   # rows

"""
coords expressed as "(row, col)" ... so "(y,x)"

(0,0)   (0,1)   (0,2)
(1,0)   (1,1)   (1,2)
(2,0)   (2,1)   (2,2)

i don't like this way
(0,0)   (1,0)   (2,0)
(0,1)   (1,1)   (2,1)
(0,2)   (1,2)   (2,2)
"""

WALLS = []
PATH = []
OOTO = []
#LAST_SQUARE = None
#EXIT_POINT = None
maze_coords = [(row, col) for row in range(Y) for col in range(X)]

def isOOB(p):
    x, y = p
    if x < 0 or x == X or y < 0 or y == Y:
        return 1


def new_coords(p, dir):
    x, y = p
    if dir == 'N':
        y -= 1
    elif dir == 'S':
        y += 1
    elif dir == 'E':
        x += 1
    else:
        x -= 1
    return x, y


def isWall(p):
    if p in WALLS:
        return 1


def inPath(p):
    if p in PATH:
        return 1

def get_OOTO_pairs(p, dir):
    x, y = p
    if dir == "N":
        x11 = x - 1
        y11 = y
        x12 = x - 1
        y12 = y - 1
        x21 = x + 1
        y21 = y
        x22 = x + 1
        y22 = y - 1

    elif dir == "S":
        x11 = x - 1
        y11 = y - 1
        x12 = x - 1
        y12 = y
        x21 = x + 1
        y21 = y - 1
        x22 = x + 1
        y22 = y

    elif dir == "E":
        x11 = x - 1
        y11 = y - 1
        x12 = x
        y12 = y - 1
        x21 = x - 1
        y21 = y + 1
        x22 = x
        y22 = y + 1

    else:
        x11 = x
        y11 = y - 1
        x12 = x - 1
        y12 = y - 1
        x21 = x
        y21 = y + 1
        x22 = x - 1
        y22 = y + 1

    p11 = (x11, y11)
    p12 = (x12, y12)
    p21 = (x21, y21)
    p22 = (x22, y22)
    l = [(p11, p12), (p21, p22)]
    return l


#END = (7,7)
def isEnd(p):
    x, y = p
    # if on last col and at least halfway down to last row, or vice versa
    # This should be ok if always starting in upper lh corner
    if (x == X-1 and y >= (Y-1)/2) or (x >= (X-1)/2 and y == Y-1):
        return 1

def advance(p):
    PATH.append(p)
    if isEnd(p):
        print ('Done with maze')
        #LAST_SQUARE = p
        #return 1
        return p

    # choose one of the four dirs in random order
    dirs = ['N', 'S', 'E', 'W']
    shuffle(dirs)

    for dir in dirs:
        next_position = new_coords(p, dir)
        if not isOOB(next_position) and not isWall(next_position) and not inPath(next_position):
            walls_ADD = []
            ooto_REMOVE = []

            # if you move into one of a pair, the other has to become a wall
            for pair in OOTO:
                for coord in pair:
                    if next_position == coord:
                        ooto_REMOVE.append(pair)        # Save for rollback
                        walls_ADD.append(coord)         # Save for rollback

            # reversible state update #1
            for pair in ooto_REMOVE:
                idx = OOTO.index(pair)
                del OOTO[idx]
            for coord in walls_ADD:
                WALLS.append(coord)


            ooto_NEW_list = get_OOTO_pairs(next_position, dir)  # this will have two pairs
            ooto_ADD = []   # these are the ones confirmed to be added

            for pair in ooto_NEW_list:
                if pair not in OOTO:        # if pair is already in the list don't add it
                    p1, p2, = pair
                    if not isOOB(p1):                               # if one is OOB, the other is too... don't add the pair
                        if not p1 in WALLS and not p2 in WALLS:     # if one is already a wall, don't add the pair
                            if not p1 in PATH and not p2 in PATH:   # if one is already in path, don't add the pair
                                ooto_ADD.append((p1,p2))

            # reversible state update #2
            for pair in ooto_ADD:
                OOTO.append(pair)
                # not adding walls at this point
                # (you have to "moved in" to a OOTO pair for walls to be added)

            # if advance(next_position):
            #     return 1
            # lastsquare = advance(next_position)
            # if lastsquare:
            #     return lastsquare
            if lastsquare := advance(next_position):
                return lastsquare

            # if didn't advance, rollback
            for pair in ooto_REMOVE:
                OOTO.append(pair)
            for coord in walls_ADD:
                idx = WALLS.index(coord)
                del WALLS[idx]
            for pair in ooto_ADD:
                idx = OOTO.index(pair)
                del OOTO[idx]

    # tried all 4 directions and was blocked, rolling back path
    idx = PATH.index(p)
    del PATH[idx]

################

def get_maze(path, path_char='.', wall_char='#'):
    """
        This returns a dictionary with the maze
        It has the path chars marked and everything else a wall
        It does not have borders or spacers
    """
    d = {}

    for coord in maze_coords:
            d.update({coord: wall_char})

    for coord in path:
        d.update({coord: path_char})

    return d


def print_maze(maze, border=False, b_char='#', spacer=False):
    """
        Border and spacer are both optional
        b_char: the border/wall char (default: "#")
        spacer: whether to separate columns with space for readability
        Usage:
            print_maze(maze)                        # no border or spacer
            print_maze(maze, True)                  # with border
            print_maze(maze, True, "??????")            # with border, specify border char
            print_maze(maze, True, spacer=True)     # with border and spacer
            print_maze(maze, True, "??????", True)      # with border and spacer, specifying border char
            print_maze(maze, spacer=True)           # with spacer, no border
    """
    sp_char = ''
    if spacer:
        sp_char = ' '

    if not border:
        b_char = ''

    if border:
        print((b_char + sp_char) * (X + 2))

    for row in range(Y):
        print(b_char + sp_char, end='')
        for col in range(X):
            print(maze[(col, row)] + sp_char, end="")
        print(b_char)

    if border:
        print((b_char + sp_char) * (X + 2))

    print()


def get_border_maze(path, path_char='.', wall_char='#', entry_point=None, exit_point=None, entry_char='S', exit_char='E'):
    """
        This version adds the borders to the dictionary
        This facilitates marking entry and exit points, which need to be addressed but are outside the maze's boundaries
    """

    # get the base maze with no borders or spacers
    maze = get_maze(path, path_char, wall_char)

    # for every row (incl row=-1 and row=y), add col=-1 and col=x
    for row in range(-1, Y + 1):
        maze.update({(row, -1): wall_char})
        maze.update({(row, X): wall_char})

    # for every col (not incl col=-1 and col=x), add row=-1 and row=y
    for col in range(X):
        maze.update({(-1, col): wall_char})
        maze.update({(Y, col): wall_char})

    if entry_point:
        maze.update({entry_point: entry_char})
    if exit_point:
        maze.update({exit_point: exit_char})

    return maze

def print_border_maze(maze, spacer=False):
    """
        Print the maze that already has borders added
        spacer: whether to separate columns with space for readability
    """
    sp = ''
    if spacer:
        sp = ' '

    for row in range(-1, Y + 1):
        for col in range(-1, X + 1):
            print(maze[(col, row)] + sp, end="")
        print()
    print()


def main():
    START = (0,0)
    last_square = advance(START)
    if last_square:
        print ("successfully finished creating the maze, part 1")
    else:
        print ("exhausted all possibilities and was unable to complete the maze")

    print ("Path:")
    print (PATH)

    if last_square:
        print (f'{last_square=}')
        # it's giving it as (col, row), so for now reverse it
        #y,x = last_square
        x,y = last_square
        if x == X-1:
            EXIT_POINT = (x+1, y)
            #EXIT_POINT = (x, y+1)
        #elif y == Y-1:
        else:
            EXIT_POINT = (x, y+1)
            #EXIT_POINT = (x+1, y)
        # else:
        #     EXIT_POINT = (x, y)
        #     print ('it was neither x==X-1 or y==Y-1')
        #     print (f'{X=}')
        #     print (f'{Y=}')

    else:
        print ('there was no last square')

    print (f'{EXIT_POINT=}')
    border_maze = get_border_maze(PATH, entry_point=(-1, 0), exit_point=EXIT_POINT)
    print_border_maze(border_maze)
    print_border_maze(border_maze, spacer=True)

    # border_maze = get_border_maze(PATH)
    # print_border_maze(border_maze)
    # print_border_maze(border_maze, spacer=True)

    # maze = get_maze(PATH)
    # print_maze(maze, True, spacer=True)

if __name__ == '__main__':
    main()


