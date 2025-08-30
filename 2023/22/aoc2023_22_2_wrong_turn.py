"""Advent of Code: 2019.1.1"""
import sys
from dataclasses import dataclass
from collections import deque

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

def drop_bricks(bricks : list[SandBrick]) -> (dict[SandBrick,set[SandBrick]], dict[SandBrick,set[SandBrick]]):
    bricks_below : dict[SandBrick,set[SandBrick]] = { bricks[0] : {None} }
    bricks_above : dict[SandBrick,set[SandBrick]] = { bricks[0] : set() }

    lowest_bricks = [ [bricks[0]]*(bricks[0].second.x+1) for _ in range(bricks[0].second.y+1) ]

    for brick in bricks[1:]:
        below : set[SandBrick] = set()
        highest_z = 0

        for x in range(brick.first.x,brick.second.x+1):
            for y in range(brick.first.y,brick.second.y+1):
                if lowest_bricks[y][x].second.z > highest_z:
                    highest_z = lowest_bricks[y][x].second.z
                    below.clear()
                    below.add(lowest_bricks[y][x])
                elif lowest_bricks[y][x].second.z == highest_z:
                    below.add(lowest_bricks[y][x])

        brick.second.z = (brick.second.z - brick.first.z) + highest_z + 1
        brick.first.z = highest_z + 1

        for x in range(brick.first.x,brick.second.x+1):
            for y in range(brick.first.y,brick.second.y+1):
                lowest_bricks[y][x] = brick

        bricks_below[brick] = below
        bricks_above[brick] = set()

        for brick_below in bricks_below[brick]:
            bricks_above[brick_below].add(brick)

    return (bricks_below, bricks_above)

def count_removable_bricks(bricks,bricks_below,bricks_above) -> int:
    removable_bricks = 0
    for brick in bricks[1:]:
        # If now brick above, remove
        if len(bricks_above[brick]) == 0:
            removable_bricks += 1
            continue

        # If brick above got more than one brick below, remove.
        removable = True
        for brick_above in bricks_above[brick]:
            if len(bricks_below[brick_above]) == 1:
                removable = False
        if removable:
            removable_bricks += 1

    return removable_bricks

def find_best_brick(bricks,bricks_below,bricks_above) -> int:
    highest_destruction = 0

    for i,brick in enumerate(bricks[1:]):
        destroyed_bricks = {brick}
        bricks_just_destroyed = deque([brick])

        while bricks_just_destroyed:
            destroyed = bricks_just_destroyed.popleft()

            for brick_above in bricks_above[destroyed]:
                #can_be_destroyed = True
                for supporting_brick in bricks_below[brick_above]:
                    if supporting_brick not in destroyed_bricks:
                        #can_be_destroyed = False
                        break
                else:
                    bricks_just_destroyed.append(brick_above)
                    destroyed_bricks.add(brick_above)
        highest_destruction = max(highest_destruction,len(destroyed_bricks))
        print(i)

    return highest_destruction

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

    bricks_below, bricks_above = drop_bricks(bricks)

    bricks_destroyed = find_best_brick(bricks,bricks_below,bricks_above)

    print(bricks_destroyed)

if __name__ == "__main__":
    main()
