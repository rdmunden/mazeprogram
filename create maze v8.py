"""
    v8  - There are some refinements to be made to the maze creation algorithm:
        1. It has been determined that it's best not to roll back the walls created in blocked branches.
            - These blocked paths can be left as open paths for the maze solver to explore.
            - Because of this, all the "rollback" code can be eliminated.
        2. 'lookahead' walls need to be treated differently.
            - The result of making all these "lookahead" walls is many cases the creation of "tunnels" along the solution path,
                where a virtual "tunnel" of walls is created straight to the end.
            - iow there is no place left for the solver to turn off in the wrong direction.
            - Instead of making them actual walls, they will be made as invisible walls so as to not create these tunnels to
                the exit for the maze solver.
            - These invisible walls are not strictly needed by the maze creation algorithm because it is already prohibited from
                turning back upon itself
            - However these invisible walls will mark locations where real ("solidified") walls could possibly be, and in some cases,
                must be added.
            -
            - However in some cases the invisible walls will need to be made into solidified walls where appropriate per the building
                algorithm, just not all of them

        TODO:
        - To make a more efficient job of turning invisible walls into solid walls, the wall creation algorithm should be modified
        to work in a pro-active manner.
        - Instead of creating matched pairs that will be used later to create walls when they are stepped in to, they will be used
        to immediately create walls. In this way invisible walls can also be taken into consideration.  Also it will no longer be
        necessary for a running list of matched pairs to be kept

        TODO: invisible walls:
        1. in original creation, they will need to be checked to see if there are adjacent invis walls.
            - if there are, one of them needs to be made a solidifed wall
        2. later, another check will be done on invis walls
            - if they are in a 4 square block and the other 3 squares are solution path or blocked path, they must be solidified

        TODO: This is the start of part 2, where the rest of the unvisited cells are filled
        - will need to catalog all unvisited squares then attempt to exit when all squares have been visited or made a wall
        - will have to be careful not to overwrite any existing paths and walls
        - it probably won't be able to visit every cell or make it a wall
"""

from random import shuffle
LVL = 0
path_tried = []
repeat_attempts = 0

# dims
X = 20   # columns
Y = 20   # rows

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
BLOCKED_PATHS = []
INVISIBLE_WALLS = []
maze_coords = [(row, col) for row in range(Y) for col in range(X)]
unvisited = maze_coords.copy()

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
    if p in WALLS or p in INVISIBLE_WALLS:
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

def lookahead_block(p, dir):
    y, x = p
    if dir == 'N':
        forward_position = (y-1, x)
        left_position = (y, x-1)
        right_position = (y, x+1)
    elif dir == 'S':
        forward_position = (y+1, x)
        left_position = (y, x+1)
        right_position = (y, x-1)
    elif dir == 'E':
        forward_position = (y, x+1)
        left_position = (y-1, x)
        right_position = (y+1, x)
    else:
        forward_position = (y, x-1)
        left_position = (y+1, x)
        right_position = (y-1, x)

    if forward_position in PATH or left_position in PATH or right_position in PATH:
        if forward_position in PATH:
            print (f'forward position when going {dir} in path: {forward_position}')
        if left_position in PATH:
            print (f'left position when going {dir} in path: {left_position}')
        if right_position in PATH:
            print (f'right position when going {dir} in path: {right_position}')
        return 1


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

        if not isOOB(next_position) and not isWall(next_position) and not inPath(next_position) and next_position not in BLOCKED_PATHS:
            #if current_position != (0,0) and lookahead_block(next_position, dir):
            if lookahead_block(next_position, dir):
                #WALLS.append(next_position)    # Handle this in "isWall"
                INVISIBLE_WALLS.append(next_position)
                print (f'adding invisible wall at {next_position} due to lookahead block')
                #return

        # print (f'{PATH=}')
        # print (f'{dir=}')
        # print (f'{next_position=}')

        if not isOOB(next_position) and not isWall(next_position) and not inPath(next_position) and next_position not in BLOCKED_PATHS:
            walls_ADD = []
            ooto_REMOVE = []

            # if you move into one of a pair, the other has to become a wall
            # this should really only happen if you make a right turn immed
            # UPDATE v8: this code should not get ran anymore bc of the new procedure that proactively creates the walls
            # iow by the time the alogrithm steps into one of these matched pairs the wall that goes there should have already been created
            for pair in OOTO:
                # for coord in pair:
                #     if next_position == coord:
                #         ooto_REMOVE.append(pair)        # Save for rollback
                #         walls_ADD.append(coord)         # Save for rollback
                coord1, coord2 = pair
                if next_position == coord1:
                    ooto_REMOVE.append(pair)  # Save for rollback
                    if coord2 not in WALLS:                             # UPDATE: had to add this check, at time of creating a pair, neither was a wall, but that may have changed later, it could have been made into a wall on a blocked path - if we're not rolling back wall created in blocked paths
                        walls_ADD.append(coord2)  # Save for rollback
                elif next_position == coord2:
                    ooto_REMOVE.append(pair)  # Save for rollback
                    if coord1 not in WALLS:
                        walls_ADD.append(coord1)  # Save for rollback

            # reversible state update #1
            for pair in ooto_REMOVE:
                idx = OOTO.index(pair)
                del OOTO[idx]
            for coord in walls_ADD:
                WALLS.append(coord)


            # Now that you've moved from one square to the other, that makes two OOTO pairs, one on either side of the path you just traced
            # this should really only be useful if you immed make a 90° turn
            # if you didn't then immed turn into that pair then you never should enter it
            # any other time you approach that pair later it should be handled by lookahead
            ooto_NEW_list = get_OOTO_pairs(next_position, dir)  # this will have two pairs
                # shouldn't add if ...
                #   ... one is a wall   <-- think i can just do this
                #   ... one is a path   <-- the other       .... *** don't add if in ooto_REMOVE ... or add first then remove
                #   ... one is a wall and the other a path
                #           ... both are paths ... that can't/mustn't be
                #           ... both are walls, that could be i think...
            ooto_ADD = []   # these are the ones confirmed to be added

            #    c
            # a1 ^ a2
            # b1 | b2
            #
            # if a1 or a2 is a path (and c too for that matter) it shouldn't even let you enter here bc of lookahead
            # i.e. it should make an "invisible wall" here insted of letting you go here
            # if b1 or b2 is a path, the corresponding a should be made a wall
            # if both a1 and b1 or a2 and b2 are invisible walls, at least one of them needs to be made a solid wall

            # TODO: Need to add the case where two paths pass each other one lane apart, so both have the same matched pair
            # in that case you may need to reverse the coords in one when comparing them bc they are recorded depending on the dir you were going
            # altho it's possible for them to pass the same spot going in the same direction, still one lane apart
            # i think that is being handled pretty well already tho with the lookahead feature
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
            #❗ but it may be desirable to keep these changes, as the will help to fill out the maze later
            #❗This is mystery feature "X" as i try to figure out what it is doing
            #   - sometimes it seems to do the opposite of what i expect
            #   - when it is turned on i expect to not get walls in the middle of blocked areas yet i do
            #   - and when it is turned off i expect to get walls in blocked areas and yet i do not
            # for pair in ooto_REMOVE:
            #     OOTO.append(pair)
            # for coord in walls_ADD:
            #     idx = WALLS.index(coord)
            #     del WALLS[idx]
            # for pair in ooto_ADD:
            #     idx = OOTO.index(pair)
            #     del OOTO[idx]

    # tried all 4 directions and was blocked, rolling back path
    if PATH in path_tried:
        print ("path already tried")
        repeat_attempts += 1
        print (f'{repeat_attempts=}')
        pass
    else:
        path_tried.append(PATH.copy())
        #print ('appended:')
        print (f'paths tried: {len(path_tried)}\r')

    idx = PATH.index(current_position)
    blocked = PATH[idx]
    del PATH[idx]
    if blocked not in BLOCKED_PATHS:
        BLOCKED_PATHS.append(blocked)
    LVL -= 1
    #print (f"didn't advance, level = {LVL}")

VISITED = []
OOTO2 = []      # Need a new container for these, these are not the same as the other time
def isVisited(p):
    if p in VISITED:
        return 1

# unvisited = maze_coords.copy()

################
def advance_fill(current_position):
    # v8 - don't use this yet, it was started but not fully developed and not used yet
    global LVL
    global repeat_attempts
    LVL += 1
    VISITED.append(current_position)

    # this is not going to be allowed to find the maze exit in order to cover as much of the maze as possible
    # if isEnd(current_position):
    #     print ('Done with maze')
    #     #LAST_SQUARE = current_position
    #     #return 1
    #     return current_position

    # choose one of the four dirs
    # we'll visit every direction but prefer paths that haven't been visited yet
    # put the unvisited positions to the front of the list, then append the rest after that
    dirs = ['N', 'S', 'E', 'W']
    preferred_dirs = []
    for i in dirs:
        if not isVisited(new_coords(current_position, i)):
            preferred_dirs.append(i)

    for i in dirs:
        if i not in preferred_dirs:
            preferred_dirs.append(i)

    dirs = preferred_dirs

    for dir in dirs:
        next_position = new_coords(current_position, dir)

        # Since this is the second round we'll not worry about the solution path
        # but still don't want to get go in loops
        # also not worrying about blocked paths (for now)
        # we'll have to block paths again to reduce combinations to try, but this time we will convert them to open pathways afterwards
        # it's not possible to do something either one way or the other with the previous blocked paths as they are
        # for many it would be desirable to convert them to open pathways after, but not always so you can't do so uniformly
        # some of them need to be converted to walls, and in clusters of them we need to have some be pathways and some be walls
        # whenever you have a blocked pathway, there is only one entrance to it
        # -- not true, if it enters a new blocked area, and then travels along its own border, there can be multiple entrances
        # -- and they will be adjacent to one another
        # -- there can also be unvisited blocks adjacent to blocked areas, so those can become add'l entrances to the blocked area
        # you need to need to visit that entrance, but then you need to go thru the entire blocked section to make walls
        if not isOOB(next_position) and not isWall(next_position) and not isVisited(next_position): # and next_position not in BLOCKED_PATHS:
            if lookahead_block(next_position, dir):
                WALLS.append(next_position)
                print (f'adding wall at {next_position}')
                #return

        # print (f'{PATH=}')
        # print (f'{dir=}')
        # print (f'{next_position=}')

        if not isOOB(next_position) and not isWall(next_position) and not inPath(next_position) and next_position not in BLOCKED_PATHS:
            walls_ADD = []
            ooto_REMOVE = []

            # if you move into one of a pair, the other has to become a wall
            for pair in OOTO2:
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
            #❗ but it may be desirable to keep these changes, as the will help to fill out the maze later
            # ❕❕ This is the second time ❕❕
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
        It has already been checked that there are no collisions between path and walls and blocked
        That leaves all the rest to be unvisited
        First mark all coords with the "unvisited" char
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
        d.update({coord: "░"})

    return d

def get_maze_with_walls_and_blocked_plus_lookahead(path, path_char='.', wall_char='#'):
    """
        This will include lookahead walls, which are also walls
        so these have to be overlaid after walls
        these should not be in blocked paths but not checking bc walls are being checked
    """
    d = {}

    for coord in maze_coords:
        d.update({coord: "▓"})

    for coord in path:
        d.update({coord: path_char})

    for coord in WALLS:
        d.update({coord: wall_char})

    for coord in BLOCKED_PATHS:
        d.update({coord: "░"})

    for coord in INVISIBLE_WALLS:
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
    # ---------- defining the maze ----------
    START = (0,0)
    last_square = advance(START)
    if last_square:
        print ("successfully finished creating the maze, part 1")
    else:
        print ("exhausted all possibilities and was unable to complete the maze")

    print ("Path:")
    print (PATH)
    print ("Walls:")
    print (WALLS)
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
        EXIT_POINT = (Y,X)

    print (f'{EXIT_POINT=}')

    # ---------- filling in the rest of the maze ----------
    # will check for duplicates and collisions
    # each set should be unique and mutually exclusive
    problems_found = 0
    path_set = set(PATH)
    walls_set = set(WALLS)
    blocked_set = set(BLOCKED_PATHS)
    if len(PATH) != len(path_set):
        print ('Duplicate in solution path')
        problems_found = 1
    if len(WALLS) != len(walls_set):
        print ('Duplicate in walls')
        problems_found = 1
    if len(BLOCKED_PATHS) != len(blocked_set):
        print ('Duplicate in blocked paths')
        problems_found = 1

    if path_set.intersection(walls_set):
        print ('collision found in solution path and walls')
        problems_found = 1
    if path_set.intersection(blocked_set):
        print ('collision found in solution path and blocked paths')
        problems_found = 1
    if walls_set.intersection(blocked_set):
        print ('collision found in walls and blocked paths')
        problems_found = 1

    if problems_found:
        return

    for i in PATH:
        idx = unvisited.index(i)
        del unvisited[idx]
    for i in WALLS:
        idx = unvisited.index(i)
        del unvisited[idx]

    # ---------- printing results ----------
    # maze = get_maze(PATH)
    # border_maze = get_border_maze(maze, entry_point=(0, -1), exit_point=EXIT_POINT)
    # print_border_maze(border_maze)
    # print_border_maze(border_maze, spacer=True)

    # border_maze = get_border_maze(PATH)
    # print_border_maze(border_maze)
    # print_border_maze(border_maze, spacer=True)

    # maze = get_maze(PATH)
    # print_maze(maze, True, spacer=True)

    # maze = get_maze_with_walls(PATH)
    # border_maze = get_border_maze(maze, entry_point=(0, -1), exit_point=EXIT_POINT)
    # #print_border_maze(border_maze)
    # print_border_maze(border_maze, spacer=True)

    maze = get_maze_with_walls_and_blocked(PATH)
    border_maze = get_border_maze(maze, entry_point=(0, -1), exit_point=EXIT_POINT)
    print_border_maze(border_maze, spacer=True)

    maze = get_maze_with_walls_and_blocked_plus_lookahead(PATH)
    border_maze = get_border_maze(maze, entry_point=(0, -1), exit_point=EXIT_POINT)
    print_border_maze(border_maze, spacer=True)
    # ---------- printing, part 2 ----------

    # maze = get_maze_with_walls_and_unvisited(PATH)
    # border_maze = get_border_maze(maze, entry_point=(0, -1), exit_point=EXIT_POINT)
    # print_border_maze(border_maze, spacer=True)

if __name__ == '__main__':
    main()
    print(__file__)

