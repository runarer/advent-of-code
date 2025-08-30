"""
  Advent of Code: 2019.1.1
    
    For each XXA; when does the instructions and position repeat.
    I need to know how many steps until a XXZ. (Are there more than one XXZ for each starting pos)
    Then how many iterations of the instruction to end up back at XXZ.
"""
import sys, math

def main():
    """Start"""
    #get argument
    if len(sys.argv) < 2:
        sys.exit("Usage: python " + sys.argv[0] + " filename")
    filename = sys.argv[1]
    try:
        with open(filename, 'rt', encoding="utf-8") as file:
            lines = file.readlines()
    except IOError as err:
        print(f"{err}\nError opening {filename}. Terminating program.", file=sys.stderr)
        sys.exit(1)

    # Do stuff with lines
    instructions = lines[0].strip()
    nr_inst = len(instructions)
    desert_map = { line[0:3] : { 'L' : line[7:10], 'R' : line[12:15] } for line in lines[2:]}

    positions = [ pos for pos in desert_map.keys() if pos[2] == 'A']
    steps_until_z =  { pos : 0  for pos in positions}

    for pos in positions:
        steps = 0
        current_position = pos
        while current_position[2] != 'Z':
            next_instruction = instructions[ steps % nr_inst]
            current_position = desert_map[current_position][next_instruction]
            steps += 1
        steps_until_z[pos] = steps

    to_align = sorted(steps_until_z.values())[1:]
    min_steps_pr_round = min(steps_until_z.values())

    multiplier = 1
    multipliers = []
    for ta in to_align[::-1]:
        steps = min_steps_pr_round
        multiplier = 1

        while steps % ta != 0:
            steps += min_steps_pr_round
            multiplier += 1

        multipliers.append(multiplier)

    total_number_of_steps = min_steps_pr_round * math.prod(multipliers)
    print(total_number_of_steps)


if __name__ == "__main__":
    main()
