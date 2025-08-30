"""Advent of Code: 2024.2.1"""
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
    total_sum = 0
    for line in lines:
        results = re.findall(r"mul\((\d+),(\d+)\)",line)
        total_sum += sum(int(a)*int(b) for a,b in results)
        print(results)
    print(total_sum)



if __name__ == "__main__":
    main()
