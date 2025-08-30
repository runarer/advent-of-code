"""Advent of Code: 2022.8.2"""
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
    scenic_score_map = [ [0 for _ in range(0,len(tree_map[0]))] for _ in range(len(tree_map))]

    # # Check from top
    for x in range(len(tree_map[0])):
        for y,_ in enumerate(tree_map):
            # Count until higher or same value
            for i in range(y+1,len(tree_map)):
                scenic_score_map[y][x] += 1
                if tree_map[y][x] <= tree_map[i][x]:
                    break

    # # Check from bottom
    for x in range(len(tree_map[0])):
        for y in range(len(tree_map)-1,-1,-1):
            # Count until higher or same value
            scenic_score_temp = 0            
            for i in range(y-1,-1,-1):
                scenic_score_temp += 1
                if tree_map[y][x] <= tree_map[i][x]:
                    break
            scenic_score_map[y][x] *= scenic_score_temp



    # Check from right, ser riktig ut
    for y,_ in enumerate(tree_map):
        for x,_ in enumerate(tree_map[y]):
            # Count until higher or same value
            scenic_score_temp = 0
            for i in range(x+1,len(tree_map[y])):
                scenic_score_temp += 1
                if tree_map[y][x] <= tree_map[y][i]:
                    break
            scenic_score_map[y][x] *= scenic_score_temp

    # Check from left, ser riktig ut
    for y,_ in enumerate(tree_map):
        for x in range(len(tree_map[y])-1,-1,-1):
            # Count until higher or same value
            scenic_score_temp = 0
            for i in range(x-1,-1,-1):
                scenic_score_temp += 1
                if tree_map[y][x] <= tree_map[y][i]:
                    break
            scenic_score_map[y][x] *= scenic_score_temp

    best_scenic_score = max( [max(line) for line in scenic_score_map] )
    print(best_scenic_score)


if __name__ == "__main__":
    main()
