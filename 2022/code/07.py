import sys

sys.path.append(".")
from utils import data_import


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def get_size(self):
        return self.size


class Directory:
    def __init__(self, dir_name, parent_dir=None):
        self.name = dir_name
        self.files = []
        self.subdirectories = []
        self.parent_dir = parent_dir
        if parent_dir is not None:
            parent_dir.add_subdirectory(self)

    def add_file(self, file):
        self.files.append(file)

    def add_subdirectory(self, subdirectory):
        self.subdirectories.append(subdirectory)

    def get_size(self):
        return sum(f.get_size() for f in self.files) + sum(
            d.get_size() for d in self.subdirectories
        )

    def get_parent(self):
        return self.parent_dir


def process_commands(commmand_list):
    fs = {}
    fs["/"] = Directory("/")
    current_dir = fs["/"]

    for command in commmand_list:

        # $ cd .. = go to parent directory
        if command[:7] == "$ cd ..":
            current_dir = current_dir.get_parent()

        # special case of $ cd /
        elif command == "$ cd /":
            current_dir = fs["/"]

        # $ cd = change current_directory
        elif command[:4] == "$ cd":
            dir_name = command[5:]
            if current_dir.name == "/":
                dir_name = "/" + dir_name
            else:
                dir_name = current_dir.name + "/" + dir_name
            current_dir = fs[dir_name]

        # $ ls = do nothing
        elif command == "$ ls":
            next

        # dir 'name' = add directory to filesystem
        elif command[:3] == "dir":
            dir_name = command.replace("dir ", "")
            if current_dir.name == "/":
                dir_name = "/" + dir_name
            else:
                dir_name = current_dir.name + "/" + dir_name
            fs[dir_name] = Directory(dir_name, current_dir)

        # number name = add file to current directory
        else:
            size, name = command.split(" ")
            current_dir.add_file(File(name, int(size)))

    return fs


test_file = "test.txt"
puzzle_file = "2022/inputs/07.txt"
input_file = puzzle_file

commands = data_import(input_file)
res = process_commands(commands)

part1 = sum(k.get_size() for k in res.values() if k.get_size() < 100000)
print("Part 1:", part1)

part2 = min(
    [
        k.get_size()
        for k in res.values()
        if k.get_size() >= (res["/"].get_size() - 40000000)
    ]
)
print("Part 2:", part2)
