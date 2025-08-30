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
    #New
    all_nodes : set[Cord] = set()

    # Old
    nodes : dict[Cord,Self] = {}
    edges : dict[Cord,Cord] = {}
    e_lengths : dict[tuple[Cord,Cord],int] = {}

    def __init__(self,hiking_trail,start,target) -> None:

        self.left : Self = None
        self.right : Self = None
        self.start : Cord = start
        self.end : Cord = target

        self.length, self.end = self.len_to_sloap(hiking_trail,start,target)

        if self.end != target:
            # New, Find edges.
            # Where did we come from
            end = (0,0)

            if hiking_trail[self.end[0]-1][self.end[1]] == 'v':
                end = (self.end[0]-1,self.end[1])
            elif hiking_trail[self.end[0]][self.end[1]-1] == '>':
                end = (self.end[0],self.end[1]-1)
            else:
                print("New else hit",self.end)
            self.all_nodes.add(self.end)
            self.edges[self.start] = end
            self.edges[end] = self.start
            self.e_lengths[(self.start,end)] = self.length-1
            self.e_lengths[(end,self.start)] = self.length-1

            # Old, do not change
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
        else:
            #self.all_nodes.add(self.end)
            self.edges[self.start] = self.end
            self.edges[self.end] = self.start
            self.e_lengths[(self.start,self.end)] = self.length-1
            self.e_lengths[(self.end,self.start)] = self.length-1

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
class TrailNode:
    def __init__(self,coords:Cord) -> None:
        self.coords = coords

        self.edges : dict[str,Self] = {}
        self.edge_lengths : dict[str,int] = {}

    def add_edge(self, direction:str, edge:Self, length:int) -> None:
        self.edges[direction] = edge
        self.edge_lengths[direction] = length

def find_connected_node(hiking_trail,nodes,coords):
    for c in [(coords[0]-1,coords[1]),\
              (coords[0]+1,coords[1]),\
              (coords[0],coords[1]-1),\
              (coords[0],coords[1]+1),]:
        #print(coords,c,nodes)
        if c in nodes:
            #print("Found")
            return c
    return (-1,-1)

def build_graph(hiking_trail,start,target,nodes,edges,lengths) -> list[TrailNode]:
    print("E",edges)
    # Build nodes
    start_node = TrailNode(start)
    target_node = TrailNode(target)

    trail_nodes : dict[Cord,TrailNode] = { start : start_node, target : target_node}
    for coords in nodes:
        trail_nodes[coords] = TrailNode(coords)

    # Connect Nodes
    for node in trail_nodes.values():
        if node == start_node:
            connected_node = find_connected_node(hiking_trail,nodes,edges[start])
            node.add_edge("south",trail_nodes[connected_node],lengths[(start,edges[start])])
            continue

        if node == target_node:
            connected_node = find_connected_node(hiking_trail,nodes,edges[target])
            node.add_edge("north",trail_nodes[connected_node],lengths[(target,edges[target])])
            continue

        for direction, coords in { "north" : (node.coords[0]-1,node.coords[1]),\
                                   "south" : (node.coords[0]+1,node.coords[1]),\
                                   "west" : (node.coords[0],node.coords[1]-1),\
                                   "east" : (node.coords[0],node.coords[1]+1) }.items():
            if hiking_trail[coords[0]][coords[1]] in ">v":
                end_coords = edges[coords]
                # print(end_coords)
                connected_node = find_connected_node(hiking_trail,nodes,end_coords)
                node.add_edge(direction,trail_nodes[connected_node],lengths[(coords,end_coords)])
            else:
                continue

    return trail_nodes


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

    d_graph = HikeTrailNode(hiking_trail,start,target)
    print(d_graph.all_nodes)

    graph = build_graph(hiking_trail,start,target,d_graph.all_nodes,d_graph.edges,d_graph.e_lengths)
if __name__ == "__main__":
    main()
