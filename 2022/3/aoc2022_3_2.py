"""Advent of Code: 2022.3.2"""
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
    lines = [set(line.strip()) for line in lines]
    groups = [lines[x:x+3] for x in range(0,len(lines),3)]
    sum_of_badges = 0
    for g in groups:
        badge = list( g[0].intersection(g[1]).intersection(g[2]))[0]
        if badge.isupper():
            sum_of_badges += ord(badge)-38
        else:
            sum_of_badges += ord(badge)-96
    print(sum_of_badges)








if __name__ == "__main__":
    main()
