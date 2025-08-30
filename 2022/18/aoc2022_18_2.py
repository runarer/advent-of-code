"""Advent of Code: 2022.18.2"""
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
    max_x = 0
    max_y = 0
    max_z = 0
    min_x = 100
    min_y = 100
    min_z = 100

    for line in lines:
        x,y,z = list(map(int,line.strip().split(',')))
        max_x = max(max_x,x)
        max_y = max(max_y,y)
        max_z = max(max_z,z)
        min_x = min(min_x,x)
        min_y = min(min_y,y)
        min_z = min(min_z,z)
        cubes.add((x,y,z))

    # Generate all potensial air boubles
    all_cubes = {(x,y,z) for x in range(min_x+1,max_x) for y in range(min_y+1,max_y) for z in range(min_z+1,max_z)}    
    all_air_cubes = all_cubes.difference(cubes)

    air_pockets = set()
    while all_air_cubes:
        air_cube = all_air_cubes.pop()

        new_air_pocket = set()
        air_cubes_to_check = set()
        air_cubes_to_check.add(air_cube)

        an_airpocket = True
        while air_cubes_to_check:
            air_cube_to_check = air_cubes_to_check.pop()
            x,y,z = air_cube_to_check

            for side in [(x-1,y,z),(x+1,y,z),(x,y-1,z),(x,y+1,z),(x,y,z-1),(x,y,z+1)]:
                # Allready checked it
                if side in new_air_pocket:
                    continue
                # it is lava
                if side in cubes:
                    continue
                # To be checked
                if side in air_cubes_to_check:
                    continue
                # It is air, check it
                if side in all_air_cubes:
                    air_cubes_to_check.add(side)
                    all_air_cubes.remove(side)
                # The coordinate is outside, trow away all air cubes
                else:
                    an_airpocket = False
            new_air_pocket.add(air_cube_to_check)

        if an_airpocket:
            air_pockets = air_pockets.union(new_air_pocket)

    total_exposed_sides = 0
    for cube in cubes:
        x,y,z = cube
        exposed_sides = 0
        for side in [(x-1,y,z),(x+1,y,z),(x,y-1,z),(x,y+1,z),(x,y,z-1),(x,y,z+1)]:
            if side in cubes:
                continue
            if side in air_pockets:
                continue
            exposed_sides += 1

        total_exposed_sides += exposed_sides

    print(total_exposed_sides)



# 3188 to high
# There can be lava inside the air pockets



if __name__ == "__main__":
    main()


#### Dette fungerte ikke da vi kan ha luft med lava rundt, der lavablokkene ikke er sammen.

# Kan grupperer alle blokker som tilhører en dråpe.
# Lag en kopi av hele settet.
# 1. Start med en blokk, lag et set med denne blokken; 'to_check'
# 2. Lag et tomt set; 'drop'
# 3. Undersøk om det er noen i nærheten, legg dem til i 'to_check'.
# 4. Legg til blokken i visited.
# 

    # all_cubes = cubes.copy()
    # drops = []
    # while all_cubes:        
    #     cube = all_cubes.pop()

    #     new_drop = set()
    #     cubes_to_check = set()
    #     cubes_to_check.add(cube)

    #     while cubes_to_check:
    #         cube_to_check = cubes_to_check.pop()
    #         x,y,z = cube_to_check
    #         for side in [(x-1,y,z),(x+1,y,z),(x,y-1,z),(x,y+1,z),(x,y,z-1),(x,y,z+1)]:
    #             if side in new_drop:
    #                 continue
    #             if side in all_cubes:
    #                 cubes_to_check.add(side)
    #                 all_cubes.remove(side)
    #         new_drop.add(cube_to_check)
    #     drops.append(new_drop) #Copy?

    # print(drops)