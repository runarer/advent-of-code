"""
    Advent of Code: 2019.1.1
    

    For each brick, remove it from the list and re-drop the bricks
"""
import sys
from dataclasses import dataclass
from copy import deepcopy

@dataclass
class Point:
    x : int
    y : int
    z : int

@dataclass
class SandBrick:
    first : Point
    second : Point

    def __hash__(self):
        return hash(str(self))

def new_sandblock(line:str) -> SandBrick:
    first,second = line.strip().split('~')

    first_point = Point(*map(int,first.split(',')))
    second_point = Point(*map(int,second.split(',')))

    sand_brick = SandBrick( first_point , second_point )

    return sand_brick

def calc_bottom(bricks : list[SandBrick]) -> SandBrick:
    max_brick_x = max( max(b.first.x,b.second.x) for b in bricks)
    max_brick_y = max( max(b.first.y,b.second.y) for b in bricks)

    return SandBrick(Point(0,0,0),Point(max_brick_x,max_brick_y,0))

def drop_bricks(bricks : list[SandBrick]) -> int:
    lowest_bricks = [ [bricks[0]]*(bricks[0].second.x+1) for _ in range(bricks[0].second.y+1) ]

    bricks_that_fell = 0

    for brick in bricks[1:]:
        highest_z = 0

        old_z = brick.first.z

        for x in range(brick.first.x,brick.second.x+1):
            for y in range(brick.first.y,brick.second.y+1):
                if lowest_bricks[y][x].second.z > highest_z:
                    highest_z = lowest_bricks[y][x].second.z

        brick.second.z = (brick.second.z - brick.first.z) + highest_z + 1
        brick.first.z = highest_z + 1

        if old_z > brick.first.z:
            bricks_that_fell += 1

        for x in range(brick.first.x,brick.second.x+1):
            for y in range(brick.first.y,brick.second.y+1):
                lowest_bricks[y][x] = brick

    return bricks_that_fell

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
    bricks : list[SandBrick] = [new_sandblock(line) for line in lines]

    bottom_brick = calc_bottom(bricks)    
    bricks.append(bottom_brick)
    bricks.sort(key=lambda x : x.first.z)

    _ = drop_bricks(bricks)

    sum_of_other_bricks : int  = 0
    for brick in bricks[1:]:
        new_bricks = deepcopy(bricks)
        new_bricks.remove(brick)
        bricks_dropped = drop_bricks(new_bricks)
        print(bricks_dropped)
        sum_of_other_bricks += bricks_dropped
    print(sum_of_other_bricks)

if __name__ == "__main__":
    main()
