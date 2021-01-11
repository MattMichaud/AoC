def parse_input(filename):
    with open(filename, 'r') as f:
        data = f.read()
    data = [int(c) for c in data.split()]
    return(data)

def sum_metadata(li):
    children_quantity = li[0]
    meta_quantity = li[1]
    remaining_li = li[2:]
    children_processed = 0
    meta_sum = 0
    while children_processed < children_quantity:
        children_sum, remaining_li = sum_metadata(remaining_li)
        meta_sum += children_sum
        children_processed += 1
    meta_sum += sum(remaining_li[:meta_quantity])
    return(meta_sum, remaining_li[meta_quantity:])


def node_value(li):
    children_quantity = li[0]
    meta_quantity = li[1]
    remaining_li = li[2:]
    children_processed = 0
    children_values = []
    while children_processed < children_quantity:
        child_value, remaining_li = node_value(remaining_li)
        children_values.append(child_value)
        children_processed += 1
    meta_refs = remaining_li[:meta_quantity]
    remaining_li = remaining_li[meta_quantity:]
    if children_quantity == 0:
        return(sum(meta_refs), remaining_li)
    else:
        meta_sum = 0
        for index in meta_refs:
            if 0 < index <= children_quantity:
                meta_sum += children_values[index - 1]
        return(meta_sum, remaining_li)


input_file = '2018_08_input.txt'
input_list = parse_input(input_file)
result, _ = sum_metadata(input_list)
print('Part 1 Answer:', result)
result, _ = node_value(input_list)
print('Part 2 Answer:', result)