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
    #lose 0
    #draw 3
    #win 6
    #a x rock 1
    #b y paper 2
    #c z scissor 3
    total_score = 0
    scores = {'AX':4,'AY':8,'AZ':3,'BX':1,'BY':5,'BZ':9,'CX':7,'CY':2,'CZ':6}    
    for line in lines:
        opponent, you = line.strip().split()
        total_score += scores[opponent+you]

    print(total_score)

if __name__ == "__main__":
    main()
