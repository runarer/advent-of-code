"""Advent of Code: 2022.5.1"""
import sys
import re

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
    # Map of stacks
    nr_stacks = 0
    moves_start = 1 # Skipping an empty line
    cargo_input = []

    # Get cargo stacks and the number of stacks
    for line in lines:
        moves_start += 1

        results = re.findall(r"\s+(\d+)\s?",line)
        if results:
            nr_stacks = int(results[-1])
            break
        else:
            cargo_input.append([line[x:x+3] for x in range(0,len(line),4)])

    cargo_stacks = {x:[] for x in range(1,nr_stacks+1)}

    for cargos in cargo_input[::-1]:
        current_stack = 0
        for cargo in cargos:
            current_stack += 1
            if cargo == "   ":
                continue
            else:
                cargo_stacks[current_stack].append(cargo)

    # Do the moves
    for line in lines[moves_start:]:
        move = line.strip().split()
        move_nr = int(move[1])
        move_from = int(move[3])
        move_to = int(move[5])
        for _ in range(0,move_nr):
            cargo_stacks[move_to].append(cargo_stacks[move_from].pop())

    # Print results
    answer = ""
    for top in cargo_stacks.values():
        answer += top.pop()[1]
    print(answer)

if __name__ == "__main__":
    main()
