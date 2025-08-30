""" 
    Dijkstra
    https://www.redblobgames.com/pathfinding/a-star/implementation.html#python-dijkstra

"""
import collections
import heapq
from typing import Iterator, Optional, TypeVar, Protocol, List, Dict, Tuple

#Definerer en type! YOO!!!
Location = TypeVar("Location")
#Protocol er som interface, men kanskje litt anderledes
class Graph(Protocol):
    def neighbors(self, id:Location) -> List[Location]: pass

GridLocation = Tuple[int,int]

class SquareGrid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.walls: List[GridLocation]

    def in_bound(self, id: GridLocation) -> bool:
        (x,y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id: GridLocation) -> bool:
        return id not in self.walls

    def neighbors(self, id: GridLocation) -> Iterator[GridLocation]:
        (x,y) = id
        neighbors = [(x+1,y),(x-1,y),(x,y-1),(x,y+1)]
        if (x + y) % 2 == 0: neighbors.reverse() # see "Ugly paths" section for an explanation
        results = filter(self.in_bound,neighbors)
        results = filter(self.passable, results)
        return results

## Dijkstra
class WeightedGraph(Graph):
    def cost(self, from_id: Location, to_id: Location) -> float: pass

class GridWithWeight(SquareGrid):
    def __init__(self, width: int, height: int):
        super().__init__(width,height)
        self.weights: Dict[GridLocation, float] = {}

    def cost(self, from_node: GridLocation, to_node: GridLocation) -> float:
        #Here movement is only dependent on to_node.
        return self.weights.get(to_node, 1) # <- Hva betyr dette, 1 er default value.

def dijkstra_search(graph: WeightedGraph, start: Location, goal: Location):
    frontier: List[Tuple[float, Location]] = []
    heapq.heappush(frontier, (0,start))
    came_from: Dict[Location, Optional[Location]] = {}
    cost_so_far: Dict[Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:
        current: Location = heapq.heappop(frontier)[1]

        if current == goal:
            break

        for next_node in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next_node)
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost
                heapq.heappush(priority, next_node)
                came_from[next_node] = current

        return came_from, cost_so_far

def reconstruct_path(came_from: Dict[Location, Location], start: Location, goal: Location) -> List[Location]:
    current: Location = goal
    path: List[Location] = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start) # optional ? Why, jo tar ikke med i while loop
    path.reverse() # optional.
    return path
##

def breadth_first_search(graph: Graph, start: Location, goal: Location):
    frontier = collections.deque()
    frontier.append(start)
    came_from: Dict[Location, Optional[Location]] = {}
    came_from[start] = None

    while frontier:
        current: Location = frontier.popleft()

        if current == goal: #Early exit
            break

        for next_node in graph.neighbors(current):
            if next_node not in came_from:
                frontier.append(next_node)
                came_from[next_node] = current

    return came_from

def draw_grid(grid: SquareGrid):
    for y in range(grid.height):
        line = ""
        for x in range(grid.width):            
            if (x,y) in grid.walls:
                line += '#'
            else:
                line += '.'
        print(line)

def main():
    # grid = SquareGrid(30,15)
    # grid.walls = [(11,2),(0,5),(14,12)]
    # start = (8,7)
    # goal = (17,2)
    # parent =  breadth_first_search(grid, start, goal)
    # draw_grid(grid)
    start, goal = (0,0), (9,9)
    came_from, cost_so_far = dijkstra_search(,start,goal)

if __name__ == '__main__':
    main()
