def parse_input(filename):
    with open(filename, 'r') as f:
        data = f.read().splitlines()
    return(data)

def parse_claim(claim):
    at = claim.find('@')
    comma = claim.find(',')
    colon = claim.find(':')
    x = claim.find('x')

    claim_id = int(claim[1:at-1])
    start_x = int(claim[at+1:comma])
    start_y = int(claim[comma+1:colon])
    dim_x = int(claim[colon+1:x])
    dim_y = int(claim[x+1:])

    return(claim_id, start_x, start_y, dim_x, dim_y)

def process_claims(claims):
    fabric = {}
    for claim in claims:
        claim_id, start_x, start_y, dim_x, dim_y = parse_claim(claim)
        for (dx,dy) in [(x,y) for x in range(dim_x) for y in range(dim_y)]:
            loc = (start_x + dx, start_y + dy)
            if loc not in fabric:
                fabric[loc] = [claim_id]
            else:
                fabric[loc].append(claim_id)
    return(fabric)

def part1(fabric):
    square_inches = 0
    for item in fabric:
        if len(fabric[item]) >= 2:
            square_inches += 1
    return(square_inches)

def part2(claims, fabric):
    claim_IDs = set()
    for claim in claims:
        claim_id, _, _, _, _ = parse_claim(claim)
        claim_IDs.add(claim_id)
    for loc in fabric:
        if len(fabric[loc]) > 1:
            for id in fabric[loc]:
                if id in claim_IDs:
                    claim_IDs.remove(id)
    if len(claim_IDs) == 1:
        return(claim_IDs.pop())
    else:
        return(0)

claims = parse_input('2018/inputs/2018_03_input.txt')
fabric = process_claims(claims)
test_input = ['#1 @ 1,3: 4x4','#2 @ 3,1: 4x4','#3 @ 5,5: 2x2']
print('Part 1 Answer:',part1(fabric))
print('Part 2 Answer:',part2(claims, fabric))