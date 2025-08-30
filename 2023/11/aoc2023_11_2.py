"""Advent of Code: 2019.1.1"""
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
    lines = [list(line.strip()) for line in lines]
    new_rows = [ i for i,line in enumerate(lines) if '#' not in line]
    new_cols = [ i for i,_ in enumerate(lines[0]) if not any(l[i] == "#" for l in lines) ]

    galaxies = []
    for j,line in enumerate(lines):
        for i,c in enumerate(line):
            if c == '#':
                galaxies.append((j,i))

    sum_of_shortest_dist = 0
    for i,gal in enumerate(galaxies[:-1]):
        for n_gal in galaxies[i+1:]:
            min_row = min(gal[0],n_gal[0])
            max_row = max(gal[0],n_gal[0])
            min_col = min(gal[1],n_gal[1])
            max_col = max(gal[1],n_gal[1])
            empty_rows = sum( 1 for i in new_rows if min_row < i <max_row )
            empty_cols = sum( 1 for i in new_cols if min_col < i <max_col )

            sum_of_shortest_dist += sum( (max_row-min_row, max_col-min_col)) \
                                    + (empty_rows + empty_cols)*(1000000-1)

    print(sum_of_shortest_dist)


if __name__ == "__main__":
    main()
