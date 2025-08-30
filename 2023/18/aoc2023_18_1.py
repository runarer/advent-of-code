"""
    Advent of Code: 2019.1.1

    Walls are a set and inside can be created by a breadth first filling algoritm.
    Just need to know a square inside, is (1,1) inside?

    Find square inside:
        index(#).walls
    
"""
import sys

def draw_lagoon(walls,inside):
    min_line = min( x for x,_ in walls )
    min_row  = min( y for _,y in walls )
    max_line = max( x for x,_ in walls )
    max_row  = max( y for _,y in walls )

    #walls.sort()

    #print(walls[0]," | ",walls[-1])
    #print(min_line,min_row," | ",max_line,max_row)
    drawing = [ ['.' for _ in range(min_row,max_row+1)] for _ in range(min_line,max_line+1) ]

    #print(len(drawing),len(drawing[0]))

    move_line = abs(min_line)
    move_row  = abs(min_row)

    for line,row in walls:
        drawing[line+move_line][row+move_row] = '#'

    for line,row in inside:
        drawing[line+move_line][row+move_row] = '#'

    f = open("output.txt","w", encoding="utf-8")
    for line in drawing:
        f.writelines("".join(line)+"\n")
    f.close()

def fill_inside(walls,square_inside):
    #print(square_inside)
    inside = set()
    inside.add(square_inside)
    #print(inside)

    square_to_check = [square_inside]
    while square_to_check:
        l,r = square_to_check.pop()
        for neighbor in[ (l+x,r+y) for x,y in [(-1,0),(0,1),(1,0),(0,-1)]]:
            if neighbor in walls or neighbor in inside:
                continue
            inside.add(neighbor)
            square_to_check.append(neighbor)

    return inside
    #return len(inside)+len(walls)

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
    instructions =  [ (l[0],int(l[1]),l[2]) for line in lines if (l:= line.strip().split())]

    start = (0,0)
    walls = [ start ]

    start_line,start_row = start
    for direction,steps,_ in instructions:
        if direction == 'U':
            for i in range(1,steps+1):
                walls.append( (start_line-i,start_row) )
            start_line -= steps
        elif direction == 'R':
            for i in range(1,steps+1):
                walls.append( (start_line,start_row+i) )
            start_row += steps
        elif direction == 'D':
            for i in range(1,steps+1):
                walls.append( (start_line+i,start_row) )
            start_line += steps
        else:
            for i in range(1,steps+1):
                walls.append( (start_line,start_row-i) )
            start_row -= steps

    walls.sort()

    inside_squares = fill_inside(set(walls),(walls[0][0]+1,walls[0][1]+1))

    #print(inside_squares)

    draw_lagoon(walls,inside_squares)
    print(len(set(walls))+len(inside_squares))

if __name__ == "__main__":
    main()
