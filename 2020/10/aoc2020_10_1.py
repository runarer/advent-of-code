"""Advent of Code: 2020.10.1"""
import sys

def main():
    """Start"""
    #get argument
    if len(sys.argv) < 1:
        sys.exit("Usage: python " + sys.argv[0] + " filename")
    filename = sys.argv[1]
    try:
        with open(filename, 'rt', encoding="utf-8") as file:
            lines = file.readlines()
    except IOError as err:
        print(f"{err}\nError opening {filename}. Terminating program.", file=sys.stderr)
        sys.exit(1)

    # Do stuff with lines
    adapters = [0] + [ int(line.strip()) for line in lines]
    adapters.sort()

    ones = 0
    threes = 1
    for i in range(1,len(adapters)):
        diff = adapters[i] - adapters[i-1]
        if diff == 3:
            threes += 1
        elif diff == 1:
            ones += 1

    print(ones,threes,ones*threes)

if __name__ == "__main__":
    main()
