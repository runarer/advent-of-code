from http.client import MOVED_PERMANENTLY
import sys

def move_east(seafloor_map) -> int:
    """Tested and working"""

    moved = False
    for line in seafloor_map:

        move_last = False
        if line[0] == '.' and line[-1] == '>':
            move_last = True

        moved_last_iteration = False
        for i in range(len(line)-1):
            if moved_last_iteration:
                moved_last_iteration = False                
                continue
            if line[i] == '>' and line[i+1] == '.':
                moved_last_iteration = True
                moved = True
                line[i] = '.'
                line[i+1] = '>'
        
        if move_last:
            moved = True
            line[0] = '>'
            line[-1] = '.'

    return moved

def move_south(seafloor_map) -> bool:
    """Tested and working"""

    moved = False

    for i in range(len(seafloor_map[0])):

        move_last = False
        if seafloor_map[0][i] == '.' and seafloor_map[-1][i] == 'v':
            move_last = True

        moved_last_iteration = False
        for j in range(len(seafloor_map)-1):
            if moved_last_iteration:
                moved_last_iteration = False
                continue
            if seafloor_map[j][i] == 'v' and seafloor_map[j+1][i] == '.':
                moved_last_iteration = True
                moved = True
                seafloor_map[j][i] = '.'
                seafloor_map[j+1][i] = 'v'

        if move_last:
            moved = True
            seafloor_map[0][i] = 'v'
            seafloor_map[-1][i] = '.'

    return moved

def do_steps(seafloor_map) -> int:
    """Return number of steps for the seacucumbers to stop moving."""

    steps  = 0
    while True:
        steps += 1

        moved_east = move_east(seafloor_map)
        moved_south = move_south(seafloor_map)

        if not moved_south and not moved_east:
            break

    return steps

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

    #seafloor_map = [[char for char in line.strip()] for line in lines]
    seafloor_map = [list(line.strip()) for line in lines]
    steps = do_steps(seafloor_map)
    # print("-------------------------------- MOVING EAST ---------------------------------")
    # #steps = move_east(seafloor_map)
    # steps = move_east(seafloor_map)
    # for line in seafloor_map:
    #     print("".join(line))

    # print("-------------------------------- MOVING South ---------------------------------")
    # steps = move_south(seafloor_map)
    # #steps = move_south(seafloor_map)
    for line in seafloor_map:
        print("".join(line))


    print("The seacucumbers stop moving in:",steps)



if __name__ == "__main__":
    main()
