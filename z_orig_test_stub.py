""" This is the orig module of printing functions.  It has 3 globals defined here to make it work on its own """
""" Update: copied fr current version... the next 4 lines are added to define globals to make this work as a stub """

X = 20       # cols 0 - 5
Y = 20       # rows 0 - 5
maze_coords = [(row, col) for row in range(Y) for col in range(X)]
#WALLS = [(0, 1), (2, 0), (6, 2), (5, 4), (5, 5), (6, 7), (6, 8), (7, 12), (6, 16), (4, 15), (4, 17), (2, 18), (1, 18), (0, 16), (1, 14), (0, 12), (1, 10), (1, 4), (1, 6), (3, 5), (4, 2), (3, 7), (4, 7), (5, 14), (6, 10), (3, 9), (2, 11), (4, 10), (3, 12), (4, 14)]
#WALLS = [(0, 1), (2, 0), (6, 2), (5, 4), (5, 5), (6, 7), (6, 8), (7, 12), (6, 16), (4, 15), (4, 17), (2, 18), (2, 17), (1, 15), (2, 14), (0, 13), (1, 11), (1, 10), (0, 8), (2, 9), (2, 12), (5, 14), (6, 10), (1, 7), (3, 8), (2, 6), (4, 2)]
# WALLS = [(1, 0), (0, 2), (2, 1), (4, 2), (3, 4), (5, 7), (4, 9), (6, 8), (5, 10), (7, 9), (6, 11), (6, 12), (6, 14), (2, 18), (0, 14), (4, 17), (2, 14), (1, 16), (4, 14), (3, 11), (3, 9), (3, 12), (1, 10), (2, 8), (0, 8), (1, 6), (2, 3)]
# WALLS = [(0, 1), (2, 0), (1, 2), (3, 4), (2, 6), (1, 10), (2, 12), (0, 11), (1, 13), (1, 14), (3, 14), (3, 14), (4, 16), (3, 18), (2, 16), (8, 17), (9, 15), (8, 13), (10, 14), (12, 14), (14, 13), (13, 15), (15, 15), (15, 15), (16, 13), (14, 11), (12, 11), (13, 9), (12, 6), (10, 7), (10, 5), (8, 5), (7, 3), (5, 2), (5, 3), (4, 5), (6, 5), (8, 9), (11, 8), (12, 12), (10, 12), (8, 11), (2, 8), (6, 7), (8, 18), (7, 15)]
#
# WALLS = [(0, 1), (2, 0), (1, 2), (3, 4), (2, 6), (1, 10), (2, 12), (0, 11), (1, 13), (1, 14), (3, 14), (3, 14), (4, 16), (3, 18), (2, 16), (8, 17), (9, 15), (8, 13), (10, 14), (12, 14), (14, 13), (13, 15), (15, 15), (15, 15), (16, 13), (14, 11), (12, 11), (13, 9), (12, 6), (10, 7), (10, 5), (7, 3), (5, 2), (5, 3), (4, 5), (6, 6), (5, 8), (12, 12), (8, 5), (7, 8), (9, 9), (11, 8), (10, 11), (10, 12), (8, 11), (6, 12), (8, 18), (5, 14), (2, 8), (3, 10), (4, 12)]
WALLS = [(1, 1), (0, 3), (2, 3), (1, 5), (3, 4), (2, 6), (4, 5), (3, 7), (5, 6), (4, 8), (6, 7), (6, 9), (8, 9), (9, 9), (11, 10), (10, 8), (11, 6), (9, 6), (10, 4), (8, 5), (9, 3), (7, 4), (8, 2), (6, 3), (7, 1), (5, 2), (5, 0), (3, 1), (1, 1), (2, 3), (4, 2), (4, 4), (5, 5), (7, 5), (7, 7), (9, 6), (8, 8), (5, 0), (8, 1), (10, 0), (10, 2), (12, 3), (16, 3), (18, 3), (17, 1), (19, 1), (15, 1), (14, 3), (16, 3), (13, 2), (12, 2), (13, 0), (13, 0), (15, 1), (19, 1), (18, 3), (19, 5), (18, 7), (18, 8), (19, 10), (17, 9), (18, 11), (16, 10), (15, 12), (13, 13), (12, 13), (13, 11), (13, 13), (11, 11), (12, 8), (13, 10), (14, 9), (13, 7), (12, 8), (11, 5), (13, 5), (13, 5), (15, 5), (15, 7), (15, 5), (17, 5), (17, 5), (16, 7), (15, 8), (14, 10), (10, 13), (10, 15), (9, 17), (8, 15), (7, 17), (8, 13), (8, 15), (6, 15), (7, 13), (5, 12), (6, 10), (6, 9), (4, 10), (2, 12), (3, 14), (3, 16), (5, 15), (6, 15), (5, 17), (7, 18), (9, 19), (5, 18), (5, 17), (3, 18), (3, 16), (1, 17), (1, 15), (1, 13), (0, 11), (2, 9), (2, 11), (1, 9), (1, 7), (1, 7), (1, 13), (1, 15), (1, 18), (3, 18), (5, 13), (4, 12), (4, 10), (4, 12), (8, 11), (7, 12)]
PATH = [(0, 0), (0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (2, 4), (2, 5), (3, 5), (3, 6), (4, 6), (4, 7), (5, 7), (5, 8), (6, 8), (7, 8), (7, 9), (7, 10), (8, 10), (9, 10), (10, 10), (10, 9), (11, 9), (11, 8), (11, 7), (10, 7), (10, 6), (10, 5), (9, 5), (9, 4), (8, 4), (8, 3), (7, 3), (7, 2), (6, 2), (6, 1), (6, 0), (7, 0), (8, 0), (9, 0), (9, 1), (10, 1), (11, 1), (11, 2), (11, 3), (11, 4), (12, 4), (13, 4), (14, 4), (15, 4), (16, 4), (17, 4), (17, 3), (17, 2), (18, 2), (19, 2), (19, 3), (19, 4), (18, 4), (18, 5), (18, 6), (19, 6), (19, 7), (19, 8), (19, 9), (18, 9), (18, 10), (17, 10), (17, 11), (16, 11), (15, 11), (14, 11), (14, 12), (14, 13), (14, 14), (13, 14), (12, 14), (11, 14), (11, 13), (11, 12), (10, 12), (9, 12), (9, 13), (9, 14), (9, 15), (9, 16), (10, 16), (10, 17), (10, 18), (9, 18), (8, 18), (8, 17), (8, 16), (7, 16), (6, 16), (5, 16), (4, 16), (4, 15), (3, 15), (2, 15), (2, 16), (2, 17), (2, 18), (2, 19), (1, 19), (0, 19), (0, 18), (0, 17), (0, 16), (0, 15), (0, 14), (0, 13), (0, 12), (1, 12), (1, 11), (1, 10), (2, 10), (3, 10), (3, 9), (3, 8), (2, 8), (1, 8), (0, 8), (0, 7), (0, 6), (0, 5)]

BLOCKED_PATHS = [(1, 0), (9, 8), (9, 7), (8, 7), (8, 6), (7, 6), (6, 6), (6, 5), (6, 4), (5, 4), (5, 3), (4, 3), (3, 3), (3, 2), (2, 2), (2, 1), (2, 0), (3, 0), (4, 0), (4, 1), (5, 1), (19, 0), (15, 3), (11, 0), (12, 0), (12, 1), (13, 1), (15, 0), (14, 0), (14, 1), (14, 2), (15, 2), (16, 2), (16, 1), (16, 0), (17, 0), (18, 0), (18, 1), (13, 12), (12, 7), (12, 5), (12, 6), (13, 6), (14, 5), (16, 5), (15, 10), (15, 9), (16, 9), (16, 8), (17, 8), (17, 7), (17, 6), (16, 6), (15, 6), (14, 6), (14, 7), (14, 8), (13, 8), (13, 9), (12, 9), (12, 10), (12, 11), (12, 12), (8, 14), (8, 19), (7, 19), (2, 10), (0, 4), (0, 5), (1, 6), (0, 6), (0, 7), (3, 8), (2, 7), (2, 8), (1, 8), (0, 8), (0, 9), (0, 10), (1, 10), (1, 11), (1, 12), (0, 12), (0, 13), (1, 14), (0, 14), (0, 15), (2, 18), (3, 19), (2, 19), (1, 19), (0, 19), (0, 18), (0, 17), (0, 16), (1, 16), (2, 16), (2, 17), (3, 17), (4, 17), (4, 18), (4, 19), (5, 19), (6, 19), (6, 18), (6, 17), (6, 16), (5, 16), (4, 16), (5, 14), (4, 13), (4, 14), (4, 15), (3, 15), (2, 15), (2, 14), (2, 13), (3, 13), (3, 12), (4, 11), (3, 11), (3, 10), (3, 9), (4, 9), (5, 9), (5, 10), (5, 11), (7, 11), (6, 11), (6, 12), (6, 13), (6, 14), (7, 14), (7, 15)]

##
X = 8
Y = 8
PATH = [(0, 0), (0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (1, 5), (2, 5), (2, 4), (3, 4), (3, 3), (3, 2), (2, 2), (2, 1), (2, 0), (3, 0), (3, 1), (4, 1), (4, 2), (4, 3), (4, 4), (5, 4), (5, 5), (6, 5), (6, 4), (6, 3), (5, 3), (5, 2), (5, 1), (5, 0), (6, 0), (6, 1), (6, 2), (7, 2), (7, 3), (7, 4)]
WALLS = []
BLOCKED_PATHS = []

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


##
## stub work area
##

#path = [(0,0), (1,0), (1,1), (1,2), (2,2), (3,2), (3,1), (4,1), (5,1), (5,2), (5,3), (5,4), (4,4), (3,4), (3,5)]

# path_char = "░░"
# wall_char = "▓▓"
# maze = get_maze(path, path_char, wall_char)
# print_maze(maze)
# print_maze(maze, True, "▓▓")
# print_maze(maze, True, "▓▓", True)
# print_maze(maze, spacer=True)

# maze = get_maze(path)
# print_maze(maze)
# print_maze(maze, True)
# print_maze(maze, True, spacer=True)
# print_maze(maze, spacer=True)

# print ('----------------')
# border_maze = get_border_maze(path, entry_point=(-1, 0), exit_point=(3, 6))
# print_border_maze(border_maze)
# print_border_maze(border_maze, spacer=True)
#
# border_maze = get_border_maze(path)
# print_border_maze(border_maze)
# print_border_maze(border_maze, spacer=True)

##
## these globals must be defined here
##
#PATH = [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (5, 2), (5, 3), (6, 3), (6, 4), (6, 5), (6, 6), (5, 6), (5, 7), (5, 8), (5, 9), (6, 9), (7, 9), (7, 10), (7, 11), (6, 11), (6, 12), (6, 13), (6, 14), (6, 15), (5, 15), (5, 16), (4, 16), (3, 16), (3, 17), (3, 18), (3, 19), (2, 19), (1, 19), (0, 19), (0, 18), (0, 17), (1, 17), (1, 16), (1, 15), (0, 15), (0, 14), (0, 13), (1, 13), (1, 12), (1, 11), (0, 11), (0, 10), (0, 9), (0, 8), (0, 7), (0, 6), (0, 5), (1, 5), (2, 5), (2, 4), (3, 4), (4, 4), (4, 5), (4, 6), (3, 6), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (3, 10), (3, 11), (4, 11), (4, 12), (4, 13), (3, 13), (3, 14)]
#PATH = [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (5, 2), (5, 3), (6, 3), (6, 4), (6, 5), (6, 6), (5, 6), (5, 7), (5, 8), (5, 9), (6, 9), (7, 9), (7, 10), (7, 11), (6, 11), (6, 12), (6, 13), (6, 14), (6, 15), (5, 15), (5, 16), (4, 16), (3, 16), (3, 17), (3, 18), (3, 19), (2, 19), (1, 19), (1, 18), (1, 17), (1, 16), (2, 16), (2, 15), (3, 15), (3, 14), (3, 13), (2, 13), (1, 13), (1, 12), (0, 12), (0, 11), (0, 10), (0, 9), (1, 9), (1, 8), (2, 8), (2, 7), (3, 7), (3, 6), (3, 5), (3, 4)]
# ctrl + sp + j
#PATH = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (3, 5), (3, 6), (3, 7), (2, 7), (1, 7), (1, 8), (1, 9), (2, 9), (2, 10), (2, 11), (1, 11), (1, 12), (0, 12), (0, 13), (0, 14), (0, 15), (1, 15), (2, 15), (2, 14), (2, 13), (3, 13), (4, 13), (4, 14), (4, 15), (3, 15), (3, 16), (3, 17), (2, 17), (2, 18), (2, 19), (3, 19), (4, 19), (5, 19), (6, 19), (7, 19), (8, 19), (9, 19), (9, 18), (9, 17), (9, 16), (8, 16), (8, 15), (8, 14), (9, 14), (9, 13), (10, 13), (11, 13), (12, 13), (13, 13), (13, 14), (14, 14), (14, 15), (14, 16), (15, 16), (16, 16), (16, 15), (16, 14), (15, 14), (15, 13), (15, 12), (14, 12), (13, 12), (13, 11), (13, 10), (12, 10), (12, 9), (12, 8), (12, 7), (11, 7), (11, 6), (10, 6), (9, 6), (9, 5), (9, 4), (8, 4), (7, 4), (6, 4), (6, 3), (6, 2), (6, 1), (5, 1), (4, 1), (4, 2), (4, 3), (4, 4), (5, 4), (5, 5), (5, 6), (6, 6), (7, 6), (7, 7), (7, 8), (7, 9), (7, 10), (8, 10), (9, 10), (9, 11), (9, 12), (8, 12), (7, 12), (7, 13), (7, 14)]



# For now just make this the last coord in path
#EXIT_POINT = (3, 14)
# EXIT_POINT = (0, 12)
## EXIT_POINT = PATH[len(PATH)-1]
# get it programmatically:
# l = len(PATH)
## print (f'Programmatically determined stopping point: {PATH[len(PATH)-1]}')
# print (f'Manual value: {EXIT_POINT}')

# -------- New code for getting the exit point --------
# -------- This is not taken directly fr the main program but borrows from it and re-works it to fit into this stub
STOPPING_POINT = PATH[len(PATH)-1]
y, x = STOPPING_POINT
if x == X - 1:
    EXIT_POINT = (y, x + 1)
else:
    EXIT_POINT = (y + 1, x)
# --------------------------------------------------------

# first check no path and walls overlap
for i in PATH:
    for j in WALLS:
        if i == j:
            print (f'overlap at coord {i}')

# check no dups in path
path_st = set(PATH)
if len(PATH) != len(path_st):
    print ('there were dups in path')

# --------
maze = get_maze_with_walls(PATH)
border_maze = get_border_maze(maze, entry_point=(0, -1), exit_point=EXIT_POINT)
#print_border_maze(border_maze)
print_border_maze(border_maze, spacer=True)

maze = get_maze_with_walls_and_blocked(PATH)
border_maze = get_border_maze(maze, entry_point=(0, -1), exit_point=EXIT_POINT)
print_border_maze(border_maze, spacer=True)