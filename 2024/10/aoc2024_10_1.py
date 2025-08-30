"""Advent of Code: 2024.10.1"""
import sys
from itertools import chain

def find_tops(trail_map, starting_point):
    height = len(trail_map)
    width = len(trail_map[0])
    
    tops = 0

    visited = [starting_point]
    while visited:
        row,col = visited.pop(0)
        cur = trail_map[row][col]
        if cur == 9:
            tops += 1
            continue
        
        # North
        if row-1 >= 0 and trail_map[row-1][col] == cur+1:            
            new_point = (row-1,col)
            if new_point not in visited:
                visited.append(new_point)

        # East
        if col+1 < width and trail_map[row][col+1] == cur+1:
            new_point = (row,col+1)
            if new_point not in visited:
                visited.append(new_point)

        # South
        if row+1 < height and trail_map[row+1][col] == cur+1:
            new_point = (row+1,col)
            if new_point not in visited:
                visited.append(new_point)

        # West
        if col-1 >= 0 and trail_map[row][col-1] == cur+1:
            new_point = (row,col-1)
            if new_point not in visited:
                visited.append(new_point)

    return tops


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
    trail_map = [ [ int(c) for c in line.strip() ] for line in lines]
    starting_points = list(chain(*[ [ (r,c) for c,v in enumerate(l) if v == 0 ] for r,l in enumerate(trail_map)]))
        
    print(sum( find_tops(trail_map,sp) for sp in starting_points))


if __name__ == "__main__":
    main()