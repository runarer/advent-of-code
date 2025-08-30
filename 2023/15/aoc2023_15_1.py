"""Advent of Code: 2019.1.1"""
import sys
from functools import reduce

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
    print(sum(reduce(lambda x,y: ((x+ord(y))*17)%256,l,0) for l in lines[0].strip().split(',')))


if __name__ == "__main__":
    main()
