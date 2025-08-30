"""Advent of Code: 2024.10.1"""
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
    droped_bytes = [ tuple(map(int,line.strip().split(','))) for line in lines ]
    target_x = 7
    target_y = 7
    # memory = [ [ '#' if (x,y) in droped_bytes else '.' for x in range(memory_width)] for y in range(memory_height) ]
    memory = [ [ '#' if (x,y) in droped_bytes[:12] else '.' for x in range(target_x)] for y in range(target_y) ]

    for line in memory:
        print("".join(line))
    
    
if __name__ == "__main__":
    main()
