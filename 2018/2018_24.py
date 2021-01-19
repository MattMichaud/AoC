IMMUNE_SYSTEM = 'Immune System'
INFECTION = 'Infection'

class Group:

    def __init__(self, group_type, group_id, unit_count, hit_points, immune_list, weakness_list, attack_damage, attack_type, initiative):
        self.unit_count = unit_count
        self.type = group_type
        self.id = group_id
        self.unit_hit_points = hit_points
        self.unit_attack_damage = attack_damage
        self.attack_type = attack_type
        self.initiative = initiative
        self.weaknesses = weakness_list
        self.immunities = immune_list

    @property
    def effective_power(self):
        return self.unit_count * self.unit_attack_damage

    def atk_dmg(self, defender):
        damage = self.effective_power
        if self.attack_type in defender.immunities:
            damage = 0
        if self.attack_type in defender.weaknesses:
            damage *= 2
        return(damage)

def build_groups(filename, boost=0):
    data = open(filename, 'r').readlines()
    groups = []
    unit_type = ''
    current_id = 1
    for line in data:
        if line[:3] == 'Imm':
            unit_type = IMMUNE_SYSTEM
            current_id = 1
            boost_amount = boost
        elif line[:3] == 'Inf':
            unit_type = INFECTION
            current_id = 1
            boost_amount = 0
        elif line[0].isdigit():
            line = line.replace('\n','').split(' ')
            unit_count = int(line[0])
            hit_points = int(line[4])
            line = ' '.join(line[7:])
            weakness_list = []
            immune_list = []
            if line[0] == '(':
                subgroup = [i.split(' to ') for i in line[1:line.find(')')].split('; ')]
                for i in subgroup:
                    if i[0] == 'weak':
                        weakness_list.extend(i[1].split(', '))
                    else:
                        immune_list.extend(i[1].split(', '))
                line = line[line.find(')')+2:]
                pass
            line = line.split(' ')
            attack_damage = int(line[5])
            attack_type = line[6]
            initiative = int(line[-1])
            groups.append(Group(unit_type, current_id, unit_count, hit_points, immune_list, weakness_list, attack_damage + boost_amount, attack_type, initiative))
            current_id += 1
    return(groups)

def fight(groups, debug=False):
    immune_system = set([g for g in groups if g.type == IMMUNE_SYSTEM])
    infection = set([g for g in groups if g.type == INFECTION])

    while immune_system and infection:
        potential_combatants = immune_system | infection
        attacking = {}
        for combatant in sorted(immune_system | infection, key=lambda x: (x.effective_power, x.initiative), reverse=True):
            try:
                s = max((x for x in potential_combatants if x.type != combatant.type and combatant.atk_dmg(x) != 0), key=lambda x: (combatant.atk_dmg(x), x.effective_power, x.initiative))
            except:
                attacking[combatant] = None
                continue
            potential_combatants.remove(s)
            attacking[combatant] = s
        did_damage = False
        for combatant in sorted(immune_system | infection, key=lambda x: x.initiative, reverse=True):
            if combatant.unit_count <= 0:
                continue
            target = attacking[combatant]
            if target is None:
                continue
            killed_units = combatant.atk_dmg(target) // target.unit_hit_points
            if killed_units > 0:
                did_damage = True
            target.unit_count -= killed_units
            if target.unit_count <= 0:
                immune_system -= {target}
                infection -= {target}
        if not did_damage: return None
    winner = max(immune_system, infection, key=len)
    return winner

def part1(filename):
    groups = build_groups(input_file, 0)
    winner = fight(groups)
    winning_score = sum(x.unit_count for x in winner)
    print('Part 1 Answer:',winning_score)

def part2(filename, starting_increment=1000):
    increment = starting_increment
    current = 0
    while True:
        groups = build_groups(input_file, boost=current)
        winner = fight(groups)
        immune_win = False
        winning_score = None
        if winner:
            winning_score = sum(x.unit_count for x in winner)
            for i in winner:
                if i.type == IMMUNE_SYSTEM:
                    immune_win = True
                    break
        if immune_win:
            if increment == 1:
                #print('Boost Amount:', current)
                print('Part 2 Answer:', winning_score)
                break
            else:
                current = current - increment
                increment = int(increment / 10)
        else:
            current += increment

input_file = 'test_input.txt'
input_file = '2018/inputs/2018_24_input.txt'
part1(input_file)
part2(input_file)