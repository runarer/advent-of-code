"""Advent of Code: 2024.4.2"""
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
    height = len(lines)
    width = len(lines[0])-1    

    xmas = 0
    for row in range(1,height-1):
        for col in range(1,width-1):
            if lines[row][col] == 'A':
                if lines[row-1][col-1] == 'M' and lines[row+1][col+1] == 'S':
                    if (lines[row+1][col-1] == 'M' and lines[row-1][col+1] == 'S') or (lines[row+1][col-1] == 'S' and lines[row-1][col+1] == 'M'):
                        xmas += 1 
                if lines[row-1][col-1] == 'S' and lines[row+1][col+1] == 'M':
                    if (lines[row+1][col-1] == 'M' and lines[row-1][col+1] == 'S') or (lines[row+1][col-1] == 'S' and lines[row-1][col+1] == 'M'):
                        xmas += 1 
    
    print(xmas)


if __name__ == "__main__":
    main()
