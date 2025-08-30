"""Advent of Code: 2024.6.1"""
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
    height = len(lines)
    width = len(lines[0])

    lab_map = [ [c for c in line.strip()] for line in lines ]

    # find guard
    guard_row = -1
    guard_col = -1
    for i,line in enumerate(lab_map):
        if '^' in line:
            guard_row = i
            guard_col = line.index('^')
    lab_map[guard_row][guard_col] = 'X'
    
    # Move guard
    direction = "North"
    while 0 <= guard_row < width and 0 <= guard_col < height:
        if direction == "North":
            # Done
            if guard_row - 1 < 0:
                lab_map[guard_row][guard_col] = 'X'
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
                lab_map[guard_row][guard_col] = 'X'
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
                lab_map[guard_row][guard_col] = 'X'
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
                lab_map[guard_row][guard_col] = 'X'
                break
            # Obstacle
            if lab_map[guard_row][guard_col - 1] == '#':
                direction = "North"
                continue
            # Move
            guard_col -= 1
        
        lab_map[guard_row][guard_col] = 'X'
        
    for line in lab_map:
        print("".join(line))
    print(sum( sum( 1 if c == 'X' else 0 for c in line ) for line in lab_map))

if __name__ == "__main__":
    main()
