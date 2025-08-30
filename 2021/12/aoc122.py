import sys
from functools import reduce
# Kan jeg "jukse" med å legge til flere i cave map som zs og Zs.
# Kun en not islower() and not isupper() kan være i path.

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
    """Kan erstatte reduce med et 'merke' i listen. """
    paths = []
    for next_cave in cave_map[cave_path[-1]]:
        if next_cave == "end":
            paths.append(cave_path + [next_cave])
            continue
        if next_cave == "start":
            continue
        if next_cave.islower() and next_cave in cave_path:
            small_caves = list(filter(lambda c : c.islower(),cave_path))
            if reduce((lambda x, y: x or y), map((lambda n : small_caves.count(n) > 1), small_caves)):                
                continue
        paths += travel(cave_path + [next_cave],cave_map)
    return paths

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
