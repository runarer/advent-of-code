"""Advent of Code: 2022.12.1"""
import sys
from collections import deque

def alpha_to_number(character):
    """ Return the heigth for"""
    if character =='S':
        return 0
    if character == 'E':
        return 27
    return ord(character) - 96

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
    forest_map = [ [ alpha_to_number(char) for char in line.strip() ] for line in lines ]
    forest_map_max_x = len(forest_map[0]) - 1
    forest_map_max_y = len(forest_map) - 1
    max_length = len(forest_map[0]) * len(forest_map) + 100
    
    start = ()
    destination = ()
    # Find start and destination nodes
    for i, line in enumerate(forest_map):
        if 0 in line:
            start = (line.index(0),i)
        if 27 in line:
            destination = (line.index(27),i)

    def get_neighbors(node):
        x,y = node
        neighbors = []
        if x > 0 and forest_map[y][x-1] <= forest_map[y][x] + 1:
            neighbors.append((x-1,y))
        if x < forest_map_max_x and forest_map[y][x+1] <= forest_map[y][x] + 1:
            neighbors.append((x+1,y))
        if y > 0 and forest_map[y-1][x] <= forest_map[y][x] + 1:
            neighbors.append((x,y-1))
        if y < forest_map_max_y and forest_map[y+1][x] <= forest_map[y][x] + 1:
            neighbors.append((x,y+1))
        return neighbors

    visited = set([(start)])
    distance = { (x,y):max_length for x in range(len(forest_map[0])) for y in range(len(forest_map))}
    distance[start] = 0

    queue = deque([start])

    while queue:
        node = queue.popleft()
        neighbors = get_neighbors(node)
        for neighbor in neighbors:
            if neighbor not in visited:
                distance[neighbor] = min(distance[neighbor],distance[node]+1)
                if neighbor not in queue:
                    queue.append(neighbor)
        if node == destination:
            break
        visited.add(node)

    
    print(distance[destination])

if __name__ == "__main__":
    main()
