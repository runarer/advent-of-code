"""Advent of Code: 2024.22.1"""
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

    part1 = sum(1 for c1,c2,c3 in connected if c1.startswith('t') or c2.startswith('t') or c3.startswith('t'))
    print(f"Part 1: {part1}")

if __name__ == "__main__":
    main()
