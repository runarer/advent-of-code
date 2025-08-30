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
"""
import sys

class PipeMap:
    pipe_map =[]
    start = None
    moves = { '|' : ((-1, 0),( 1, 0)), '-' : (( 0,-1),( 0, 1)), '7' : (( 1, 0),( 0,-1)),
              'J' : (( 0,-1),(-1, 0)), 'L' : (( 0, 1),(-1, 0)), 'F' : (( 0, 1),( 1, 0)) }

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

    def get_cycle_length(self):
        prev_pos = self.start


        # Take one step
        steps = 1
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
            if prev_pos != ( t := self.add_tup(cur_pos,self.moves[s][0])):
                prev_pos = cur_pos
                cur_pos = t
            else:
                temp = self.add_tup(cur_pos,self.moves[s][1])
                prev_pos = cur_pos
                cur_pos = temp
            steps += 1

        return steps

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
    pipe_map = [ line.strip() for line in lines ]
    pm = PipeMap(pipe_map)
    print(pm.get_cycle_length() // 2)


if __name__ == "__main__":
    main()
