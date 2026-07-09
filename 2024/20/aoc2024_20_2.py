"""Advent of Code: 2024.20.2

    One thing that's unclear, does the cheat end when reaching the track of 
    can I move across the track and into another wall aslong as I got time left
    to do so?
"""
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

    cheats = {}

    max_steps = steps_to_end[start[0]][start[1]]

    # For all cells not a wall (-1), we will check a radius of 2 cells in each direction to 
    # see if we can find a shorter path to the end.
    for row in range(len(map)):
        for col in range(len(map[row])):
            if steps_to_end[row][col] == -1:
                continue
            current_steps = steps_to_end[row][col]
            
            # one wall cheats
            for d_row, d_col in [(-2,0),(2,0),(0,-2),(0,2)]:
                t_row, t_col = row + d_row, col + d_col

                if 0 <= t_row < len(map) and 0 <= t_col < len(map[0]) and steps_to_end[t_row][t_col] != -1:
                    if steps_to_end[t_row][t_col] < current_steps:
                        steps_saved = steps_to_end[row][col] - 2 - steps_to_end[t_row][t_col]
                        
                        if steps_saved not in cheats:
                            cheats[steps_saved] = []
                        
                        cheats[steps_saved].append((row, col, t_row, t_col))


    # for steps_saved in sorted(cheats.keys()):
    #     print(f"There are {len(cheats[steps_saved])} cheats that save {steps_saved} picoseconds.")


    # for row in map:
    #     print(''.join(row))

    # for row in steps_to_end:
    #     print(' '.join(f"{cell:3}" for cell in row))

    sum_cheats = sum( len(cheats[s]) for s in cheats.keys() if s >= 100 )
    print(f"Part 1: {sum_cheats}")

if __name__ == "__main__":
    main()
