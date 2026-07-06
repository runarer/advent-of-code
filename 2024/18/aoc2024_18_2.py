"""Advent of Code: 2024.18.2"""
import sys

target_x = 71
target_y = 71
part1_bytes = 1024

target = (70,70)
start = (0,0)

def findSteps(memory, start, target):
    """Find steps from start to target in memory"""
    from collections import deque

    queue = deque([(start, 0)])  # (position, steps)
    visited = set([start])

    while queue:
        (x, y), steps = queue.popleft()

        if (x, y) == target:
            return steps

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < target_x and 0 <= ny < target_y and memory[ny][nx] == '.' and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), steps + 1))

    return -1  # Target not reachable

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
    droped_bytes = [ tuple(map(int,line.strip().split(','))) for line in lines ]
    
    # memory = [ [ '#' if (x,y) in droped_bytes else '.' for x in range(memory_width)] for y in range(memory_height) ]
    memory = [ [ '#' if (x,y) in droped_bytes[:part1_bytes] else '.' for x in range(target_x)] for y in range(target_y) ]


    # We know that there's a path at 1024 bytes.
    # We can add one and one byte and check until not reachable.   
    for (x,y) in droped_bytes[part1_bytes:]:
        memory[y][x] = '#'
        steps = findSteps(memory, start, target)

        if steps == -1:
            print(f"Part 2: {x},{y}")
            break

if __name__ == "__main__":
    main()
