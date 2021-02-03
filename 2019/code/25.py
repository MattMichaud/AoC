import sys
sys.path.append('.')
from intcode_2 import Intcode
from utils import read_intcode

filename = '2019/inputs/25.txt'
vm = Intcode(read_intcode(filename))
vm.run_until_io_or_done()
vm.run_until_io_or_done()
print(vm.get_output())

# used simulator at https://mazegame.org/adventofcode/2019/day25/index.html