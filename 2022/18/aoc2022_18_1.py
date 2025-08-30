"""Advent of Code: 2022.18.1"""
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
    cubes = set()
    for line in lines:
        x,y,z = line.strip().split(',')
        cubes.add((int(x),int(y),int(z)))

    total_exposed_sides = 0
    for cube in cubes:
        x,y,z = cube
        exposed_sides = 0
        for side in [(x-1,y,z),(x+1,y,z),(x,y-1,z),(x,y+1,z),(x,y,z-1),(x,y,z+1)]:
            if side not in cubes:
                exposed_sides += 1
        total_exposed_sides += exposed_sides

    print(total_exposed_sides)


if __name__ == "__main__":
    main()
