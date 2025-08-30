"""Advent of Code: 2022.1.1"""
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
    max_calories = 0
    sum_calories = 0
    for line in lines:
        line = line.strip()
        if line == "":
            max_calories = max(max_calories,sum_calories)
            sum_calories = 0
        else:
            sum_calories += int(line)

    print(max_calories)
        


        


if __name__ == "__main__":
    main()
