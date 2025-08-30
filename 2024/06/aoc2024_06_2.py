"""Advent of Code: 2024.4.1"""
import sys

# This is a brute force solution. 
# Can optimise 


def loop(lab_map,guard_row,guard_col):
    visited = { (guard_row,guard_col) : ["North"]}
    loop = True

    height = len(lab_map)
    width = len(lab_map[0])

    # Move guard
    direction = "North"
    while 0 <= guard_row < width and 0 <= guard_col < height:
        if direction == "North":
            # Done
            if guard_row - 1 < 0:
                loop = False
                break
            # Obstacle
            if lab_map[guard_row -1][guard_col] == '#':
                direction = "East"
                continue
            # Move
            guard_row -= 1
        
        elif direction == "East":
            # Done
            if guard_col + 1 >= width:
                loop = False
                break
            # Obstacle
            if lab_map[guard_row][guard_col + 1] == '#':
                direction = "South"
                continue
            # Move
            guard_col += 1
        
        elif direction == "South":
            # Done
            if guard_row + 1 >= height:
                loop = False
                break
            # Obstacle
            if lab_map[guard_row + 1][guard_col] == '#':
                direction = "West"
                continue
            # Move
            guard_row += 1
        
        elif direction == "West":
            # Done
            if guard_col - 1 < 0:
                loop = False
                break
            # Obstacle
            if lab_map[guard_row][guard_col - 1] == '#':
                direction = "North"
                continue
            # Move
            guard_col -= 1

        if (guard_row,guard_col) in visited:
            # We have a loop
            if direction in visited[(guard_row,guard_col)]:
                break
            else:
                visited[(guard_row,guard_col)].append(direction)
        else:
            visited[(guard_row,guard_col)] = [direction]
    
    return loop

def initial_path(lab_map,guard_row, guard_col):
    visited = [(guard_row,guard_col)]

    height = len(lab_map)
    width = len(lab_map[0])

    direction = "North"
    while (0 <= guard_row < width and 0 <= guard_col < height):
        if direction == "North":
            # Done
            if guard_row - 1 < 0:
                break
            # Obstacle
            if lab_map[guard_row -1][guard_col] == '#':
                direction = "East"
                continue
            # Move
            guard_row -= 1
        
        elif direction == "East":
            # Done
            if guard_col + 1 >= width:
                break
            # Obstacle
            if lab_map[guard_row][guard_col + 1] == '#':
                direction = "South"
                continue
            # Move
            guard_col += 1
        
        elif direction == "South":
            # Done
            if guard_row + 1 >= height:                
                break
            # Obstacle
            if lab_map[guard_row + 1][guard_col] == '#':
                direction = "West"
                continue
            # Move            
            guard_row += 1
        
        elif direction == "West":
            # Done
            if guard_col - 1 < 0:
                break
            # Obstacle
            if lab_map[guard_row][guard_col - 1] == '#':
                direction = "North"
                continue
            # Move
            guard_col -= 1
        
        visited.append( (guard_row,guard_col) )
    visited.append( (guard_row,guard_col) )

    return set(visited)


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
    height = len(lines)
    width = len(lines[0])

    # Need to store direction and position for every move, if a move return to same position 
    # with in the same direction, we have a loop.
    lab_map = [ [c for c in line.strip()] for line in lines ]

    # find guard
    guard_row = -1
    guard_col = -1
    for i,line in enumerate(lab_map):
        if '^' in line:
            guard_row = i
            guard_col = line.index('^')
    
    # Move guard
    loops = 0
    path = initial_path(lab_map,guard_row,guard_col)
    path.remove((guard_row,guard_col))
    for x,y in path:
        lab_map[x][y] = '#'
        if loop(lab_map,guard_row,guard_col):
            loops += 1
        lab_map[x][y] = '.'
    print(loops)


if __name__ == "__main__":
    main()
