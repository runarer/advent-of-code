""" 
    Breadth First Search
    https://www.redblobgames.com/pathfinding/a-star/implementation.html#python

    Nå for grid
"""
import collections
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
    grid = SquareGrid(30,15)
    grid.walls = [(11,2),(0,5),(14,12)]
    start = (8,7)
    goal = (17,2)
    parent =  breadth_first_search(grid, start, goal)
    draw_grid(grid)

if __name__ == '__main__':
    main()
