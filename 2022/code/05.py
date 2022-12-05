import sys

sys.path.append(".")
from utils import data_import


input_file = "2022/inputs/test.txt"
# input_file = '2022/inputs/05.txt'

data = data_import(input_file, str, ",")
print(data)
