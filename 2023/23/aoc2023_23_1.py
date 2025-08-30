"""
    Advent of Code: 2019.1.1
    
    This is a directed graph. 
    
    Of "<>^v" only ">v" are used. 
    No Dead ends.

    One '.' between arrows. An arrow indicates end of line.
"""
import sys
from typing import Self

type Cord = tuple[int,int]

class HikeTrailNode:
    nodes : dict[Cord,Self] = {}

    def __init__(self,hiking_trail,start,target) -> None:
        self.left : Self = None
        self.right : Self = None
        self.start : Cord = start
        self.end : Cord = target

        self.length, self.end = self.len_to_sloap(hiking_trail,start,target)

        if self.end != target:
            right = (self.end[0],self.end[1]+1)
            if right in self.nodes:
                self.right = self.nodes[right]
            elif hiking_trail[right[0]][right[1]] == '>':
                self.right = HikeTrailNode(hiking_trail,right,target)
                self.nodes[right] = self.right

            left = (self.end[0]+1,self.end[1])
            if left in self.nodes:
                self.left = self.nodes[left]
            if hiking_trail[left[0]][left[1]] == 'v':
                self.left = HikeTrailNode(hiking_trail,left,target)
                self.nodes[left] = self.left

    def len_to_sloap(self,hiking_trail : list[list[str]], start : Cord, target :Cord) -> tuple[int,Cord]:
        visited : set[Cord] = set()
        visited.add(start)
        visited.add( (start[0]-1,start[1]) ) # To avoid out of index.
        visited.add( (start[0],start[1]-1) )

        cur_step : Cord = start
        new_target : Cord = target

        while cur_step != new_target:
            for next_step in [(cur_step[0]-1,cur_step[1]),\
                            (cur_step[0],cur_step[1]+1),\
                            (cur_step[0]+1,cur_step[1]),\
                            (cur_step[0],cur_step[1]-1)]:
                if next_step in visited:
                    continue
                if hiking_trail[next_step[0]][next_step[1]] == '#':
                    continue

                cur_step = next_step
                if hiking_trail[next_step[0]][next_step[1]] == '>':
                    new_target = (next_step[0],next_step[1]+1)
                elif hiking_trail[next_step[0]][next_step[1]] == 'v':
                    new_target = (next_step[0]+1,next_step[1])
                visited.add(cur_step)

        return (len(visited)-2,new_target)
    
def find_longest(start: HikeTrailNode, target :Cord) -> int:
    if start is None:
        return 0

    if start.end == target:
        return start.length

    return start.length + max(find_longest(start.left,target),find_longest(start.right,target))

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
    hiking_trail = [ list(line.strip()) for line in lines ]

    start = (0,hiking_trail[0].index('.'))
    target = (len(hiking_trail)-1,hiking_trail[-1].index('.'))

    start = HikeTrailNode(hiking_trail,start,target)
    longest = find_longest(start,target)-1
    print(longest)


if __name__ == "__main__":
    main()
