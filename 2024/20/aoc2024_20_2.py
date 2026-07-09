"""Advent of Code: 2024.20.2"""
import sys

# 
def generate_search_grid(cells_outwards):
    search_grid = set()

    for x in range(cells_outwards+1):
        for y in range(cells_outwards+1 - x):
            search_grid.add((x+y,(-1*x,y)))
            search_grid.add((x+y,(-1*x,-1*y)))
            search_grid.add((x+y,(x,y)))
            search_grid.add((x+y,(x,-1*y)))

    search_grid.remove((0,(0,0)))

    return search_grid

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
    rows = len(map)
    cols = len(map[0])

    # find the starting and ending positions
    start = (0,0)
    end = (0,0)
    for row in range(rows):
        for col in range(cols):
            if map[row][col] == 'S':
                start = (row,col)
            elif map[row][col] == 'E':
                end = (row,col)
            if start != (0,0) and end != (0,0):
                break

    # create a 2D array of steps to reach the end from each cell. 
    # Initialize with -1 for walls and a large number for open cells.
    steps_to_end = [ [-1]*cols for _ in range(rows)]
    for row in range(rows):
        for col in range(cols):
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
            if 0 <= n_row < rows and 0 <= n_col < cols:
                # is a wall
                if steps_to_end[n_row][n_col] == -1:
                    continue
                # since it's a single path next will be the neighbor with a higher step count.
                if steps_to_end[n_row][n_col] > current_steps:
                    steps_to_end[n_row][n_col] = current_steps + 1
                    next = (n_row, n_col)
                    break

    # Part 2 solution, can solve part 1 by setting max_steps to 2
    max_steps = 20
    search_grid = generate_search_grid(max_steps)

    cheats = {}

    # For all cells not a wall (#), these are our starting points for findin cheats
    starting_points = [ (r,c) for r,row in enumerate(steps_to_end) for c,col in enumerate(row) if col != -1 ]

    for start in starting_points:
        row,col = start

        current_steps = steps_to_end[row][col]

        # we look through the search grid and each non wall that's closer to the end
        # is considered a cheat.
        for steps,(d_row, d_col) in search_grid:
            n_row, n_col = row + d_row, col + d_col
            if 0 <= n_row < rows and 0 <= n_col < cols:
                if steps_to_end[n_row][n_col] >= 0:
                    steps_saved = steps_to_end[row][col] - steps - steps_to_end[n_row][n_col]
                            
                    if steps_saved not in cheats:
                        cheats[steps_saved] = []
                    
                    cheats[steps_saved].append((row, col, n_row, n_col))

    # for steps_saved in sorted(cheats.keys()):
    #     print(f"There are {len(cheats[steps_saved])} cheats that save {steps_saved} picoseconds.")

    sum_cheats = sum( len(cheats[s]) for s in cheats.keys() if s >= 100 )
    print(f"Part 2: {sum_cheats}")


if __name__ == "__main__":
    main()
