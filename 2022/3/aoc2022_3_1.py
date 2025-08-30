"""Advent of Code: 2022.3.1"""
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
    sum_of_items = 0
    for line in lines:
        sack = line.strip()
        room1 = set(sack[0:int(len(sack)/2)])
        room2 = set(sack[int(len(sack)/2):])
        shared_item = list(room1.intersection(room2))[0]
        if shared_item.isupper():
            sum_of_items += ord(shared_item)-38
        else:
            sum_of_items += ord(shared_item)-96

    print(sum_of_items)

if __name__ == "__main__":
    main()
