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

    for line in lines:
        for i in new_cols[::-1]:
            line.insert(i,'.')

    for i in new_rows[::-1]:
        lines.insert(i,lines[new_rows[0]])

    galaxies = []
    for j,line in enumerate(lines):
        for i,c in enumerate(line):
            if c == '#':
                galaxies.append((j,i))
    #print(galaxies)

    sum_of_shortest_dist = 0
    for i,gal in enumerate(galaxies):
        for n_gal in galaxies[i:]:
            sum_of_shortest_dist += sum( (max(gal[0],n_gal[0])-min(gal[0],n_gal[0]),\
                                          max(gal[1],n_gal[1])-min(gal[1],n_gal[1])))

    print(sum_of_shortest_dist)


if __name__ == "__main__":
    main()
