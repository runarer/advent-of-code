"""Advent of Code: 2019.1.1
    Do not need the path, just the cost.
    So for each grid, we want the smallest cost to get there from start

    When a move is made; three obstacles are placed around and 3 steps away.
    Changing direction removes obstacle.
    Continue moving in the same direction do not move the obstacle in front.
    
"""
import sys
from queue import PriorityQueue

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
    q = PriorityQueue()

    q.put((2,"Hello World"))
    q.put((11, 99))
    q.put((5,7.5))
    q.put((1, True))

    while not q.empty():
        print(q.get())

if __name__ == "__main__":
    main()
