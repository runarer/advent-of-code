"""Advent of Code: 2019.1.1
    For each char there are two possible moves. One of these are the one we came from.
    I must be the otherone. No need to check before move. Can check for 'S' after move.

    A Map for movements. 
    { '|' : {(-1, 0),( 1, 0)},
      '-' : {( 0,-1),( 0, 1)},
      '7' : {( 1, 0),( 0,-1)},
      'J' : {( 0,-1),(-1, 0)},
      'L' : {( 0, 1),(-1, 0)},
      'F' : {( 0, 1),( 1, 0)} }

    Can use part one to find all coordiantes in the loop.
    The for each line, check each char to coordinates

    Go line by line, First and last line cannot have any.

    Replace 'S' with right tile. Then find first 'F' that's part of pipe, starting from (0,0).
    Left and above are then outside if the are not part of the pipe.
    Down right is inside if not part of pipe. Can use this as a staring point for filling out 
    inside. Then move along the pipe.
    

    NEW:
     Walk along the pipe. Mark sides as O or I if not part of pipe. After OXXXXO is 6 tiles outside.
     IXXI is four inside if XX are not part of pipe. Can mark parts that are part of the pipe and 
     visited with P.
"""
import sys


class PipeMap:
    pipe_map = []
    start = None
    moves = { '|' : ((-1, 0),( 1, 0)), '-' : (( 0,-1),( 0, 1)), '7' : (( 1, 0),( 0,-1)),
              'J' : (( 0,-1),(-1, 0)), 'L' : (( 0, 1),(-1, 0)), 'F' : (( 0, 1),( 1, 0)) }

    big_tile = { '|' : ((0,1),(1,1),(2,1)), '-' : ((1,0),(1,1),(1,2)),
                 '7' : ((1,0),(1,1),(2,1)), 'J' : ((1,0),(1,1),(0,1)), 
                 'L' : ((0,1),(1,1),(1,2)), 'F' : ((1,2),(1,1),(2,1)), 'S' : ((1,2),(1,1),(2,1)) }

    def __init__(self,pmap) -> None:
        self.pipe_map = pmap

        # Find start position
        for i,line in enumerate(self.pipe_map):
            if 'S' in line:
                self.start = (i,line.index('S'))
                break

    def add_tup(self,tup1,tup2):
        return (tup1[0]+tup2[0],tup1[1]+tup2[1])

    def get_tile(self,pos):
        return self.pipe_map[pos[0]][pos[1]]

    def get_pipe_line(self):
        pipe_line = [self.start]
        prev_pos = self.start

        # Take one step  
        cur_pos = None
        if   self.get_tile( m := self.add_tup(self.start,(-1,0)) ) in "|F7":
            cur_pos = m
        elif self.get_tile( m := self.add_tup(self.start,( 0,1))) in "-J7":
            cur_pos = m
        elif self.get_tile( m := self.add_tup(self.start,( 1,0))) in "|LJ":
            cur_pos = m
        else:
            cur_pos = self.add_tup(self.start,(0,-1))

        # Walk
        while (s := self.get_tile(cur_pos)) != 'S':
            pipe_line.append(cur_pos)
            if prev_pos != ( t := self.add_tup(cur_pos,self.moves[s][0])):
                prev_pos = cur_pos
                cur_pos = t
            else:
                temp = self.add_tup(cur_pos,self.moves[s][1])
                prev_pos = cur_pos
                cur_pos = temp           

        return pipe_line

    def walk_the_pipe(self):
        new_pipe_map = [ [ '.' for _ in range(len(self.pipe_map[0])) ] for _ in range(len(self.pipe_map)) ]
        pipe_line = self.get_pipe_line()

        for part in pipe_line:
            new_pipe_map[part[0]][part[1]] = self.get_tile(part)
        
        self.pipe_map[self.start[0]][self.start[1]] = 'F'
        new_pipe_map[self.start[0]][self.start[1]] = 'F'

        direction = 'D'

        for part in reversed(pipe_line):
            match (c := self.get_tile(part)):
                case 'F':
                    if direction == 'U':
                        direction = 'L'
                    elif direction == 'R':
                        # If above or left is '.', Set as 'I'
                        if new_pipe_map[part[0]-1][part[1]] == '.':
                            new_pipe_map[part[0]-1][part[1]] = 'I'
                        if new_pipe_map[part[0]][part[1]-1] == '.':
                            new_pipe_map[part[0]][part[1]-1] = 'I'
                        direction = 'D'
                    else:
                        print(f"Error: 'F' else: {part} {direction}")
                case 'L':
                    if direction == 'R':
                        direction = 'U'
                    elif direction == 'D':
                        # If above or left is '.', Set as 'I'
                        if new_pipe_map[part[0]][part[1]-1] == '.':
                            new_pipe_map[part[0]][part[1]-1] = 'I'
                        if new_pipe_map[part[0]+1][part[1]] == '.':
                            new_pipe_map[part[0]+1][part[1]] = 'I'
                        direction = 'L'
                    else:
                        print(f"Error: 'L' else: {part} {direction}")
                case 'J':
                    if direction == 'D':
                        direction = 'R'
                    elif direction == 'L':
                        # If above or left is '.', Set as 'I'
                        if new_pipe_map[part[0]][part[1]+1] == '.':
                            new_pipe_map[part[0]][part[1]+1] = 'I'
                        if new_pipe_map[part[0]+1][part[1]] == '.':
                            new_pipe_map[part[0]+1][part[1]] = 'I'
                        direction = 'U'
                    else:
                        print(f"Error: 'J' else: {part} {direction}")
                case '7':
                    if direction == 'L':
                        direction = 'D'
                    elif direction == 'U':
                        # If above or left is '.', Set as 'I'
                        if new_pipe_map[part[0]-1][part[1]] == '.':
                            new_pipe_map[part[0]-1][part[1]] = 'I'
                        if new_pipe_map[part[0]][part[1]+1] == '.':
                            new_pipe_map[part[0]][part[1]+1] = 'I'
                        direction = 'R'
                    else:
                        print(f"Error: '7' else: {part} {direction}")
                case '-':
                    if direction == 'R':
                        if new_pipe_map[part[0]-1][part[1]] == '.':
                            new_pipe_map[part[0]-1][part[1]] = 'I'
                        direction = 'R'
                    elif direction == 'L':
                        # If above or left is '.', Set as 'I'
                        if new_pipe_map[part[0]+1][part[1]] == '.':
                            new_pipe_map[part[0]+1][part[1]] = 'I'
                        direction = 'L'
                    else:
                        print(f"Error: '-' else: {part} {direction}")
                case '|':
                    if direction == 'D':
                        if new_pipe_map[part[0]][part[1]-1] == '.':
                            new_pipe_map[part[0]][part[1]-1] = 'I'
                        direction = 'D'
                    elif direction == 'U':
                        # If above or left is '.', Set as 'I'
                        if new_pipe_map[part[0]][part[1]+1] == '.':
                            new_pipe_map[part[0]][part[1]+1] = 'I'
                        direction = 'U'
                    else:
                        print(f"Error: '|' else: {part} {direction}")
                case _:
                    print(f"No match in case. {c}")

        tr = str.maketrans("-|7JLF","\u2500\u2502\u2510\u2518\u2514\u250C")

        for l,line in enumerate(new_pipe_map):
            # Fill in I's
            if 'I' in line:
                fill_in = False
                for i in range(line.index('I'),len(line)):
                    if line[i] == 'I':
                        fill_in = True
                    elif line[i] == '.' and fill_in:
                        line[i] = 'I'
                    else:
                        fill_in = False

            print("".join(line).translate(tr),line.count('I'),l)
        print(sum( l.count('I') for l in new_pipe_map))


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
    pipe_map = [[c for c in line.strip() ] for line in lines ]
    pm = PipeMap(pipe_map)
    pm.walk_the_pipe()


if __name__ == "__main__":
    main()
