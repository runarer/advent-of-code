"""Advent of Code: 2023.25.1"""
import sys

def MaximumAdjecencySearh(vertexes,edges):
    start = vertexes[0]
    foundSet = [start]
    cutWeight = []
    canditates = set(vertexes)
    canditates.remove(start)

    while(canditates):
        maxNextVertex = 0
        maxWeight = -10_000_000
        for next in canditates:
            print(next,len(canditates))
            weightSum = 0
            for s in foundSet:
                edge = 1 if s in edges[next] else 0
                if edge != 0:
                    weightSum += edge

            if weightSum > maxWeight:
                maxNextVertex = next
                maxWeight = weightSum
        
        canditates.remove(maxNextVertex)
        foundSet.append(maxNextVertex)
        cutWeight.append(maxWeight)

    n = len(foundSet)
    return (foundSet[n-2],foundSet[n-1],cutWeight[-1])



    pass

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
    wires = {}

    for line in lines:
        endpoint,connectedList = line.strip().split(':')
        connected = connectedList.strip().split()

        if endpoint not in wires.keys():
            wires[endpoint] = connected
        else:
            wires[endpoint].extend(connected)

        for c in connected:
            if c not in wires.keys():
                wires[c] = [endpoint]
            else:
                wires[c].append(endpoint)

    # with open("wires.txt", "w") as f:
    #     for wire,connected in wires.items():
    #         f.write(f"{wire}:{connected}\n")
    
    (a,b,c) = MaximumAdjecencySearh(list(wires.keys()),wires)
    print(a,b,c)
        



if __name__ == "__main__":
    main()
