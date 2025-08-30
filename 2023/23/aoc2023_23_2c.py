"""
    Advent of Code: 2019.1.1
    
    This is a directed graph. 
    
    Of "<>^v" only ">v" are used. 
    No Dead ends.

    One '.' between arrows. An arrow indicates end of line.
"""
import sys
from typing import Self

class TrailNode:
    def __init__(self,coords:tuple[int,int]) -> None:
        self.coords = coords

        self.edges : dict[str,Self] = {}
        self.edge_lengths : dict[str,int] = {}

def find_all_nodes(hiking_trail) -> tuple[set[TrailNode],dict[tuple[int,int],TrailNode]]:
    nodes = set()
    connections = {}

    for i,line in enumerate(hiking_trail[1:-1],start=1):
        for j,c in enumerate(line[1:-1],start=1):
            if c == '.':
                if sum(1 for x,y in [(i-1,j),(i+1,j),(i,j-1),(i,j+1)] if hiking_trail[x][y] in ">v" ) > 2:
                    node = TrailNode( (i,j) )
                    nodes.add( node )

                    for neigbour in [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]:
                        if hiking_trail[neigbour[0]][neigbour[1]] == '#':
                            continue
                        connections[neigbour] = node
    return (nodes,connections)

def find_end(hiking_trail,node,start) -> tuple[int,int]:
    visited : set[int,int] = set()
    visited.add(node)
    visited.add(start)

    cur_step = start
    new_target = None

    while cur_step != new_target:
        for next_step in [(cur_step[0]-1,cur_step[1]),\
                        (cur_step[0],cur_step[1]+1),\
                        (cur_step[0]+1,cur_step[1]),\
                        (cur_step[0],cur_step[1]-1)]:

            if next_step[0] < 0 or next_step[0] >= len(hiking_trail):
                new_target = cur_step
                break
            if next_step in visited:
                continue
            if hiking_trail[next_step[0]][next_step[1]] == '#':
                continue

            cur_step = next_step
            if hiking_trail[next_step[0]][next_step[1]] in ">v":
                new_target = next_step
            visited.add(cur_step)

    return (new_target,len(visited)-1)

def connect_all_edges(hiking_trail,nodes,connections):
    for node in nodes:
        i,j = node.coords

        if i == 0:
            end,length = find_end(hiking_trail,node.coords,(1,1))

            node.edges["south"] = connections[end]
            node.edge_lengths["south"] = length
            continue

        if i == (l :=  len(hiking_trail)-1):
            end,length = find_end(hiking_trail,node.coords,(l-1,l-1))

            node.edges["north"] = connections[end]
            node.edge_lengths["north"] = length
            continue


        for direction,neigbour in {"north":(i-1,j),"south":(i+1,j),"west":(i,j-1),"east":(i,j+1)}.items():
            if hiking_trail[neigbour[0]][neigbour[1]] == '#':
                continue

            # Find edge
            end,length = find_end(hiking_trail,node.coords,neigbour)

            node.edges[direction] = connections[end]
            node.edge_lengths[direction] = length

def build_graph(hiking_trail) -> TrailNode:    
    start = (0,hiking_trail[0].index('.'))
    target = (len(hiking_trail)-1,hiking_trail[-1].index('.'))

    nodes,connections = find_all_nodes(hiking_trail)

    start_node = TrailNode(start)
    nodes.add( start_node )
    connections[start] = start_node

    target_node = TrailNode(target)
    nodes.add( target_node )
    connections[target] = target_node

    connect_all_edges(hiking_trail,nodes,connections)

    return (start_node,target_node)

def find_longest_path(start:TrailNode,target:TrailNode,visited:set[TrailNode]) -> int:
    longest_path = 0

    for direction,connected_node in start.edges.items():
        if connected_node == target:
            return start.edge_lengths[direction]

        if connected_node in visited:
            continue

        visited.add(connected_node)
        path_to_target = find_longest_path(connected_node,target,visited)
        visited.remove(connected_node)

        if path_to_target == 0:
            continue

        path_to_target += 1 + start.edge_lengths[direction]
        longest_path = max(path_to_target,longest_path)

    return longest_path

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

    start_node,target_node = build_graph(hiking_trail)

    visited = {start_node}
    longest_path = find_longest_path(start_node,target_node,visited)
    print(longest_path)

if __name__ == "__main__":
    main()

# 6333 to high