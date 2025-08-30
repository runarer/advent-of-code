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
    rocks = set()
    start = None

    for i,line in enumerate(lines):
        for j,c in enumerate (line.strip()):
            if c == 'S':
                start = (i,j)
            elif c == '#':
                rocks.add( (i,j) )

    steps = set()
    steps.add(start)
    for _ in range(64):
        next_steps = set()

        for s in steps:
            for ns in [(s[0]-1,s[1]),(s[0],s[1]+1),(s[0]+1,s[1]),(s[0],s[1]-1)]:
                if ns not in rocks:
                    next_steps.add(ns)
        steps = next_steps

    print(len(steps))



if __name__ == "__main__":
    main()
