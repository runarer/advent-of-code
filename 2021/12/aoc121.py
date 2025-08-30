import sys

def build_map(connections):
    cave_map = {}

    for connection in connections:
        cave1,cave2 = connection.strip().split('-')
        if cave1 in cave_map:
            cave_map[cave1].append(cave2)
        else:
            cave_map[cave1] = [cave2]
        if cave2 in cave_map:
            cave_map[cave2].append(cave1)
        else:
            cave_map[cave2] = [cave1]

    return cave_map

def travel(cave_path, cave_map):
    paths = []
    for next_cave in cave_map[cave_path[-1]]:
        if next_cave == "end":
            paths.append(cave_path + [next_cave])
            continue
        if next_cave in cave_path and next_cave.islower():
            continue
        if next_cave == "start":
            continue
        paths += travel(cave_path + [next_cave],cave_map)
    return paths

    #return [travel(next_cave,cave_map) for next_cave in cave_map[cave]]
    # print(cave_path)
    # return [travel(cave_path + [next_cave],cave_map) \
    #      for next_cave in cave_map[cave_path[-1]] \
    #          if next_cave.isupper() or next_cave not in cave_path or "end" in cave_path]

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
    
    cave_map = build_map(lines)
    paths = travel(["start"],cave_map)
    print(len(paths))


if __name__ == "__main__":
    main()
