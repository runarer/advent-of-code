"""Advent of Code: 2024.20.2

    One thing that's unclear, does the cheat end when reaching the track of 
    can I move across the track and into another wall aslong as I got time left
    to do so?
"""
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

    max_steps = 20
    search_grid = generate_search_grid(max_steps)

    cheats = {}

    # For all cells not a wall (#), these are our starting points for findin cheats
    starting_points = [ (r,c) for r,row in enumerate(steps_to_end) for c,col in enumerate(row) if col != -1 ]

    for start in starting_points:
        row,col = start

        current_steps = steps_to_end[row][col]

        for steps,(d_row, d_col) in search_grid:
            n_row, n_col = row + d_row, col + d_col
            if 0 <= n_row < rows and 0 <= n_col < cols:
                if steps_to_end[n_row][n_col] >= 0:
                    steps_saved = steps_to_end[row][col] - steps - steps_to_end[n_row][n_col]
                            
                    if steps_saved not in cheats:
                        # making this a set did not help, make it a list when solved.
                        cheats[steps_saved] = set()
                    
                    cheats[steps_saved].add((row, col, n_row, n_col))



        # from collections import deque
        
        
        # queue = deque([(start,0)])  # (position, steps)
        # visited = set([start])

        # while queue:
        #     (c_row, c_col), steps = queue.popleft()

        #     if steps_to_end[c_row][c_col] == 0:
        #         steps_saved = steps_to_end[row][col] - steps # -1 since steps already counted the one landed on.
                            
        #         if steps_saved not in cheats:
        #             # making this a set did not help, make it a list when solved.
        #             cheats[steps_saved] = set()
                
        #         cheats[steps_saved].add((row, col, c_row, c_col))

        #     for d_row, d_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        #         n_row, n_col = c_row + d_row, c_col + d_col
        #         if 0 <= n_row < rows and 0 <= n_col < cols and (n_row, n_col) not in visited and steps <= max_steps:
        #             visited.add((n_row, n_col))
        #             if steps_to_end[n_row][n_col] == -1:
        #                 # We can travel some more
        #                 queue.append(((n_row, n_col), steps + 1))
        #             else:
        #                 # We have a new cheat
        #                 if steps_to_end[n_row][n_col] < current_steps: # does not seem to mather if steps are added
        #                     steps_saved = steps_to_end[row][col] - steps - steps_to_end[n_row][n_col] - 1 # -1 since steps already counted the one landed on.
                            
        #                     if steps_saved not in cheats:
        #                         # making this a set did not help, make it a list when solved.
        #                         cheats[steps_saved] = set()
                            
        #                     cheats[steps_saved].add((row, col, n_row, n_col))

        #                     if steps < max_steps:
        #                         queue.append(((n_row, n_col), steps + 1))







        # # one wall cheats
        # for d_row, d_col in [(-2,0),(2,0),(0,-2),(0,2)]:
        #     t_row, t_col = row + d_row, col + d_col

        #     if 0 <= t_row < len(map) and 0 <= t_col < len(map[0]) and steps_to_end[t_row][t_col] != -1:
        #         if steps_to_end[t_row][t_col] < current_steps:
        #             steps_saved = steps_to_end[row][col] - 2 - steps_to_end[t_row][t_col]
                    
        #             if steps_saved not in cheats:
        #                 cheats[steps_saved] = []
                    
        #             cheats[steps_saved].append((row, col, t_row, t_col))


    for steps_saved in sorted(cheats.keys()):
        print(f"There are {len(cheats[steps_saved])} cheats that save {steps_saved} picoseconds.")


    # for row in map:
    #     print(''.join(row))

    # for row in steps_to_end:
    #     print(' '.join(f"{cell:3}" for cell in row))

    sum_cheats = sum( len(cheats[s]) for s in cheats.keys() if s >= 100 )
    print(f"Part 1: {sum_cheats}")

    # print(search_grid)

if __name__ == "__main__":
    main()
