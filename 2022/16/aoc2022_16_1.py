"""Advent of Code: 2022.16.1"""
import sys
# import copy
# from queue import PriorityQueue

# This is "Single-source shortest path problem", kan løses med Dijkstra,
# noe jeg mistenkte fra starten av og skulle ha undersøkt nærmere.

# Hvordan skal graph være bygd opp?
# graph['AA'] = {'BB':2,'DD':3, 'FF':1}

def calculate_shortest_distances(graph):
    """ Finds the shortest distance for all nodes """
    distances = {}

    for node in graph:
        distances[node] = calculate_shortest_distance(graph,node)

    return distances


def calculate_shortest_distance(graph,initial_node):
    """Uses Dijkstas to find the shortest distance"""

    # Set all nodes as unvisited
    unvisited = set(graph.keys())

    # Assign a big distance value, exept for first node
    distance = { node:1000000 for node in graph }
    distance[initial_node] = 0

    current_node = initial_node
    while unvisited:
        # Calculate tentative distances        
        for neighbour in graph[current_node]:
            if neighbour in unvisited:
                distance[neighbour] = min(distance[neighbour],\
                                        distance[current_node]+graph[current_node][neighbour])

        # Remove current_node from unvisited
        unvisited.remove(current_node)

        # find next unvisited, the one with lowest distance
        smallest_distance = 1000000
        for node in unvisited:
            if distance[node] < smallest_distance:
                current_node = node
                smallest_distance = distance[node]

    return distance


def calculate_pressure_release(shorthest_distance,pressure,mins):
    """ Somtehrtingf """

    potential_pressure_releace = {}

    for node,travel_time in shorthest_distance.items():
        time = mins - 1 - travel_time
        if time > 0:
            potential_pressure_releace[node] = pressure[node] * time
        else:
            potential_pressure_releace[node] = 0

    return potential_pressure_releace

def open_valve(current_node,time,visited,pressure,shortest_distances):
    """ dase """
    if time < 2:
        return 0
    if len(visited) == len(shortest_distances[current_node]):
        return 0

    time -= 1

    new_visited = visited + [current_node]

    best_score = 0
    for node, travel_time in shortest_distances[current_node].items():
        if node in new_visited:
            continue

        #Need to check if there is time to visit and turn on this valve
        if (time - (travel_time + 1)) < 1:
            continue

        best_score = max(best_score,open_valve(node,time - travel_time,\
                         new_visited, pressure,shortest_distances))

    return best_score + time * pressure[current_node]

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
    lines = [line.strip().split() for line in lines]

    pressure = {}
    start = "AA"
    minutes = 30

    cave_temp = {}
    connections = {}
    for line in lines:
        cave_part = line[1]
        pressure[cave_part] = int(line[4].split('=')[1].split(';')[0])
        connected = [ part[0:2] for part in line[9:]]
        if (pressure[cave_part] > 0) or (cave_part == start):
            cave_temp[cave_part] = connected
        else:
            connections[cave_part] = connected

    cave = {}
    for room, connected_rooms in cave_temp.items():
        cave[room] = {}
        for connected_room in connected_rooms:
            mins = 1
            prev_room = room
            current_room = connected_room
            while current_room in connections:
                r1, r2 = connections[current_room]
                if r1 == prev_room:
                    prev_room = current_room
                    current_room = r2
                else:
                    prev_room = current_room
                    current_room = r1

                mins += 1
            cave[room][current_room] = mins

    shortest_distances = calculate_shortest_distances(cave)

    best_pressure = open_valve("AA",31,[],pressure,shortest_distances)
    print(best_pressure)

if __name__ == "__main__":
    main()







# I can reduce the graf of the cave down to start (AA) and every room with a valve.
# Room with pressure 0 are just passthrues
# For each node of the graf, not the start, find distanse in minutes to the other valves.
# With help of pressure and distance the next best move can be calculated.
# If all move from on node to another are thru start, we have a two subgraphs.
# What about the 30 minutes?

# def move(cave, location, minute):
#     """ Depth first search, return pressure released. """
#     if minute <= 0:
#         print("bottom")
#         return 0

#     # Open valve? Lønner det seg alltid å åpne?
#     opened_the_valve = False
#     if cave[location]['pressure'] > 0 and not cave[location]['open']:
#         minute -= minute
#         cave[location]['open'] = True
#         opened_the_valve = True

#     # Go to next room if time
#     if minute <= 0:
#         print("bottom 2")
#         return 0
#     best_pressure = 0
#     for next_room in cave[location]['connected']:
#         best_pressure = move(cave,next_room,minute-1)

#     # Calculate pressure from this room
#     if opened_the_valve:
#         best_pressure += cave[location]['pressure'] * minute

#     return best_pressure