"""Advent of Code: 2019.1.1"""
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
    lines = [line.strip().split(" -> ") for line in lines]

    stone_walls = set()
    sand_settled =  0
    last_before_bottom = 0

    for line in lines:
        for i in range(len(line)-1):
            x1,y1 = list(map(int,line[i].split(',')))
            x2,y2 = list(map(int,line[i+1].split(',')))
            #print("From",x1,y1,"To",x2,y2)
            last_before_bottom = max(last_before_bottom,y1,y2)
            
            # Vertical line
            if x1 == x2:
                for stone in range(min(y1,y2),max(y1,y2)+1):
                    stone_walls.add((x1,stone))
            else:
                for stone in range(min(x1,x2),max(x1,x2)+1):
                    stone_walls.add((stone,y1))

    floor = last_before_bottom + 2

    sand_stopps_falling = False

    while not sand_stopps_falling:
        # Drop new sand
        falling_sand_x = 500
        falling_sand_y = 0
        while True:
            # Fall into abyss
            if falling_sand_y + 1 == floor:
                stone_walls.add((falling_sand_x,falling_sand_y))
                sand_settled += 1
                break
            
            # Fall down
            if (falling_sand_x,falling_sand_y+1) not in stone_walls:
                falling_sand_y += 1
                continue

            # Fall left

            if (falling_sand_x-1,falling_sand_y+1) not in stone_walls:
                falling_sand_x -= 1
                falling_sand_y += 1
                continue

            # Fall right
            if (falling_sand_x+1,falling_sand_y+1) not in stone_walls:
                falling_sand_x += 1
                falling_sand_y += 1
                continue

            # Settle
            if falling_sand_y == 0:
                sand_stopps_falling = True
                sand_settled += 1
            else:
                stone_walls.add((falling_sand_x,falling_sand_y))
                sand_settled += 1
            break
    print(sand_settled)

if __name__ == "__main__":
    main()
