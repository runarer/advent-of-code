"""Advent of Code: 2019.1.1"""
import sys

def energized_tiles(square_grid,start):
    square_w = len(square_grid[0])
    square_h = len(square_grid)

    visited = [ [ [] for _ in line ] for line in square_grid ]

    next_beam = [start]

    while next_beam:
        current_beam = next_beam.pop()

        current_line = current_beam[0]
        current_row = current_beam[1]
        current_direction = current_beam[2]

        # Option 1, depth first with recurcive, or without
        # Option 2, breath first.

        while (-1 < current_line < square_h) and (-1 < current_row < square_w):
            # Check for previous visits in same direction
            if current_direction in visited[current_line][current_row]:
                break
            visited[current_line][current_row].append(current_direction)

            # Check for splitters
            if square_grid[current_line][current_row] == '-' and current_direction in "NS":
                # add on beam to next_beam
                next_beam.append((current_line,current_row-1,'W'))

                # and continue with the other one.
                current_row += 1
                current_direction = 'E'
                continue

            if square_grid[current_line][current_row] == '|' and current_direction in "EW":                
                # add on beam to next_beam
                next_beam.append((current_line-1,current_row,'N'))

                # and continue with the other one.
                current_line += 1
                current_direction = 'S'                
                continue

            # Check for mirrors, change directions
            if square_grid[current_line][current_row] == '/':
                if current_direction == 'N':
                    current_direction = 'E'
                    current_row += 1
                elif current_direction == 'E':
                    current_direction = 'N'
                    current_line -= 1
                elif current_direction == 'S':
                    current_direction = 'W'
                    current_row -= 1
                elif current_direction == 'W':
                    current_direction = 'S'
                    current_line += 1
                else:
                    print("Wrong in /")                
                continue
            if square_grid[current_line][current_row] == '\\':
                if current_direction == 'N':
                    current_direction = 'W'
                    current_row -= 1
                elif current_direction == 'E':
                    current_direction = 'S'
                    current_line += 1
                elif current_direction == 'S':
                    current_direction = 'E'
                    current_row += 1
                elif current_direction == 'W':
                    current_direction = 'N'
                    current_line -= 1
                else:
                    print("Wrong in \\")
                continue

            # Open space
            if current_direction == 'N':
                current_line -= 1
            elif current_direction == 'E':
                current_row += 1
            elif current_direction == 'S':
                current_line += 1
            elif current_direction == 'W':
                current_row -= 1
            else:
                print("Wrong in last")
    
    return sum( sum( 1 for c in line if c) for line in visited)

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

    square_grid = [ list(line.strip()) for line in lines]

    largest_energy = 0
    sq_w = len(square_grid[0])
    sq_h = len(square_grid)
    for i in range(sq_h):
        largest_energy = max(largest_energy,energized_tiles(square_grid,(i,0,'E')))
        largest_energy = max(largest_energy,energized_tiles(square_grid,(i,sq_w-1,'W')))
    for i in range(sq_w):
        largest_energy = max(largest_energy,energized_tiles(square_grid,(0,i,'S')))
        largest_energy = max(largest_energy,energized_tiles(square_grid,(sq_h-1,0,'N')))
    print(largest_energy)
    # Kunne gjort en endring der for hver /\-| som treffes i en retning så lagrer man 

if __name__ == "__main__":
    main()