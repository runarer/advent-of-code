"""Advent of Code: 2020.24.1"""
import sys

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

    print(len(black_tiles))

if __name__ == "__main__":
    main()
