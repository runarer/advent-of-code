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
    all_nodes : dict[Cord,Self] = {}
    # visited : set[Self] = {(-1,1)}
    visited : set[Self] = {(0,1)}
    # directions = ["up","right","down","left"]

    def __init__(self,hiking_trail,start,target) -> None:
        self.nodes = { d : None for d in ["up","right","down","left"] }

        self.edges : dict[Cord,tuple[Self,int]] = {}

        start : Cord = start
        end : Cord = target

        self.all_nodes[start] = self
        length, end, n_node = self.len_to_sloap(hiking_trail,start,target)
        self.visited.add(n_node)
        print(f"{start} {end} {length} {n_node}")
        self.all_nodes[end] = self

        if end == target:
            return

        neighbors = {"up":(n_node[0]-1,n_node[1]),"right":(n_node[0],n_node[1]+1),
                     "down":(n_node[0]+1,n_node[1]),"left":(n_node[0],n_node[1]-1)}
        
        for direction, coords in neighbors.items():
            if hiking_trail[coords[0]][coords[1]] == '#':
                continue
            # print(f"{direction} {coords}")
            if coords in self.all_nodes:
                self.nodes[direction] = self.all_nodes[coords]
                # ToDo Length
            elif hiking_trail[coords[0]][coords[1]] in ">v":
                self.nodes[direction] = HikeTrailNode(hiking_trail,coords,target)

    def len_to_sloap(self,hiking_trail : list[list[str]], start : Cord, target :Cord) -> tuple[int,Cord,Cord]:
        # visited : set[Cord] = set()
        length : int = 1
        # visited.add(start)
        # visited.add( (start[0]-1,start[1]) ) # To avoid out of index.
        # visited.add( (start[0],start[1]-1) )

        # print("\t",start,target)

        self.visited.add(start)
        cur_step : Cord = start
        new_target : Cord = target
        target_not_found = True

        while cur_step != new_target:# and target_not_found:
            for next_step in [(cur_step[0]-1,cur_step[1]),\
                            (cur_step[0],cur_step[1]+1),\
                            (cur_step[0]+1,cur_step[1]),\
                            (cur_step[0],cur_step[1]-1)]:
                # print("\t\t",next_step)
                if next_step in self.visited:
                    # print("\t\tV")
                    continue
                if hiking_trail[next_step[0]][next_step[1]] == '#':
                    #print("\t\t#")
                    continue

                cur_step = next_step
                if hiking_trail[next_step[0]][next_step[1]+1] == '>':
                    new_target = (next_step[0],next_step[1]+1)
                    # target_not_found = False
                    # break
                elif hiking_trail[next_step[0]+1][next_step[1]] == 'v':
                    new_target = (next_step[0]+1,next_step[1])
                    # target_not_found = False
                    # break
                elif hiking_trail[next_step[0]][next_step[1]-1] == '>':
                    new_target = (next_step[0],next_step[1]-1)
                    # target_not_found = False
                    # break
                elif hiking_trail[next_step[0]-1][next_step[1]] == 'v':
                    new_target = (next_step[0]-1,next_step[1])
                    # target_not_found = False
                    # break
                length += 1
                self.visited.add(cur_step)

        return (length,cur_step,new_target)

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

    start = (1,hiking_trail[0].index('.'))
    target = (len(hiking_trail)-1,hiking_trail[-1].index('.'))

    start_node = HikeTrailNode(hiking_trail,start,target)

    # start = HikeTrailNode(hiking_trail,start,target)
    # longest = find_longest(start,target)-1
    # print(longest)


if __name__ == "__main__":
    main()
