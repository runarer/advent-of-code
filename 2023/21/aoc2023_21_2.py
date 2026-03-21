"""Advent of Code: 2019.1.1"""
import sys
"""
    The magical numbers used were found with aoc2023_21_2_findSquareValues.py

    These can also be calculated, 
"""
def countStepsInSquares(squares):
    return 7335*((squares+1)//2) + 7320*(squares//2)

def countTop():
    return 932+5522+935

def countBottom():
    return 937+5518+931

def countCenter(centerSquares):
    return 5506+5534+countStepsInSquares(centerSquares)

def countFromCenter(squares,west,east):
    total = 0
    while(squares > 0):
        total += west+east+countStepsInSquares(squares)
        squares -= 2
    return total



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

    steps = 26501365
    centerSquares = ((steps-65) * 2)//131 - 2 + 1
    totalSteps = countTop() + countBottom() + countCenter(centerSquares)+countFromCenter(centerSquares-2,932+6415,935+6427)+countFromCenter(centerSquares-2,937+6411,931+6427)
    print(totalSteps)


if __name__ == "__main__":
    main()
