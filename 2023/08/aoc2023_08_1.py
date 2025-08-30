"""Advent of Code: 2019.1.1"""
import sys

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
    desert_map = { line[0:3] : { 'L' : line[7:10], 'R' : line[12:15] } for line in lines[2:]}

    steps = 0
    current_position = "AAA"
    while current_position != "ZZZ":
        next_instruction = instructions[steps % len(instructions)]
        current_position = desert_map[current_position][next_instruction]
        steps += 1

    print(steps)


if __name__ == "__main__":
    main()
