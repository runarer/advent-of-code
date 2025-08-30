"""Advent of Code: 2024.15.1"""
import sys
from itertools import chain

direction_moves = {'^':(-1,0),'>':(0,1),'v':(1,0), '<':(0,-1)}
new_blocks = {'O':"[]",'#':"##",'.':"..",'@':"@."}

def print_warehouse(warehouse):
    for line in warehouse:
        print("".join(line))

def find_starting_point(warehouse):
    for row, line in enumerate(warehouse):
        if '@' in line:
            return (row,line.index('@'))
    return (0,0)

def move_blocks(warehouse,blocks,direction):
    blocks_to_move = set()
    
    for block in blocks:
        row,col = block
        to_row = row + direction_moves[direction][0]
        to_col = col + direction_moves[direction][1]
        
        if warehouse[to_row][to_col] == '#':            
            return False
        
        if warehouse[to_row][to_col] == '.':
            # we can move
            continue       

        if warehouse[row][col] == '[' and warehouse[to_row][to_col] == ']':
            blocks_to_move.add((to_row,to_col-1))
            blocks_to_move.add((to_row,to_col))
        elif warehouse[row][col] == ']' and warehouse[to_row][to_col] == '[':
            blocks_to_move.add((to_row,to_col+1))
            blocks_to_move.add((to_row,to_col))
        else:
            blocks_to_move.add((to_row,to_col))
    
    if blocks_to_move:
        if not move_blocks(warehouse,blocks_to_move,direction):
            return False
    
    # We can now move blocks.
    for block in blocks:
        row,col = block
        to_row = row + direction_moves[direction][0]
        to_col = col + direction_moves[direction][1]
        
        warehouse[to_row][to_col] = warehouse[row][col]
        warehouse[row][col] = '.'
    return True


def move(warehouse,block,direction):
    move_to_row = block[0] + direction_moves[direction][0]
    move_to_col = block[1] + direction_moves[direction][1]
    
    if warehouse[move_to_row][move_to_col] == '[' or warehouse[move_to_row][move_to_col] == "]":
        # print(warehouse[move_to_row][move_to_col],warehouse[block[0]][block[1]])
        if direction in "<>":
            
            if not move(warehouse,(move_to_row,move_to_col),direction):
                return False            
        
            # warehouse[move_to_row][move_to_col] = warehouse[block[0]][block[1]]
            # warehouse[block[0]][block[1]] = '.'    
            # return True
        else:
            if warehouse[move_to_row][move_to_col] == '[':
                if not move_blocks(warehouse,[(move_to_row,move_to_col),(move_to_row,move_to_col+1)],direction):
                    return False

            elif warehouse[move_to_row][move_to_col] == "]":
                if not move_blocks(warehouse,[(move_to_row,move_to_col-1),(move_to_row,move_to_col)],direction):
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

    new_warehouse = [list("".join([new_blocks[b] for b in line])) for line in warehouse]
    # new_warehouse = warehouse
    start = find_starting_point(new_warehouse)

    print_warehouse(new_warehouse)
    # print(start)

    # move(new_warehouse,start,'<')
    # print_warehouse(new_warehouse)

    for m in moves:
        if move(new_warehouse,start,m):
            start = (start[0] + direction_moves[m][0],start[1]+direction_moves[m][1])    
    print_warehouse(new_warehouse)
    
    print(sum ( sum(row*100+col for col,c in enumerate(line) if c == '[') for row,line in enumerate(new_warehouse) ))


    


if __name__ == "__main__":
    main()

# 1534133 to low