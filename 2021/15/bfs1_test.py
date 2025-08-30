""" Dette finner hva man kan nå.
    https://www.redblobgames.com/pathfinding/a-star/implementation.html#python
"""
import collections
from typing import TypeVar
from typing import Protocol, List, Dict

#Definerer en type! YOO!!!
Location = TypeVar("Location")
#Protocol er som interface, men kanskje litt anderledes
class Graph(Protocol):
    def neighbors(self, id:Location) -> List[Location]: pass

class SimpleGraph():
    def __init__(self) -> None:
        self.edges: Dict[Location, List[Location]] = {}

    def neighbors(self, id:Location) -> List[Location]:
        return self.edges[id]

def breadth_first_search(graph: Graph, start: Location):
    frontier = collections.deque()
    frontier.append(start)
    reached: Dict[Location, bool] = {}
    reached[start] = True

    while frontier: # Fungerer dette? Skal sjekke om køen ikke er tom.
        current: Location = frontier.popleft()
        print(" Besøker %s" % current)
        for next in graph.neighbors(current):
            if next not in reached:
                frontier.append(next)
                reached[next] = True

def main():
    example_graph = SimpleGraph()
    example_graph.edges = {
        'A':['B'],
        'B':['C'],
        'C':['B','D','F'],
        'D':['C','E'],
        'E':['F'],
        'F':[]
    }

    print("Når fra A:")
    breadth_first_search(example_graph,'A')
    print("Når fra E:")
    breadth_first_search(example_graph,'E')


if __name__ == '__main__':
    main()
