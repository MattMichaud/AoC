import sys
sys.path.append('.')
from utils import IntCodeComputer

def update_pos_dir(currX, currY, curr_dir, comp_output):

    if (curr_dir == 0 and comp_output == 0) or (curr_dir == 2 and comp_output == 1): return currX - 1, currY, 3
    elif (curr_dir == 0 and comp_output == 1) or (curr_dir == 2 and comp_output == 0): return currX + 1, currY, 1
    elif (curr_dir == 1 and comp_output == 0) or (curr_dir == 3 and comp_output == 1): return currX, currY - 1, 0
    elif (curr_dir == 1 and comp_output == 1) or (curr_dir == 3 and comp_output == 0): return currX, currY + 1, 2

def create_hull(hull_size):
    hull = []
    for i in range(hull_size):
        hull.append([])
        for j in range(hull_size):
            hull[i].append([])
            hull[i][j]=[0,0] # [colour, 0 if never painted / 1 if it has]
    return hull

def part1(filename):
    data = [int(c) for c in open(filename).read().split(",")]
    hull_size = 100
    hull = create_hull(hull_size)
    direction = 0 # 0 up / 1 right / 2 down / 3 left
    posX = posY = int(hull_size/2) # start in the middle

    comp0 = IntCodeComputer(programCode=data)
    comp0.addInput(hull[posX][posY][0])
    while(comp0.finished is not True):
        comp0.compute()
        outputFromComp = comp0.outputArray[-2:]
        hull[posX][posY][0] = outputFromComp[0]
        hull[posX][posY][1] = 1
        posX, posY, direction = update_pos_dir(posX, posY, direction, outputFromComp[1])
        comp0.addInput(hull[posX][posY][0])

    total_painted = sum(1 for i in range(hull_size) for j in range(hull_size) if hull[i][j][1] == 1)
    print('Part 1 Answer: {}'.format(total_painted))

def part2(filename):
    from PIL import Image
    data = [int(c) for c in open(filename).read().split(",")]
    hull_size = 100
    hull = create_hull(hull_size)
    direction = 0 # 0 up / 1 right / 2 down / 3 left
    posX = posY = int(hull_size/2) # start in the middle

    comp0 = IntCodeComputer(programCode=data)
    hull[posX][posY][0]=1
    comp0.addInput(hull[posX][posY][0])
    while(comp0.finished is not True):
        comp0.compute()
        outputFromComp = comp0.outputArray[-2:]
        hull[posX][posY][0] = outputFromComp[0]
        hull[posX][posY][1] = 1
        posX, posY, direction = update_pos_dir(posX, posY, direction, outputFromComp[1])
        comp0.addInput(hull[posX][posY][0])

    ###Some non vital code to make the image more readable
    left_most = right_most = up_most = down_most = -1

    x_coords = [x for x in range(hull_size) for y in range(hull_size) if hull[x][y][0] == 1]
    y_coords = [y for x in range(hull_size) for y in range(hull_size) if hull[x][y][0] == 1]
    left_most = min(x_coords)
    right_most = max(x_coords)
    up_most = min(y_coords)
    down_most = max(y_coords)

    zoom = 20
    picX = (right_most - left_most + 3) * zoom
    picY = (down_most - up_most + 3) * zoom
    im = Image.new('RGB', (picX, picY), "black")
    for hullX in range(left_most-1,right_most+2):
        for hullY in range(up_most-1,down_most+2):
            for xVal in range(zoom):
                for yVal in range(zoom):
                    if (hull[hullX][hullY][0] == 1):
                        im.putpixel(((hullX-left_most)*zoom+xVal+zoom, (hullY-up_most)*zoom+yVal+zoom), (255, 255, 255, 255))
                    else:
                        im.putpixel(((hullX-left_most)*zoom+xVal+zoom, (hullY-up_most)*zoom+yVal+zoom), (0, 0, 0, 255))
    im.show()

filename = '2019/inputs/11.txt'
part1(filename)
part2(filename)