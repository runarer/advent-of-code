""" Advent of Code: 2020.3.1

"""
import sys
from functools import reduce

def nr_of_trees_hit(down, right, map_of_slope):
    """ Takes a 2d list of bools, reprecenting tree or no tree."""
    trees_hit = 0
    row_nr = 0
    col_nr = 0
    last_row = len(map_of_slope) - 1
    cols = len(map_of_slope[0])

    while col_nr < last_row:
        row_nr += right
        col_nr += down
        if map_of_slope[col_nr][row_nr % cols]:
            trees_hit += 1
    return trees_hit

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

    map_of_slope = [ [x == '#' for x in line.strip()] for line in lines]
    hits = []
    hits.append(nr_of_trees_hit(1, 1, map_of_slope))
    hits.append(nr_of_trees_hit(1, 3, map_of_slope))
    hits.append(nr_of_trees_hit(1, 5, map_of_slope))
    hits.append(nr_of_trees_hit(1, 7, map_of_slope))
    hits.append(nr_of_trees_hit(2, 1, map_of_slope))

    answer = reduce(lambda x, y: x*y, hits)
    print(answer)

if __name__ == "__main__":
    main()
