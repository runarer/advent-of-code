"""Advent of Code: 2024.15.1"""
import sys

direction_moves = {'^':(-1,0),'>':(0,1),'v':(1,0), '<':(0,-1)}

def print_warehouse(warehouse):
    for line in warehouse:
        print("".join(line))

def find_starting_point(warehouse):
    for row, line in enumerate(warehouse):
        if '@' in line:
            return (row,line.index('@'))
    return (0,0)

def move(warehouse,block,direction):
    move_to_row = block[0] + direction_moves[direction][0]
    move_to_col = block[1] + direction_moves[direction][1]
    
    if warehouse[move_to_row][move_to_col] == 'O':
        if not move(warehouse,(move_to_row,move_to_col),direction):
            return False
    elif warehouse[move_to_row][move_to_col] == '#':
        return False
    
    warehouse[move_to_row][move_to_col] = warehouse[block[0]][block[1]]
    warehouse[block[0]][block[1]] = '.'
    
    return True
    
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

    warehouse = []
    moves = ""
    read_moves = False
    
    for line in lines:
        line = line.strip()
        if not line:
            read_moves = True
            continue

        if read_moves:
            moves += line            
        else:
            warehouse.append( list(line) )
            pass

    # Find starting point
    start = find_starting_point(warehouse)

    for m in moves:
        if move(warehouse,start,m):
            start = (start[0] + direction_moves[m][0],start[1]+direction_moves[m][1])
    
    print(sum ( sum(row*100+col for col,c in enumerate(line) if c == 'O') for row,line in enumerate(warehouse) ))


if __name__ == "__main__":
    main()
