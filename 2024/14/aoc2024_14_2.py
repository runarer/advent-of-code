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

    return (x,y,vx,vy)


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
    # robot_positions = [ run(robot,100) for robot in robots]

    blinks = 0
    while True:
        robots = [ run(robot,1) for robot in robots]
        blinks += 1
        robot_positions = [ (x,y) for x,y,_,_ in robots]
        center_robots = [(x,y) for x,y in robot_positions if x == wide//2]
        for x,y in center_robots:
            if (x-1,y+1) in robot_positions and (x+1,y+1) in robot_positions and (x,y+1) in robot_positions:
                for y in range(tall):
                    for x in range(wide):
                        print( 'X' if (x,y) in robot_positions else ' ',end="")
                    print()
                print("o"*wide,blinks)
                input()



    


if __name__ == "__main__":
    main()
