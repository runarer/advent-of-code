"""
Advent of Code: 2020.1.1

Dette skal være bedre enn O(n2):

Sorter først.
Loop over nummerlisten.
    Finn summen av minste og største. 
    Er den riktig, så ferdig.
    Er den for høy, så sett største til nest største.
    Else, sett minste til nest minste.
"""
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

    numbers = [ int( line.strip() ) for line in lines]

    numbers.sort()
    smallest = 0
    largest = len(numbers)-1
    for _ in range(len(numbers)):
        summed = numbers[smallest] + numbers[largest]
        if summed == 2020:
            print(numbers[smallest] * numbers[largest])
            sys.exit(1)
        if summed > 2020:
            largest -= 1
        else:
            smallest += 1
    print("No pairs found")

    # match = [ x*y for x in numbers for y in numbers if x + y == 2020]
    # print(match[0])

    # nrs = len(numbers)
    # for _ in range(nrs):
    #     number = numbers.pop()
    #     lookfor = 2020 - number
    #     if lookfor in numbers:
    #         print(f"{number} * {lookfor} = {number*lookfor}")
    #         sys.exit(0)
    # print("Did not find any pairs")

if __name__ == "__main__":
    main()
