"""Advent of Code: 2019.1.1"""
import sys
import re

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

    #instructions = lines[-1]
    instructions = re.findall(r"(\d+|R|L)",lines[-1].strip())
    instructions = [ c if c == 'R' or c == 'L' else int(c) for c in instructions ]
    solid_walls = set()
    open_tiles = set()
    
    offset = []
    lenght = [ len(line)-1 for line in lines[:-2]]
    max_length = max(lenght)
    offset_top = [ 0 for _ in range(max_length)]
    depth = [  len(lines)-2 for _ in range(max_length)]

    # Do stuff with lines
    for i,line in enumerate(lines,1):
        if line == "\n":
            break
        start_of_line = True
        offset_of_line = 0
        for j,char in enumerate(line,1):
            if char == '.':
                open_tiles.add((i,j))
                start_of_line = False
            elif char == '#':
                solid_walls.add((i,j))
                start_of_line = False
            if start_of_line:
                offset_of_line += 1
        offset.append(offset_of_line)           

    direction = 0 # 0:'>' 1:'v' 2:'<' 3:'^'
    col = offset[0]+1
    row = 1

    for j,_ in enumerate(offset_top,1):
        for i in range(1,len(lenght)+1):
            if (i,j) in solid_walls or (i,j) in open_tiles:
                break
            else:
                offset_top[j-1] += 1
        for i in range(len(lenght),0,-1):
            if (i,j) in solid_walls or (i,j) in open_tiles:
                break
            else:
                depth[j-1] -= 1


    # print(solid_walls)
    # print(open_tiles)
    # print(instructions)
    # print(offset)
    # print(lenght)
    # print(offset_top)
    # print(depth)

    # when out of bound, find out the cube we're in; this gives us the next cube, 
    # direction and coordinates. Use cube_size to determen cube we're in.

    for instruction in instructions:
        if instruction == 'R':
            direction = (direction + 1) % 4
        elif instruction == 'L':
            direction -= 1
            if direction < 0:
                direction = 3
        else:
            print("-----------------")
            steps = instruction
            while steps:
                if direction == 0: # Right
                    if (row,col+1) in open_tiles:
                        print("Right",steps)
                        steps -=1
                        col += 1
                    elif (row,col+1) in solid_walls:
                        print("Right, wall")
                        break
                    else:
                        print("Right outside:")
                        # We are outside, B->,C->,E->,F->                        
                        if row <= 50:
                            # B -> E
                            print("Right outside: B->E")
                            new_row = (50-row) + 101
                            new_col = 100
                            if (new_row,new_col) in solid_walls:
                                break
                            #direction = (direction + 2) % 4
                            direction = 2
                            row = new_row
                            col = new_col
                            steps -= 1
                        elif row <=100:
                            # C -> B
                            print("Right outside: C->B")
                            # Top row to first col.
                            new_row = 50
                            new_col = row + 50
                            if (new_row,new_col) in solid_walls:
                                break
                            direction = 3
                            # direction -= 1
                            # if direction < 0:
                            #     direction = 3
                            row = new_row
                            col = new_col
                            steps -= 1
                        elif row <= 150:
                            # E -> B
                            print("Right outside: E->B")
                            new_row = 101 + (50 - row)
                            new_col = 150
                            if (new_row,new_col) in solid_walls:
                                break
                            direction = 2
                            #direction = (direction + 2) % 4
                            row = new_row
                            col = new_col
                            steps -= 1
                        else:
                            # F -> E
                            print("Right outside: F->E")
                            # Top row to first col.
                            new_row = 150
                            new_col = row - 100
                            if (new_row,new_col) in solid_walls:
                                break
                            direction = 3
                            # direction -= 1
                            # if direction < 0:
                            #     direction = 3
                            row = new_row
                            col = new_col
                            steps -= 1

                elif direction == 1: # Down
                    if (row+1,col) in open_tiles:                        
                        steps -=1
                        row += 1
                        print("Down",steps)
                    elif (row+1,col) in solid_walls:
                        print("Down wall")
                        break
                    else:
                        # We are outside,
                        print("Down outside")
                        if col <= 50:
                            print("Down outside: F->B")
                            # F-> B
                            new_row = 1
                            new_col = col + 100
                            if (new_row,new_col) in solid_walls:
                                break
                            row = new_row
                            col = new_col
                            steps -= 1
                        elif col <= 100:
                            # E-> F
                            print("Down outside: E->F")
                            new_row = col + 100
                            new_col = 50
                            if (new_row,new_col) in solid_walls:
                                break
                            direction = 2
                            #direction = (direction + 1) % 4 # Turn on right
                            row = new_row
                            col = new_col
                            steps -= 1
                        else:
                            # B-> C
                            print("Down outside: B->C")
                            new_row = col - 50
                            new_col = 100
                            if (new_row,new_col) in solid_walls:
                                break
                            direction = 2
                            # direction = (direction + 1) % 4 # Turn on right
                            row = new_row
                            col = new_col
                            steps -= 1

                elif direction == 2: # Left
                    if (row,col-1) in open_tiles:
                        steps -=1
                        col -= 1
                        print("Left",steps)
                    elif (row,col-1) in solid_walls:
                        print("Left wall")
                        break
                    else:
                        # We are outside,
                        print("Left outside")
                        if row <= 50:
                            # A-> D
                            print("Left outside: A->D")
                            new_row = 150 - row +1
                            new_col = 1
                            if (new_row,new_col) in solid_walls:
                                break
                            #direction = (direction + 2) % 4 # Turn two right
                            direction = 0
                            row = new_row
                            col = new_col
                            steps -= 1
                        elif row <= 100:
                            # C-> D
                            print("Left outside: C->D")
                            new_row = 101
                            new_col = row - 50
                            if (new_row,new_col) in solid_walls:
                                break
                            # Turn one left
                            direction = 1
                            # direction -= 1
                            # if direction < 0:
                            #     direction = 3
                            row = new_row
                            col = new_col
                            steps -= 1
                        elif row <= 150:
                            # D-> A
                            print("Left outside: D->A")
                            new_row = 101 - (row-50)
                            new_col = 51
                            if (new_row,new_col) in solid_walls:
                                break
                            #direction = (direction + 2) % 4 # Turn two right
                            direction = 0
                            row = new_row
                            col = new_col
                            steps -= 1
                        else:
                            # F-> A
                            print("Left outside: F->A")
                            new_row = 1
                            new_col = row - 100
                            if (new_row,new_col) in solid_walls:
                                break
                            # Turn one left
                            # direction -= 1
                            # if direction < 0:
                            #     direction = 3
                            direction = 1
                            row = new_row
                            col = new_col
                            steps -= 1

                else: # Up
                    if (row-1,col) in open_tiles:
                        steps -=1
                        row -= 1
                        print("Up",steps)
                    elif (row-1,col) in solid_walls:
                        print("Up Wall")
                        break
                    else:
                        print("Up outside")
                        # We are outside,
                        if col <= 50:
                            # D-> C
                            print("Up outside: D->C")
                            new_row = col + 50
                            new_col = 51
                            if (new_row,new_col) in solid_walls:
                                break
                            #direction = (direction + 1) % 4 # Turn one right
                            direction = 0
                            row = new_row
                            col = new_col
                            steps -= 1
                        elif col <= 100:
                            # A-> F
                            print("Up outside: A->F")
                            new_row = col + 100
                            new_col = 1
                            if (new_row,new_col) in solid_walls:
                                break
                            #direction = (direction + 1) % 4 # Turn one right
                            direction = 0
                            row = new_row
                            col = new_col
                            steps -= 1
                        else:
                            # B-> F
                            print("Up outside: B->F")
                            new_row = 200
                            new_col = col - 100
                            if (new_row,new_col) in solid_walls:
                                break
                            row = new_row
                            col = new_col
                            steps -= 1
    
    print(row,col,direction)
    print("Password:", 1000*row + 4*col + direction)

if __name__ == "__main__":
    main()

# 107011 to low
