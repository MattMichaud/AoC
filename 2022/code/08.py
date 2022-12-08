test_input = "test.txt"
puzzle_input = "2022/inputs/08.txt"
input_file = puzzle_input

trees = [list(map(int, t)) for t in open(input_file, "r").read().strip().split("\n")]

width = len(trees[0])
height = len(trees)

# Part 1
visible = {}
for y in range(height):
    for x in range(width):
        if x in [0, width - 1] or y in [0, height - 1]:
            visible[(x, y)] = True
        else:
            vis_up = all([trees[y][x] > trees[k][x] for k in range(0, y)])
            vis_down = all([trees[y][x] > trees[k][x] for k in range(y + 1, height)])
            vis_left = all([trees[y][x] > trees[y][j] for j in range(0, x)])
            vis_right = all([trees[y][x] > trees[y][j] for j in range(x + 1, width)])
            visible[(x, y)] = vis_up or vis_down or vis_left or vis_right

total_visible = sum([k for k in visible.values()])
print("Part 1:", total_visible)

# Part 2
def get_scenic_score(height, tree_list):
    score = 0
    for t in tree_list:
        score += 1
        if t >= height:
            return score
    return score


scenic_scores = {}
for y in range(height):
    for x in range(width):
        tree_height = trees[y][x]
        scenic_score = (
            get_scenic_score(tree_height, [trees[k][x] for k in range(0, y)][::-1])
            * get_scenic_score(tree_height, [trees[k][x] for k in range(y + 1, height)])
            * get_scenic_score(tree_height, [trees[y][j] for j in range(0, x)][::-1])
            * get_scenic_score(tree_height, [trees[y][j] for j in range(x + 1, width)])
        )

        scenic_scores[(x, y)] = scenic_score

max_score = max([s for s in scenic_scores.values()])
print("Part 2", max_score)
