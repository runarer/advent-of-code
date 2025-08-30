""" Advent of Code: 2020.2.1 """
import sys
import re

def is_valid(line):
    """Check if line is a valid password"""
    results = re.match(r"(\d+)-(\d+) ([a-z]): ([a-z]+)",line)
    lowest = int(results.group(1))
    highest = int(results.group(2))
    letter = results.group(3)
    password = results.group(4)

    nr_of_letter = password.count(letter)
    if lowest <= nr_of_letter <= highest:
        return True
    return False

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
    valids = [ 1 for line in lines if is_valid(line) ]
    print(sum(valids))

if __name__ == "__main__":
    main()
