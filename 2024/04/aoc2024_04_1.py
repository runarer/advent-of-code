"""Advent of Code: 2024.4.1"""
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
    width = len(lines[0])

    xmas = 0
    for row in range(height):
        for col in range(width):               
            if lines[row][col] == 'X':
                print(row,col)  
                # Check east
                if width - col > 3 and lines[row][col+1] == 'M' and lines[row][col+2] == 'A' and lines[row][col+3] == 'S':
                    xmas += 1
                    print("East",row,col)
                
                # Check south east
                if width - col > 3 and height - row > 3 and lines[row+1][col+1] == 'M' and lines[row+2][col+2] == 'A' and lines[row+3][col+3] == 'S':
                    xmas += 1
                    print("South East",row,col)
                
                # Check south
                if height - row > 3 and lines[row+1][col] == 'M' and lines[row+2][col] == 'A' and lines[row+3][col] == 'S':
                    xmas += 1
                    print("South",row,col)

                # Check south east
                if col >= 3 and height - row > 3 and lines[row+1][col-1] == 'M' and lines[row+2][col-2] == 'A' and lines[row+3][col-3] == 'S':
                    xmas += 1
                    print("South West",row,col)

                # Check east
                if col >= 3 and lines[row][col-1] == 'M' and lines[row][col-2] == 'A' and lines[row][col-3] == 'S':
                    xmas += 1
                    print("West",row,col)

                # Check north west
                if col >= 3 and row >= 3 and lines[row-1][col-1] == 'M' and lines[row-2][col-2] == 'A' and lines[row-3][col-3] == 'S':
                    xmas += 1
                    print("North East",row,col)

                # Check north
                if row >= 3 and lines[row-1][col] == 'M' and lines[row-2][col] == 'A' and lines[row-3][col] == 'S':
                    xmas += 1
                    print("North",row,col)

                # Check north east
                if width - col > 3 and row >= 3 and lines[row-1][col+1] == 'M' and lines[row-2][col+2] == 'A' and lines[row-3][col+3] == 'S':
                    xmas += 1
                    print("North West",row,col)
    print(xmas)


if __name__ == "__main__":
    main()
