"""Advent of Code: 2022.2.1"""
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
    #x lose 0
    #y draw 3
    #z win 6
    #a rock 1
    #b paper 2
    #c scissor 3

    total_score = 0
    scores = {'AX':3,'AY':4,'AZ':8,'BX':1,'BY':5,'BZ':9,'CX':2,'CY':6,'CZ':7}
    for line in lines:
        opponent, you = line.strip().split()
        total_score += scores[opponent+you]

    print(total_score)


if __name__ == "__main__":
    main()
