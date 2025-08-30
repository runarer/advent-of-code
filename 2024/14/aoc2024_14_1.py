"""Advent of Code: 2024.14.1"""
    
import sys,re

wide = 101
tall = 103

def run(position,seconds):
    x,y,vx,vy = position

    for i in range(1,seconds+1):
        x += vx
        x %= wide
        y += vy
        y %= tall

    return (x,y)


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
    robot_positions = [ run(robot,100) for robot in robots]
    # print(robot_positions)
    # print(wide//2)
    # print(tall//2)


    first_quadrant = sum( 1 if x < wide//2 and y < tall//2 else 0 for x,y in robot_positions)
    second_quadrant = sum( 1 if x > wide//2 and y < tall//2 else 0 for x,y in robot_positions)
    third_quadrant = sum( 1 if x > wide//2 and y > tall//2 else 0 for x,y in robot_positions)
    forth_quadrant = sum( 1 if x < wide//2 and y > tall//2 else 0 for x,y in robot_positions)
    # print(first_quadrant)
    # print(second_quadrant)
    # print(third_quadrant)
    # print(forth_quadrant)
    print(first_quadrant*second_quadrant*third_quadrant*forth_quadrant)

    


if __name__ == "__main__":
    main()

# 230582440, to low