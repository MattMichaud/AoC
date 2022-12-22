def parse_input(file):
    raw = open(file, "r").read()
    m, p = raw.split("\n\n")
    m = m.split("\n")
    p = p.strip()

    rows = len(m)
    cols = max(len(r) for r in m)
    # extend shorter rows with blanks
    for row in range(rows):
        while len(m[row]) < cols:
            m[row] += " "
    return m, p


def display_map(m):
    for r in range(len(m)):
        print(m[r], "\t", r)


def get_start_pos(m):
    r = 0
    c = 0
    while m[r][c] != ".":
        c += 1
    return r, c


def follow_path_part1(m, p, dir_list):
    # get dimensions for wrapping
    total_rows = len(m)
    total_cols = max(len(r) for r in m)

    # find starting location
    row, col = get_start_pos(m)
    direction = 1

    # process path instructions
    p_index = 0
    while p_index < len(p):
        # if dealing with a number, get the full number
        steps = 0
        while p_index < len(p) and p[p_index].isdigit():
            steps = steps * 10 + int(p[p_index])
            p_index += 1

        # try to move that number of steps
        for _ in range(steps):
            next_row = (row + dir_list[direction][0]) % total_rows
            next_col = (col + dir_list[direction][1]) % total_cols
            if m[next_row][next_col] == " ":  # blank space
                while m[next_row][next_col] == " ":
                    next_row = (next_row + dir_list[direction][0]) % total_rows
                    next_col = (next_col + dir_list[direction][1]) % total_cols
                if m[next_row][next_col] == "#":
                    break
                row = next_row
                col = next_col
            elif m[next_row][next_col] == "#":  # hit a wall
                break
            else:
                row = next_row
                col = next_col

        # if we are at the end of the path, stop
        if p_index == len(p):
            break

        # next instruction is a turn
        turn = p[p_index]
        dir_offset = {"L": 3, "R": 1}.get(turn)
        direction = (direction + dir_offset) % 4
        p_index += 1

    return (row, col, direction)


test_input = "test.txt"
puzzle_input = "2022/inputs/22.txt"
current_input = puzzle_input

directions = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]  # 0 = up, 1 = right, 2 = down, 3 = left

map, path = parse_input(current_input)
r, c, d = follow_path_part1(map, path, directions)
part1 = 1000 * (r + 1) + 4 * (c + 1) + {1: 0, 2: 1, 3: 2, 4: 3}.get(d)
print("Part 1:", part1)


# faces
#  .12
#  .3.
#  54.
#  6..

FACES = [(0, 1), (0, 2), (1, 1), (2, 1), (2, 0), (3, 0)]


def mapToFace(r, c, edge_length=50):
    # takes a map level row and column and converts to a
    # face level row, face levele col, and face number
    row_num = r // edge_length
    col_num = c // edge_length
    face_num = FACES.index((row_num, col_num)) + 1
    face_row = r % edge_length
    face_col = c % edge_length
    return face_row, face_col, face_num


def faceToMap(f, r, c, edge_length=50):
    # takes a face number, face level row, face level col
    # and converts to map level row and col
    row_num, col_num = FACES[f - 1]
    mr = row_num * edge_length + r
    mc = col_num * edge_length + c
    return mr, mc


# 0 = up, 1 = right, 2 = down, 3 = left
# dictionary to map current face and direction to new face and direction
# this is specific to the input for my puzzle ...
# will also need to handle flipping row or column where approrpiate
face_direction_transitions = {
    (1, 2): (3, 2),
    (1, 0): (6, 1),
    (1, 1): (2, 1),
    (1, 3): (5, 1),
    (2, 2): (3, 3),
    (2, 0): (6, 0),
    (2, 1): (4, 3),
    (2, 3): (1, 3),
    (3, 2): (4, 2),
    (3, 0): (1, 0),
    (3, 1): (2, 0),
    (3, 3): (5, 2),
    (4, 2): (6, 3),
    (4, 0): (3, 0),
    (4, 1): (2, 3),
    (4, 3): (5, 3),
    (5, 2): (6, 2),
    (5, 0): (3, 1),
    (5, 1): (4, 1),
    (5, 3): (1, 1),
    (6, 2): (2, 2),
    (6, 0): (5, 0),
    (6, 1): (4, 0),
    (6, 3): (1, 2),
}


def follow_path_part2(m, p, dir_list):
    # get dimensions for wrapping
    total_rows = len(m)
    total_cols = max(len(r) for r in m)
    face_size = total_cols // 3
    print(face_size)

    # find starting location
    row, col = get_start_pos(m)
    row, col, face_num = mapToFace(row, col, face_size)
    print("start at", (row, col), "on face", face_num)
    direction = 1

    # process path instructions
    p_index = 0
    while p_index < len(p):
        # if dealing with a number, get the full number
        steps = 0
        while p_index < len(p) and p[p_index].isdigit():
            steps = steps * 10 + int(p[p_index])
            p_index += 1

        # try to move that number of steps
        for _ in range(steps):
            next_row = row + dir_list[direction][0]
            next_col = col + dir_list[direction][1]
            if (
                next_row == -1
                or next_row == face_size
                or next_col == -1
                or next_col == face_size
            ):
                # you are trying to leave current face
                new_face, new_dir = face_direction_transitions[(face_num, direction)]
                # 0 = up, 1 = right, 2 = down, 3 = left
                if direction == 2:
                    if new_dir == 2:  # down to down
                        next_row = 0
                        next_col = col
                    elif new_dir == 3:  # down to left
                        next_row = col
                        next_col = face_size - 1
                    else:
                        print("missing new_dir when dir = down")
                elif direction == 0:
                    if new_dir == 0:  # up to up
                        next_row = face_size - 1
                        next_col = col
                    elif new_dir == 1:  # up to right
                        next_row = col
                        next_col = 0
                    else:
                        print("missing new_dir when dir = up")
                elif direction == 1:
                    if new_dir == 1:  # right to right
                        next_row = row
                        next_col = 0
                    elif new_dir == 3:  # right to left
                        next_row = face_size - 1 - row
                        next_col = face_size - 1
                    elif new_dir == 0:  # right to up
                        next_col = row
                        next_row = face_size - 1
                    else:
                        print("missing new_dir when dir = right")
                elif direction == 3:
                    if new_dir == 3:  # left to left
                        next_row = row
                        next_col = face_size - 1
                    elif new_dir == 1:  # left to right
                        next_row = face_size - 1 - row
                        next_col = 0
                    elif new_dir == 2:  # left to down
                        next_col = row
                        next_row = 0
                    else:
                        print("missing new_dir when dir = left")

                check_row, check_col = faceToMap(new_face, next_row, next_col)
                if map[check_row][check_col] == "#":
                    break
                else:
                    row = next_row
                    col = next_col
                    direction = new_dir
                    face_num = new_face

            else:
                map_next_row, map_next_col = faceToMap(face_num, next_row, next_col)
                if m[map_next_row][map_next_col] == "#":
                    break
                else:
                    row = next_row
                    col = next_col

        # if we are at the end of the path, stop
        if p_index == len(p):
            break

        # next instruction is a turn
        turn = p[p_index]
        dir_offset = {"L": 3, "R": 1}.get(turn)
        direction = (direction + dir_offset) % 4
        p_index += 1

    map_row, map_col = faceToMap(face_num, row, col)
    return (map_row, map_col, direction)


r, c, d = follow_path_part2(map, path, directions)
part2 = 1000 * (r + 1) + 4 * (c + 1) + {1: 0, 2: 1, 3: 2, 4: 3}.get(d)
print("Part 2:", part2)
