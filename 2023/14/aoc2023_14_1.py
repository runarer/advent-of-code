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
    panel = [line.strip() for line in lines]
    to_south = len(panel)

    total_load = 0
    for j in range(len(panel[0])):
        next_moves_to = 0

        for i,p in enumerate(panel):
            if p[j] != '.':
                if p[j] == '#':
                    next_moves_to = i + 1
                else:
                    total_load += to_south - next_moves_to
                    next_moves_to += 1

    print(total_load)

if __name__ == "__main__":
    main()
