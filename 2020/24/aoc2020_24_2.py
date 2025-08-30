"""Advent of Code: 2020.24.1"""
import sys

def init_state(lines):
    """ Sets the initial state for the tiles. """
    black_tiles = set()

    for line in lines:
        chars = list(line.strip())
        tile_x = 0
        tile_y = 0

        while chars:
            char = chars.pop(0)
            if char == 'e':
                tile_x += 1
            elif char == 'w':
                tile_x -= 1
            elif char == 's':
                char = chars.pop(0)
                if char == 'e':
                    if tile_y % 2 == 0:
                        tile_x += 1
                    tile_y += 1
                else: # char == 'w'
                    if tile_y % 2 == 1:
                        tile_x -= 1
                    tile_y += 1
            elif char == 'n':
                char = chars.pop(0)
                if char == 'e':
                    if tile_y % 2 == 0:
                        tile_x += 1
                    tile_y -= 1
                else: # char == 'w'
                    if tile_y % 2 == 1:
                        tile_x -= 1
                    tile_y -= 1
            else:
                print("OPS")

        tile = (tile_y,tile_x) #Er koordiantene her riktig
        if tile in black_tiles:
            black_tiles.remove(tile)
        else:
            black_tiles.add(tile)

    return black_tiles




def flip_tiles(black_tiles,days):
    """Flipes the tiles according to a rule set. """

    for _ in range(days):
        tiles_to_remove = set()
        tiles_to_add = set()
        white_to_check = set()

        # Find black tiles to flipp
        for tile in black_tiles:
            # find neighbours
            tile_y,tile_x = tile
            adjacent_tiles = [(tile_y,tile_x+1),(tile_y,tile_x-1)] # east,west
            if tile_y % 2 == 0:
                adjacent_tiles.append( (tile_y+1,tile_x  ) ) #southwest
                adjacent_tiles.append( (tile_y+1,tile_x+1) ) #southeast
                adjacent_tiles.append( (tile_y-1,tile_x  ) ) #northwest
                adjacent_tiles.append( (tile_y-1,tile_x+1) ) #northeast
            else:
                adjacent_tiles.append( (tile_y+1,tile_x-1) ) #southwest
                adjacent_tiles.append( (tile_y+1,tile_x  ) ) #southeast
                adjacent_tiles.append( (tile_y-1,tile_x-1) ) #northwest
                adjacent_tiles.append( (tile_y-1,tile_x  ) ) #northeast

            # check if neighbours are black and gather whites to check
            adjacent_black = 0
            for adjacent in adjacent_tiles:
                if adjacent in black_tiles:
                    adjacent_black += 1
                else:
                    white_to_check.add(adjacent)
            if adjacent_black == 0 or adjacent_black > 2:
                tiles_to_remove.add(tile)

        # Find white tiles to flipp
        for tile in white_to_check:
            # find neighbours
            tile_y,tile_x = tile
            adjacent_tiles = [(tile_y,tile_x+1),(tile_y,tile_x-1)] # east,west
            if tile_y % 2 == 0:
                adjacent_tiles.append( (tile_y+1,tile_x  ) ) #southwest
                adjacent_tiles.append( (tile_y+1,tile_x+1) ) #southeast
                adjacent_tiles.append( (tile_y-1,tile_x  ) ) #northwest
                adjacent_tiles.append( (tile_y-1,tile_x+1) ) #northeast
            else:
                adjacent_tiles.append( (tile_y+1,tile_x-1) ) #southwest
                adjacent_tiles.append( (tile_y+1,tile_x  ) ) #southeast
                adjacent_tiles.append( (tile_y-1,tile_x-1) ) #northwest
                adjacent_tiles.append( (tile_y-1,tile_x  ) ) #northeast

            # check if neighbours are black and gather whites to check
            adjacent_black = 0
            for adjacent in adjacent_tiles:
                if adjacent in black_tiles:
                    adjacent_black += 1
            if adjacent_black == 2:
                tiles_to_add.add(tile)

        # Flipp black and white
        black_tiles.difference_update(tiles_to_remove)
        black_tiles.update(tiles_to_add)

def main():
    """Start"""
    #get argument
    if len(sys.argv) < 1:
        sys.exit("Usage: python " + sys.argv[0] + " filename")
    filename = sys.argv[1]
    try:
        with open(filename, 'rt', encoding="utf-8") as file:
            lines = file.readlines()
    except IOError as err:
        print(f"{err}\nError opening {filename}. Terminating program.", file=sys.stderr)
        sys.exit(1)

    black_tiles = init_state(lines)
    flip_tiles(black_tiles,100)

    print(len(black_tiles))

if __name__ == "__main__":
    main()
