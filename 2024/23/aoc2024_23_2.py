"""Advent of Code: 2024.23.2

    A bit slow, ~1sec. It works with strings so hashing is easier and we can
    use set to remove duplicates easy.
"""
import sys

def build_graph(lines:list[list[str]]) -> dict[str,set[str]]:
    graph:dict[str,set[str]] = {}

    for line in lines:
        # print(line)
        if line[0] in graph:
            graph[line[0]].add(line[1])
        else:
            graph[line[0]] = {line[1]}

        if line[1] in graph:
            graph[line[1]].add(line[0])
        else:
            graph[line[1]] = {line[0]}

    return graph


def got_common(first,second) -> list[str]:
    common_list = []

    for a in first:
        for b in second:
            if a == b:
                common_list.append(a)
                break
    
    common_list.sort()
    return common_list


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
    lines = [line.strip().split('-') for line in lines]

    graph = build_graph(lines)
    computers = list(graph.keys())
    computers.sort()

    connected:set[tuple[str,str,str]] = set()
    for computer in computers:
        for cnt in graph[computer]:
            if cnt <= computer:
                continue

            for common in graph[computer].intersection(graph[cnt]):
                if common <= computer:
                    continue
                if cnt < common:
                    connected.add((computer,cnt,common))
                else:
                    connected.add((computer,common,cnt))



    connections = [",".join(t) for t in connected]
    connections.sort()

    prevoius_connections = []
    
    while connections:
        new_connections = set()

        for connection in connections:
            connection = connection.split(',')
            commons = set()
            for i,computer in enumerate(connection):
                if i == 0:
                    commons = graph[computer]
                else:
                    commons = commons.intersection(graph[computer])

            # commons now contains all computers that is connected to all of the computers in connection,
            # but they may not be connected to eachother
            
            # if no more connections could be made, we are done with this connection
            if not commons:
                continue

            # create new list of connections
            for computer in commons:
                new_list = connection
                new_list.append(computer)
                new_list.sort()

                new_connections.add(",".join(new_list))
        prevoius_connections = connections
        connections = new_connections


    print(prevoius_connections)

if __name__ == "__main__":
    main()
