import sys
import re

sys.path.append(".")
from utils import data_import

f = lambda a, b, c, d: (set(range(a, b + 1)), set(range(c, d + 1)))
assignments = [
    f(*map(int, re.findall(r"\d+", assignment)))
    for assignment in sys.stdin.read().strip().split("\n")
]
