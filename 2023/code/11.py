import itertools


def m_distance(pt1, pt2):
    return abs(pt1[0] - pt2[0]) + abs(pt1[1] - pt2[1])


def parse_input(filename):
    image = open(filename, "r").read().splitlines()
    width = len(image[0])
    length = len(image)
    stars = {}
    for r in range(length):
        for c in range(width):
            if image[r][c] == "#":
                stars[(r, c)] = "#"
    return stars


def expand_image(image, expansion_amount=1):
    distinct_r = set([r for r, c in image.keys()])
    distinct_c = set([c for r, c in image.keys()])
    min_r = min(distinct_r)
    max_r = max(distinct_r)
    min_c = min(distinct_c)
    max_c = max(distinct_c)
    empty_rows = set(range(min_r, max_r + 1)) - distinct_r
    empty_cols = set(range(min_c, max_c + 1)) - distinct_c
    new_image = {}
    for star_row, star_col in image.keys():
        empty_above = len([x for x in empty_rows if x < star_row])
        empty_left = len([y for y in empty_cols if y < star_col])
        new_image[
            (
                star_row + (expansion_amount * empty_above),
                star_col + (expansion_amount * empty_left),
            )
        ] = "#"
    return new_image


def sum_distances(stars):
    return sum(
        m_distance(pt1, pt2)
        for pt1, pt2 in list(itertools.combinations(stars.keys(), 2))
    )


test = "2023/inputs/test.txt"
puzzle = "2023/inputs/11.txt"

stars = parse_input(puzzle)
print("Part 1:", sum_distances(expand_image(stars)))
print("Part 2:", sum_distances(expand_image(stars, 10**6 - 1)))
