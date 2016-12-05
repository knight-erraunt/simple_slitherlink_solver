import itertools as it

EMPTY = -1
OUT_OF_BOARD = -2
UP = 1
DOWN = 2
RIGHT = 3
LEFT = 4

ALL_DIRS = [
    [-1, 0],
    [1,  0],
    [0, -1],
    [0,  1]
]

OFFSET_TO_DIR = {
    (-1, 0): UP,
    (1,  0): DOWN,
    (0,  1): RIGHT,
    (0, -1): LEFT
}


class Board:
    pass


def edge_to_faces(edge):
    begin, end = edge
    if begin[0] == end[0]:
        return [(begin[0], begin[1] - 1), (begin[0], begin[1])]
    else:
        return [(begin[0] - 1, begin[1]), (begin[0], begin[1])]


def face_to_edges(i, j):
    # the points surrounding the face
    A = (i, j)
    B = (i, j + 1)
    C = (i + 1, j)
    D = (i + 1, j + 1)
    return [(A, B), (A, C), (B, D), (C, D)]


def global_check(board, edges_taken, final=False):
    for i, j in it.product(range(board.nums_height), range(board.nums_width)):
        if board.nums[i][j] != EMPTY:
            amount_taken = 0
            for edge in face_to_edges(i, j):
                if edge in edges_taken:
                    amount_taken += 1
            if amount_taken > board.nums[i][j] or \
                    (final and amount_taken != board.nums[i][j]):
                return False
    return True


def fast_check(board, edges_taken, face):
    i, j = face
    if board.nums[i][j] != EMPTY:
        amount_taken = 0
        for edge in face_to_edges(i, j):
            if edge in edges_taken:
                amount_taken += 1
        if amount_taken > board.nums[i][j]:
            return False
    return True


def backtrack(board, edges_taken=None, i=1, j=1, begin_i=1, begin_j=1):
    if not edges_taken:  # edges are represented by an ORDERED pair of pairs
        edges_taken = set()
    if abs(begin_i - i) + abs(begin_j - j) == 1 and len(edges_taken) > 1:
        last_edge = tuple(sorted([(begin_i, begin_j), (i, j)]))
        board.dots[i][j] = OFFSET_TO_DIR[(begin_i - i, begin_j - j)]
        edges_taken.add(last_edge)
        if global_check(board, edges_taken, final=True):
            return True
        board.dots[i][j] = EMPTY
        edges_taken.remove(last_edge)

    for (offset, dir_to_next) in OFFSET_TO_DIR.items():
        next_i, next_j = i + offset[0], j + offset[1]
        if board.dots[next_i][next_j] == EMPTY:
            board.dots[i][j] = dir_to_next
            edge_being_added = tuple(sorted([(i, j), (next_i, next_j)]))
            edges_taken.add(edge_being_added)
            face_A, face_B = edge_to_faces(edge_being_added)
            if fast_check(board, edges_taken, face_A) and \
                    fast_check(board, edges_taken, face_B):
                ret_val = backtrack(board, edges_taken,
                                    next_i, next_j, begin_i, begin_j)
                if ret_val:
                    return True
            board.dots[i][j] = EMPTY
            edges_taken.remove(edge_being_added)

    return False


if __name__ == "__main__":
    n, m = map(int, input().split())
    B = Board()
    B.nums_height = n + 2
    B.nums_width = m + 2
    B.nums = [[EMPTY] * B.nums_width]
    for i in range(1, B.nums_height - 1):
        B.nums += [[EMPTY] + [int(x) for x in input().split()] + [EMPTY]]
    B.nums += [[EMPTY] * B.nums_width]

    # for debuging purposes
    #for row in B.nums:
    #    print(' '.join(map(str, row)))
    #print()

    B.dots_height = B.nums_height + 1
    B.dots_width = B.nums_width + 1
    B.dots = [[OUT_OF_BOARD] * B.dots_width]
    for i in range(1, B.dots_height - 1):
        B.dots += [[OUT_OF_BOARD] + [EMPTY] * (B.dots_width - 2) +
                   [OUT_OF_BOARD]]
    B.dots += [[OUT_OF_BOARD] * B.dots_width]

    # ugly part
    biggest_tile, biggest_tile_val = (1, 1), B.nums[1][1]
    for i in range(B.nums_height):
        for j in range(B.nums_width):
            if B.nums[i][j] > biggest_tile_val:
                biggest_tile_val = B.nums[i][j]
                biggest_tile = (i, j)

    # dangerous assumption that there is a tile with val >= 1
    # ... and all the tiles are <= 3
    tile_val_to_beginings = {
        3: [(0, 0)],
        2: [(0, 0), (0, 1)],
        1: [(0, 0), (0, 1), (1, 0)]
    }

    found_solution = False
    for begining_offsets in tile_val_to_beginings[biggest_tile_val]:
        begin_i = biggest_tile[0] + begining_offsets[0]
        begin_j = biggest_tile[1] + begining_offsets[1]
        if backtrack(B, edges_taken=None, i=begin_i, j=begin_j,
                     begin_i=begin_i, begin_j=begin_j):
            found_solution = True
            break

    if found_solution:
        print(str(B.dots_height) + " " + str(B.dots_width))
        for dots_row in B.dots:
            print(' '.join(map(str, dots_row)))
        print()
    else:
        print("No solution")
