"""https://www.redblobgames.com/pathfinding/grids/graphs.html"""
import sys
import heapq
from typing import Iterator, Optional, TypeVar, List, Dict, Tuple

Location = TypeVar("Location")

GridLocation = Tuple[int,int]

class CaveMap:
    def __init__(self, cave_map: List[List[int]]):
        self.width = len(cave_map)
        self.height = self.width
        self.weights = cave_map # Turn this into dict?

    def in_bound(self, node: GridLocation) -> bool:
        (x,y) = node
        return 0 <= x < self.width and 0 <= y < self.height

    def cost(self, to_node: GridLocation) -> int:
        (x,y) = to_node
        return self.weights[y][x] #Er det yx eller xy

    def neighbors(self, node: GridLocation) -> Iterator[GridLocation]:
        (x, y) = node
        neighbors = [(x+1,y),(x-1,y),(x,y-1),(x,y+1)]
        return filter(self.in_bound, neighbors)

def dijkstra_search(cave: CaveMap, start: GridLocation, goal: GridLocation):
    """ ds"""
    frontier: List[Tuple[int, GridLocation]] = []
    heapq.heappush(frontier, (0,start))
    came_from: Dict[GridLocation, Optional[GridLocation]] = {}
    cost_so_far: Dict[GridLocation, int] = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:
        current: GridLocation = heapq.heappop(frontier)[1]

        if current == goal:
            break

        for next_node in cave.neighbors(current):
            new_cost = cost_so_far[current] + cave.cost(next_node)
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost
                heapq.heappush(frontier,(priority, next_node))
                came_from[next_node] = current

    return came_from, cost_so_far

def reconstruct_path(came_from: Dict[GridLocation, GridLocation], \
    start: GridLocation, goal: GridLocation) -> List[Location]:
    current: GridLocation = goal
    path: List[GridLocation] = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path


def main():
    """Start"""
    #get argument
    if len(sys.argv) < 1:
        sys.exit("Usage: python " + sys.argv[0] + " filename")
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except IOError as err:
        print("{}\nError opening {}. Terminating program.".format(err, filename), file=sys.stderr)
        sys.exit(1)
    # This is cost "map"
    
    cave_map = [[int(cha) for cha in line.strip()] for line in lines]
    start, goal = (0,0), (len(cave_map)-1,len(cave_map)-1)
    cave = CaveMap(cave_map)
    came_from, cost_so_far = dijkstra_search(cave, start,goal)
    print(cost_so_far[goal])

    # path = reconstruct_path(came_from,start,goal)
    # for x,y in path:
    #     cave_map[y][x] = 'X'

    # with open("test3.txt",'w') as fileout:
    #     for row in cave_map:
    #         line = ""
    #         for elem in row:
    #             line += str(elem)
    #         fileout.write(line + '\n')


if __name__ == "__main__":
    main()
