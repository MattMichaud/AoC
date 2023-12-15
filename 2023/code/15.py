def parse_input(filename):
    return open(filename, "r").read().strip().split(",")


def hash(input):
    cv = 0
    for c in input:
        cv += ord(c)
        cv = cv * 17
        cv = cv % 256
    return cv


def hashmap(input):
    # need 256 boxes
    # will contain tuples of (labal, focal_length)
    boxes = []
    for _ in range(256):
        boxes.append([])
    # process each step
    for step in input:
        if step[-1] == "-":
            # remove from box if exists
            lbl = step[:-1]
            box = hash(lbl)
            contents = boxes[box]
            new_contents = []
            for l, fl in contents:
                if l != lbl:
                    new_contents.append((l, fl))
            boxes[box] = new_contents
            next
        elif "=" in step:
            # add to box or update focal length
            lbl = step[:-2]
            box = hash(lbl)
            focal_length = int(step[step.find("=") + 1 :])
            current_contents = boxes[box]
            current_labels = [l for l, fl in current_contents]
            if lbl not in current_labels:
                # add to back of box
                boxes[box].append((lbl, focal_length))
            else:
                # update focal length
                new_contents = []
                for l, fl in current_contents:
                    if l != lbl:
                        new_contents.append((l, fl))
                    else:
                        new_contents.append((l, focal_length))
                boxes[box] = new_contents
            next
    return boxes


def focusing_power(boxes):
    total_fp = 0
    for box_num, box in enumerate(boxes):
        for slot, lens in enumerate(box):
            fp = (box_num + 1) * (slot + 1) * lens[1]
            total_fp += fp
    return total_fp


test = "2023/inputs/test.txt"
puzzle = "2023/inputs/15.txt"
filename = puzzle

steps = parse_input(filename)
print("Part 1:", sum(hash(s) for s in steps))
print("Part 2:", focusing_power(hashmap(steps)))
