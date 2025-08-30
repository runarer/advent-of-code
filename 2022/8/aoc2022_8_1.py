"""Advent of Code: 2022.8.1"""
import sys

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
    tree_map = [[int(c) for c in line.strip()] for line in lines]
    visable_tree_num = len(tree_map)*2 + len(tree_map[0])*2 - 4
    visable_tree_map = [ [0 for _ in range(0,len(tree_map[0]))] for _ in range(len(tree_map))]

    # Check from top
    for x in range(1,len(tree_map[0])-1):
        highest_tree = tree_map[0][x]
        for y in range(1,len(tree_map)-1):
            if highest_tree == 9:
                break
            if tree_map[y][x] > highest_tree:
                visable_tree_map[y][x] = 1
                highest_tree = tree_map[y][x]

    # Check from bottom
    for x in range(1,len(tree_map[0])-1):
        highest_tree = tree_map[-1][x]
        for y in range(len(tree_map)-1,0,-1):
            if highest_tree == 9:
                break
            if tree_map[y][x] > highest_tree:
                visable_tree_map[y][x] = 1
                highest_tree = tree_map[y][x]

    # Check from right
    for y in range(1,len(tree_map)-1):
        highest_tree = tree_map[y][0]
        for x in range(1,len(tree_map[0])-1):
            if highest_tree == 9:
                break
            if tree_map[y][x] > highest_tree:
                visable_tree_map[y][x] = 1
                highest_tree = tree_map[y][x]

    # Check from left
    for y in range(1,len(tree_map)-1):
        highest_tree = tree_map[y][-1]
        for x in range(len(tree_map[0])-1,0,-1):
            if highest_tree == 9:
                break
            if tree_map[y][x] > highest_tree:
                visable_tree_map[y][x] = 1
                highest_tree = tree_map[y][x]

    visable_tree_num += sum( [sum(line) for line in visable_tree_map] )
    print(visable_tree_num)


if __name__ == "__main__":
    main()
