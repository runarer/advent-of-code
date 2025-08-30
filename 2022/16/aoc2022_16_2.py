"""Advent of Code: 2022.16.2"""
import sys

# This is "Single-source shortest path problem", kan løses med Dijkstra,
# noe jeg mistenkte fra starten av og skulle ha undersøkt nærmere.

# Hvordan skal graph være bygd opp?
# graph['AA'] = {'BB':2,'DD':3, 'FF':1}

# Hva med å finne alle paths fra initial_node som er 26 lange. Dette krever at man legger til 
# 1 for hver node for åpningen av ventilen.
# Alle paths som ikke deler 

# Bruk svaret fra oppgave 1 til gjøre Santas valg av ventiler. 
# Når dette er gjort kan man prøve elefantens valg på samme måte, men 
# med Santas valg markert som visited. Så legge sammen svarene.


# Kan jeg endre Dijkstra slik at lengden mellom noder er ertasttet med pressure release for å gå ditt.
# Dette gis med en funksjon som tar tid igjen som argument. 
# Dijkstra endres for størst verdi istden for minst.

# Den orginale ser ut til å fungere, bare en feil ved starten.

def pressure_released(pressures,node,minutes):
    """ Ny """
    return pressures[node]*minutes

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

    # Time for opening valve
    for node in distance:
        if node != initial_node:
            distance[node] += 1

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

# With santa and elephant: Both can take one, or the one with most time left

def open_valve(current_node1, time1, current_node2, time2, first_moved, visited, pressure, shortest_distances):
    """ dase """
    if (time1 < 2) and (time2 < 2):
        return 0
    if len(visited) == len(shortest_distances[current_node1]):
        return 0

    # if current_node1 == current_node2:
    #     print("Same",current_node2)

    time = 0
    current_node = ""

    # Who moved?
    # Add the node they came from to visited, and return pressure released from their move.
    if first_moved:
        time1 -= 1
        time = time1
        current_node = current_node1
    else:
        time2 -= 1
        time = time2
        current_node = current_node2
    
    new_visited = visited.copy()
    if current_node not in visited:
        new_visited = visited + [current_node]

    # Who will move next
    first = True
    if (time1 < time2):
        first = False

    best_score = 0
    if first:
        for node, travel_time in shortest_distances[current_node1].items(): # change to unvisitied
            if node in new_visited:
                continue

            #Need to check if there is time to visit and turn on this valve
            if (time1 - (travel_time + 1)) < 1:
                continue

            best_score = max(best_score,open_valve(node,time1 - travel_time,\
                                current_node2,time2, True,\
                                new_visited, pressure,shortest_distances))
            print("F",new_visited+[node],time)
        #print("F",visited+[current_node])
    else:
        for node, travel_time in shortest_distances[current_node2].items(): # change to unvisitied
            if node in new_visited:
                continue

            #Need to check if there is time to visit and turn on this valve
            if (time - (travel_time + 1)) < 1:
                continue
            best_score = max(best_score,open_valve(current_node1,time1,\
                                node,time2 - travel_time, False,\
                                new_visited, pressure,shortest_distances))
            print("S",new_visited+[node],time)
        #print("S",visited+[current_node])
    return best_score + time * pressure[current_node]












def rec(cave,pressure,node1,node2,time1,time2,path):
    """ Just stop """
    first_move = True

    # Stops, no more time left to do anything
    if time1 < 2:
        if time2 < 2:
            return 0
        first_move = False

    # Who moves?
    if time2 > time1:
        first_move = False

    max_pressure = 0
    if first_move:
        first_move = False
        for node in cave['AA']:
            # Have we visited this node
            pres = 0
            if node in path:
                continue
            time_left = time1 - cave[node1][node]
            if time_left > 0:
                pres = (pressure[node]*time_left) + rec(cave,pressure,node,node2,time_left,time2,path + [node])
                first_move = True
            else:
                continue
            max_pressure = max(pres,max_pressure)

    if not first_move:
        for node in cave['AA']:
            pres = 0
            if node in path:
                continue
            time_left = time2 - cave[node2][node]
            if time_left > 0:
                pres = (pressure[node]*time_left) + rec(cave,pressure,node1,node,time1,time_left,path + [node])
            else:
                continue
            max_pressure = max(pres,max_pressure)

    return max_pressure

def start_rec(cave,pressure):
    """Starts the recursen"""
    max_pressure = 0
    #selected_nodes = ["AA"]
    for node1 in cave["AA"]:
        if node1 == "AA":
            continue
        #selected_nodes.append(node1)
        for node2 in cave["AA"]:
            if node2 in ("AA",node1):
            #if node2 in selected_nodes:
                continue
            print("Checking",node1,node2)
            time1 = 26 - cave["AA"][node1]
            time2 = 26 - cave["AA"][node2]
            max_pres = 0
            max_pres += pressure[node1]*time1
            max_pres += pressure[node2]*time2
            max_pres += rec(cave,pressure,node1,node2,time1,time2,["AA",node1,node2])
            max_pressure = max(max_pres,max_pressure)

    return max_pressure

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
    # print(shortest_distances['AA'])
    # for node,minutes in shortest_distances['AA'].items():
    #     #print(node,minutes)
    #     print(node, pressure_released(pressure,node,26-minutes))

    best_pressure = start_rec(shortest_distances,pressure)
    print(best_pressure)

    # best_pressure = open_valve("AA",27,"AA",26,True,["AA"],pressure,shortest_distances)
    # print(best_pressure)

if __name__ == "__main__":
    main()

# 2512 is to low