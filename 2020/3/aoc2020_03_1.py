""" Advent of Code: 2020.3.1

"""
import sys

def nr_of_trees_hit(map_of_slope):
    """ Takes a 2d list of bools, reprecenting tree or no tree."""
    trees_hit = 0
    row_nr = 0
    col_nr = 0
    last_row = len(map_of_slope) - 1
    cols = len(map_of_slope[0])

    while col_nr < last_row:
        row_nr += 3
        col_nr += 1
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
    nr_of_hits = nr_of_trees_hit(map_of_slope)
    print(nr_of_hits)

if __name__ == "__main__":
    main()
