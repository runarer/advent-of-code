"""Advent of Code: 2019.1.1"""
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
    # Start at 0,0 -> Keep track of tail movements with a set of tuples.
    head_x = 0
    head_y = 0
    tail_x = 0
    tail_y = 0
    tail_visited = set()
    tail_visited.add((0,0))

    for line in lines:
        # Parse line
        direction, moves = line.strip().split()
        moves = int(moves)

        # Move head
        for _ in range(moves):
            if direction == 'L':
                head_x -= 1
            elif direction == 'R':
                head_x += 1
            elif direction == 'U':
                head_y += 1
            else: # direction == 'D':
                head_y -= 1

            # For each head movement: Do I need to move tail? 
            # If we do more than one move we need to move the tail.
            # No, it can move over tail.
            if abs(head_x - tail_x) > 1 or abs(head_y - tail_y) > 1:
                if direction == 'R':
                    # Should be on the same y-plane
                    if head_y != tail_y:
                        tail_y = head_y
                    tail_x += 1
                elif direction == 'L':
                    # Should be on the same y-plane
                    if head_y != tail_y:
                        tail_y = head_y
                    tail_x -= 1
                elif direction == 'U':
                    # Should be on the same x-plane
                    if head_x != tail_x:
                        tail_x = head_x
                    tail_y += 1
                else: # or direction == 'D':
                    # Should be on the same x-plane
                    if head_x != tail_x:
                        tail_x = head_x
                    tail_y -= 1

                tail_visited.add((tail_x,tail_y))

            # If tail moved add coordinatres to tail_visited

    print("Tail visited: ", len(tail_visited))
    print(tail_visited)


if __name__ == "__main__":
    main()
