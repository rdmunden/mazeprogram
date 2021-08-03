"""
    v6  - it occasionally (1 out of 10 times) partitions the maze and gets squirreled away on the wrong side of the partition
        - when that happens it can take a very long time to work it's way back out and into the other side of the partition
        - so i'm going to have it keep defining the maze even on paths that do no lead to the exit
        - this'll keep it from iterating so long over the wrong partition bc it will cut back on the amount of combinations of paths available
        - only thing i'm worried about is lead to making a "tunnel" thru the maze, where the solution path is not reachable by anything outside the "tunnel"
        - or, anywhere in the tunnel can't get outside the tunnel
        - this would have especially been possible if i had created the add'l blocks outlined below, whcih i haven't yet

        UPDATE:
        - turns out keeping the extra walls didn't solve the problem
        - it needed me to actually block those failed paths
        - which i didn't want to do bc presumably you could have visited those cells from a different state (of walls) and still found the end
        - now the question is whether or not to keep the extra walls after all
        - for now i've decided not to keep them, but it can be easily added in the future for side by side comparison
        - new global var BLOCKED_PATHS to paths that lead to dead ends
        - I will have to decide what to do with those later, you can't just blanket make them all walls.

        TODO:
        - These are the additional blocks, meant to make sure there are no closed loops in the solution path
        - bc this would make it possible for the solution to be short circuited and possibly greatly shortened
        - it's already not possible for the maze creation to loop upon itself
        - however it is allowed to create new paths that are adjacent to prev paths (even if it is not allowed to take them)
        -
        - if next position links to path, block it... instead of going there put a wall there
            1. if going again fr next position in the same dir would hit solution path, make next position a wall
            2. if turning rt or l fr next position would hit a wall, make next position a wall

        - if advance into an ooto pair and have to make the other a wall, but the other is already in path...
            ... must be blocked, make next position a wall

        - if advance is not into an ooto pair BUT one of it's ... ?
"""

from random import shuffle
LVL = 0
path_tried = []
repeat_attempts = 0
BLOCKED_PATHS = []

# dims
X = 20   # columns
Y = 20   # rows

"""
"""

WALLS = []
PATH = []
OOTO = []
#LAST_SQUARE = None
#EXIT_POINT = None
maze_coords = [(row, col) for row in range(Y) for col in range(X)]

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

def get_OOTO_pairs(p, dir):
    y, x = p
    if dir == "N":
        y11 = y
        x11 = x - 1
        #y12 = y - 1
        y12 = y + 1
        x12 = x - 1
        y21 = y
        x21 = x + 1
        #y22 = y - 1
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
        #x22 = x - 1
        x22 = x + 1

    p11 = (y11, x11)
    p12 = (y12, x12)
    p21 = (y21, x21)
    p22 = (y22, x22)
    # l = [(p11, p12), (p21, p22)]
    # return l
    return [(p11, p12), (p21, p22)]

#END = (7,7)
def isEnd(p):
    y, x = p
    # if on last col and at least halfway down to last row, or vice versa
    # This should be ok if always starting in upper lh corner
    if (y == Y-1 and x >= (X-1)/2) or (y >= (Y-1)/2 and x == X-1):
        return 1

def advance(current_position):
    global LVL
    global repeat_attempts
    LVL += 1
    PATH.append(current_position)
    if isEnd(current_position):
        print ('Done with maze')
        #LAST_SQUARE = current_position
        #return 1
        return current_position

    # choose one of the four dirs in random order
    dirs = ['N', 'S', 'E', 'W']
    shuffle(dirs)

    for dir in dirs:
        next_position = new_coords(current_position, dir)
        pass
        # print (f'{PATH=}')
        # print (f'{dir=}')
        # print (f'{next_position=}')

        if not isOOB(next_position) and not isWall(next_position) and not inPath(next_position) and next_position not in BLOCKED_PATHS:
            walls_ADD = []
            ooto_REMOVE = []

            # if you move into one of a pair, the other has to become a wall
            for pair in OOTO:
                # for coord in pair:
                #     if next_position == coord:
                #         ooto_REMOVE.append(pair)        # Save for rollback
                #         walls_ADD.append(coord)         # Save for rollback
                coord1, coord2 = pair
                if next_position == coord1:
                    ooto_REMOVE.append(pair)  # Save for rollback
                    walls_ADD.append(coord2)  # Save for rollback
                elif next_position == coord2:
                    ooto_REMOVE.append(pair)  # Save for rollback
                    walls_ADD.append(coord1)  # Save for rollback

            # reversible state update #1
            for pair in ooto_REMOVE:
                idx = OOTO.index(pair)
                del OOTO[idx]
            for coord in walls_ADD:
                WALLS.append(coord)


            ooto_NEW_list = get_OOTO_pairs(next_position, dir)  # this will have two pairs
                # shouldn't add if ...
                #   ... one is a wall   <-- think i can just do this
                #   ... one is a path   <-- the other       .... *** don't add if in ooto_REMOVE ... or add first then remove
                #   ... one is a wall and the other a path
                #           ... both are paths ... that can't/mustn't be
                #           ... both are walls, that could be i think...
            ooto_ADD = []   # these are the ones confirmed to be added

            for pair in ooto_NEW_list:                          # *** don't add if one is a wall
                if pair not in OOTO:        # if pair is already in the list don't add it
                    p1, p2, = pair
                    if not isOOB(p1):                               # if one is OOB, the other is too... don't add the pair
                        if not p1 in WALLS and not p2 in WALLS:     # if one is already a wall, don't add the pair ❗make this 'or'?
                            if not p1 in PATH and not p2 in PATH:   # if one is already in path, don't add the pair
                                # ooto_ADD.append((p1,p2))
                                ooto_ADD.append(pair)

            # reversible state update #2
            for pair in ooto_ADD:
                OOTO.append(pair)
                # not adding walls at this point
                # (you have to have "moved in" to one of a OOTO pair for walls to be added)

            # if advance(next_position):
            #     return 1
            # lastsquare = advance(next_position)
            # if lastsquare:
            #     return lastsquare
            if lastsquare := advance(next_position):
                return lastsquare

            #print ("didn't find it this dir")
            # if didn't advance, rollback
            # (following that square did not lead to the end)
            #❗ v6 - not going to undo the maze changes just bc this path doesn't lead to the exit
            #❗ update again, going back to rolling back these changes bc it didn't solve the problem by not doing it
            for pair in ooto_REMOVE:
                OOTO.append(pair)
            for coord in walls_ADD:
                idx = WALLS.index(coord)
                del WALLS[idx]
            for pair in ooto_ADD:
                idx = OOTO.index(pair)
                del OOTO[idx]

    # tried all 4 directions and was blocked, rolling back path
    if PATH in path_tried:
        print ("path already tried")
        repeat_attempts += 1
        print (repeat_attempts)
        pass
    else:
        path_tried.append(PATH.copy())
        #print ('appended:')
        print (f'{len(path_tried)}\r')

    idx = PATH.index(current_position)
    blocked = PATH[idx]
    del PATH[idx]
    if blocked not in BLOCKED_PATHS:
        BLOCKED_PATHS.append(blocked)
    LVL -= 1
    #print (f"didn't advance, level = {LVL}")

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

def get_maze_with_walls(path, path_char='.', wall_char='#'):
    """
        First mark all coords as a blank with "O"
        Then mark path
        Then mark walls
    """
    d = {}

    for coord in maze_coords:
            d.update({coord: "▓"})

    for coord in path:
        d.update({coord: path_char})

    for coord in WALLS:
        d.update({coord: wall_char})

    return d


def get_maze_with_walls_and_blocked(path, path_char='.', wall_char='#'):
    """
        First mark all coords as a blank with "O"
        Then mark path
        Then mark walls
        Then mark blocked paths
    """
    d = {}

    for coord in maze_coords:
            d.update({coord: "▓"})

    for coord in path:
        d.update({coord: path_char})

    for coord in WALLS:
        d.update({coord: wall_char})

    for coord in BLOCKED_PATHS:
        d.update({coord: "@"})

    return d

def print_maze(maze, border=False, b_char='#', spacer=False):
    """
        Border and spacer are both optional
        b_char: the border/wall char (default: "#")
        spacer: whether to separate columns with space for readability
        Usage:
            print_maze(maze)                        # no border or spacer
            print_maze(maze, True)                  # with border
            print_maze(maze, True, "▓▓")            # with border, specify border char
            print_maze(maze, True, spacer=True)     # with border and spacer
            print_maze(maze, True, "▓▓", True)      # with border and spacer, specifying border char
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

#abstract out 'get_maze' from 'get_border_maze' so i can use different versions of 'get_maze'
# ... instead of adding another arg to 'get_border_maze'
# ... now to get the final maze you will have to do the two steps separately
# ... 'get_border_maze' should be 'add_maze_border'
def get_border_maze(maze, path_char='.', wall_char='#', entry_point=None, exit_point=None, entry_char='S', exit_char='E'):
    """
        This version adds the borders to the dictionary
        This facilitates marking entry and exit points, which need to be addressed but are outside the maze's boundaries
    """

    # get the base maze with no borders or spacers
    #maze = get_maze(path, path_char, wall_char)
    #maze = get_maze(path)

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
            #print(maze[(col, row)] + sp, end="")
            print(maze[(row, col)] + sp, end="")
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
    print (f"Blocked: {len(BLOCKED_PATHS)}")

    if last_square:
        print (f'{last_square=}')
        # it's giving it as (col, row), so for now reverse it
        y,x = last_square
        #x,y = last_square
        if x == X-1:
            EXIT_POINT = (y, x+1)
            #EXIT_POINT = (x, y+1)
        #elif y == Y-1:
        else:
            EXIT_POINT = (y+1, x)
            #EXIT_POINT = (x+1, y)
        # else:
        #     EXIT_POINT = (x, y)
        #     print ('it was neither x==X-1 or y==Y-1')
        #     print (f'{X=}')
        #     print (f'{Y=}')

    else:
        print ('there was no last square')

    print (f'{EXIT_POINT=}')

    # maze = get_maze(PATH)
    # border_maze = get_border_maze(maze, entry_point=(0, -1), exit_point=EXIT_POINT)
    # print_border_maze(border_maze)
    # print_border_maze(border_maze, spacer=True)

    # border_maze = get_border_maze(PATH)
    # print_border_maze(border_maze)
    # print_border_maze(border_maze, spacer=True)

    # maze = get_maze(PATH)
    # print_maze(maze, True, spacer=True)

    maze = get_maze_with_walls(PATH)
    border_maze = get_border_maze(maze, entry_point=(0, -1), exit_point=EXIT_POINT)
    #print_border_maze(border_maze)
    print_border_maze(border_maze, spacer=True)

    maze = get_maze_with_walls_and_blocked(PATH)
    border_maze = get_border_maze(maze, entry_point=(0, -1), exit_point=EXIT_POINT)
    print_border_maze(border_maze, spacer=True)


if __name__ == '__main__':
    main()


