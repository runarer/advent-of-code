"""Advent of Code: 2024.20.1"""
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
    map = [ list(line.strip()) for line in lines]

    # find the starting and ending positions
    start = (0,0)
    end = (0,0)
    for row in range(len(map)):
        for col in range(len(map[row])):
            if map[row][col] == 'S':
                start = (row,col)
            elif map[row][col] == 'E':
                end = (row,col)
            if start != (0,0) and end != (0,0):
                break

    # create a 2D array of steps to reach the end from each cell. 
    # Initialize with -1 for walls and a large number for open cells.
    steps_to_end = [ [-1]*len(map[0]) for _ in range(len(map))]
    for row in range(len(map)):
        for col in range(len(map[row])):
            if map[row][col] != '#':
                steps_to_end[row][col] = 100_000_000
    steps_to_end[end[0]][end[1]] = 0

    next = end
    while next != start:
        row, col = next
        current_steps = steps_to_end[row][col]
        # check neighbors
        for d_row, d_col in [(-1,0),(1,0),(0,-1),(0,1)]:
            n_row, n_col = row + d_row, col + d_col
            # make sure we are inside the map
            if 0 <= n_row < len(map) and 0 <= n_col < len(map[0]):
                # is a wall
                if steps_to_end[n_row][n_col] == -1:
                    continue
                # since it's a single path next will be the neighbor with a higher step count.
                if steps_to_end[n_row][n_col] > current_steps:
                    steps_to_end[n_row][n_col] = current_steps + 1
                    next = (n_row, n_col)
                    break

    # for row in map:
    #     print(''.join(row))

    # for row in steps_to_end:
    #     print(' '.join(f"{cell:3}" for cell in row))

    # print(f"Start: {start}, End: {end}")

if __name__ == "__main__":
    main()
