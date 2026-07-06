"""Advent of Code: 2024.14.1"""
import sys,re

wide = 101
tall = 103

# Må endre til oppdatere en liste med posisjoner.
def step(robots,grid):
    for robot in robots:
        grid[robot[1]][robot[0]] = ' '

        robot[0] += robot[2]
        robot[0] %= wide
        robot[1] += robot[3]
        robot[1] %= tall

        grid[robot[1]][robot[0]] = 'X'


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
    robots = [list(map(int,re.findall(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)",line)[0])) for line in lines]
    grid = [[' ' for _ in range(wide)] for _ in range(tall)]

    steps = 0
    run = True
    while run:
        step(robots,grid)
        steps += 1

        # check all robots for neighbors, if we have clustered robots
        # print grid, steps and ask for input to continue
        score = 0

        for robot in robots:
            x,y = robot[0],robot[1]
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx,ny = (x+dx)%wide,(y+dy)%tall
                    if grid[ny][nx] == 'X':
                        score += 1

        # this was enough to get right answer.
        if score > 1000:
            print("Score:",score,"Steps:",steps)
            for y in range(tall):
                for x in range(wide):
                    print(grid[y][x],end="")
                print()
            input()

if __name__ == "__main__":
    main()
