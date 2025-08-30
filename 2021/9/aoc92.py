import sys
from functools import reduce

def find_size_of_basins(h_map):
    def find_basin(x,y):
        if h_map[x][y] == '9' or h_map[x][y] == 'X':
            return 0
        h_map[x][y] = 'X'
        return find_basin(x,y+1) + find_basin(x,y-1) + find_basin(x+1,y) + find_basin(x-1,y) + 1

    size_of_basins = []
    for x in range(len(h_map)-2):
        for y in range(len(h_map)-2):
            if h_map[x][y] != '9' or h_map[x][y] == 'X':
                basin_size = find_basin(x,y)
                if basin_size > 0:
                    size_of_basins.append(basin_size)

    return size_of_basins


def main():
    """Start"""
    #get argument
    if len(sys.argv) < 1:
        sys.exit("Usage: python " + sys.argv[0] + " filename")
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except IOError as err:
        print("{}\nError opening {}. Terminating program.".format(err, filename), file=sys.stderr)
        sys.exit(1)
    #Make border of 'X's
    height_map = [['X' for _ in range(len(lines)+2)]]
    height_map += [['X'] + list(line.strip()) + ['X'] for line in lines]
    height_map.append(['X' for _ in range(len(lines)+2)])
    large_basins = find_size_of_basins(height_map)
    large_basins.sort()
    prod_large_basins = reduce((lambda x ,y : x *y), large_basins[-3:])
    print(prod_large_basins)

if __name__ == "__main__":
    main()
