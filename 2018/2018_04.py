import re
from datetime import datetime

def read_input(filename):
    with open(filename, 'r') as f:
        data = f.read().splitlines()
    return(data)

def parse_and_sort_input(li):
    cleaned_list = []
    for index, item in enumerate(li):
        day = re.search(r'\d{4}-\d{2}-\d{2}', item).group()
        time = re.search(r'\d{2}:\d{2}', item).group() + ':00'
        message = item[item.find(']')+2:]
        dt = datetime.strptime(day + ' ' + time, '%Y-%m-%d %H:%M:%S')
        cleaned_list.append((dt, message))
    cleaned_list.sort()
    current_guard = 0
    guard_added_list = []
    for dt, message in cleaned_list:
        if 'Guard' in message:
            current_guard = re.search(r'#\d+', message).group()[1:]
        message = re.sub(r'Guard #\d+ ','', message)
        guard_added_list.append((dt, current_guard, message))
    return(guard_added_list)

def create_shifts(li):
    shift_starts = []
    shift_ends = []
    for index, item in enumerate(li):
        if 'begins' in item[2]:
            shift_starts.append(index)
            shift_ends.append(index-1)
    shift_ends = shift_ends[1:] + [len(li)-1]
    shifts = []
    for start,end in zip(shift_starts, shift_ends):
        current_shift = '.' * 60
        guard = li[start][1]
        date = str(li[start][0].month) + '-' + str(li[start][0].day)
        for index in range(start+1, end+1, 2):
            fall_asleep_minute = li[index][0].minute
            wakes_up_minute = li[index+1][0].minute
            sleep_string = '#' * (wakes_up_minute - fall_asleep_minute)
            current_shift = current_shift[:fall_asleep_minute] + sleep_string + current_shift[wakes_up_minute:]
        shifts.append((date, int(guard), current_shift))
    return(shifts)

def get_guard_IDs(shifts):
    guards = set()
    for _, guard, _ in shifts:
        guards.add(guard)
    return(guards)

def total_sleep_minutes(guard_id, shifts):
    sleep_minutes = 0
    for _, guard, pattern in shifts:
        if guard == guard_id:
            sleep_minutes += pattern.count('#')
    return(sleep_minutes)

def find_sleepiest_guard(shifts):
    guards = get_guard_IDs(shifts)
    sleepiest_guard_id = None
    sleepiest_guard_minutes = 0
    for guard in guards:
        sleep_minutes = total_sleep_minutes(guard, shifts)
        if sleep_minutes > sleepiest_guard_minutes:
            sleepiest_guard_minutes = sleep_minutes
            sleepiest_guard_id = guard
    return(sleepiest_guard_id)

def find_sleepiest_minute(guard_id, shifts):
    sleep_counter = [0] * 60
    for _, guard, pattern in shifts:
        if guard == guard_id:
            for index, c in enumerate(pattern):
                if c == '#': sleep_counter[index] += 1
    max_sleep = max(sleep_counter)
    max_index = [i for i, j in enumerate(sleep_counter) if j == max_sleep]
    return(max_index[0], max_sleep)

def part1(filename):
    raw_data = read_input(filename)
    sorted_data = parse_and_sort_input(raw_data)
    shifts = create_shifts(sorted_data)
    guards = get_guard_IDs(shifts)
    sleepiest_guard = find_sleepiest_guard(shifts)
    sleepiest_minute, _ = find_sleepiest_minute(sleepiest_guard, shifts)
    print('Part 1 Answer:',sleepiest_guard * sleepiest_minute)

def part2(filename):
    raw_data = read_input(filename)
    sorted_data = parse_and_sort_input(raw_data)
    shifts = create_shifts(sorted_data)
    guards = get_guard_IDs(shifts)
    most_frequenct_guard = most_frequent_minute = max_frequency = 0
    for guard in guards:
        minute, frequency = find_sleepiest_minute(guard, shifts)
        if frequency > max_frequency:
            max_frequency = frequency
            most_frequenct_guard = guard
            most_frequent_minute = minute
    print('Part 2 Answer:',most_frequenct_guard * most_frequent_minute)


input_file = '2018/inputs/2018_04_input.txt'
part1(input_file)
part2(input_file)