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
                        break
                    else:
                        # We are outside
                        if (row,offset[row-1]+1) in solid_walls:
                            break
                        elif (row,offset[row-1]+1) in open_tiles:
                            col = offset[row-1]+1
                            steps -= 1
                            print("Right turn around",steps)
                        else:
                            print("whut, right turn around")
                elif direction == 1: # Down
                    if (row+1,col) in open_tiles:
                        steps -=1
                        row += 1
                        print("Down",steps)
                    elif (row+1,col) in solid_walls:
                        break
                    else:
                        # We are outside
                        if (offset_top[col-1]+1,col) in solid_walls:
                            break
                        elif (offset_top[col-1]+1,col) in open_tiles:
                            row = offset_top[col-1]+1
                            steps -= 1
                            print("Down turn around",steps)
                        else:
                            print("whut, down turn around")
                elif direction == 2: # Left
                    if (row,col-1) in open_tiles:
                        steps -=1
                        col -= 1
                        print("Left",steps)
                    elif (row,col-1) in solid_walls:
                        break
                    else:
                        # We are outside
                        if (row,lenght[row-1]) in solid_walls:
                            break
                        elif (row,lenght[row-1]) in open_tiles:
                            col = lenght[row-1]
                            steps -= 1
                            print("Left turn around",steps)
                        else:
                            print("whut, left turn around")
                else: # Up
                    if (row-1,col) in open_tiles:
                        steps -=1
                        row -= 1
                        print("Up",steps)
                    elif (row-1,col) in solid_walls:
                        break
                    else:
                        # We are outside
                        if (depth[col-1],col) in solid_walls:
                            break
                        elif (depth[col-1],col) in open_tiles:
                            row = depth[col-1]
                            steps -= 1
                            print("Up turn around",steps)
                        else:
                            print("whut, up turn around")
                            sys.exit(1)
    
    print(row,col,direction)
    print("Password:", 1000*row + 4*col + direction)

if __name__ == "__main__":
    main()
