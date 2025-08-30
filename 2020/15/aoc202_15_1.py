"""Advent of Code: 2020.15.1"""
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

    # Get starting numbers
    line = lines[0].strip()
    init_number = line.split(',')

    # For the game
    turn = 0
    spoken_numbers = {}
    last = int(init_number[-1])

    # Initiate game
    for number in init_number[:-1]:
        turn += 1
        spoken_numbers[int(number)] = turn
    turn += 1

    while turn < 2020:
        turn += 1

        current = 0
        if last in spoken_numbers:
            current = turn - 1 - spoken_numbers[last]

        spoken_numbers[last] = turn-1
        last = current

    print(last)


if __name__ == "__main__":
    main()
