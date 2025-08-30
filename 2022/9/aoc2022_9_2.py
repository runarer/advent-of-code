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
    ropes = [ { 'x':0 , 'y':0} for _ in range(10)]
    last_rope_visited = set()
    last_rope_visited.add((0,0))

    for line in lines:
        # Parse line
        direction, moves = line.strip().split()
        moves = int(moves)

        # Move head
        for _ in range(moves):
            if direction == 'L':
                ropes[0]['x'] -= 1
            elif direction == 'R':
                ropes[0]['x'] += 1
            elif direction == 'U':
                ropes[0]['y'] += 1
            else: # direction == 'D':
                ropes[0]['y'] -= 1

            for rope, pos in enumerate(ropes[1:],start=1):

                if abs(ropes[rope-1]['x'] - pos['x']) == 2 or abs(ropes[rope-1]['y'] - pos['y']) == 2:
                    if ropes[rope-1]['x'] - pos['x'] > 0:
                        pos['x'] += 1
                    elif ropes[rope-1]['x'] - pos['x'] < 0:
                        pos['x'] -= 1

                    if ropes[rope-1]['y'] - pos['y'] > 0:
                        pos['y'] += 1
                    elif ropes[rope-1]['y'] - pos['y'] < 0:
                        pos['y'] -= 1
                else:
                    break

                if rope == 9:
                    last_rope_visited.add( (pos['x'],pos['y']) )

    print("Tail visited: ", len(last_rope_visited))

if __name__ == "__main__":
    main()




                # # Move diagonal right/up
                # if   (ropes[rope-1]['x'] - pos['x'] == 2 and ropes[rope-1]['y'] - pos['y'] == 1) \
                # or   (ropes[rope-1]['x'] - pos['x'] == 1 and ropes[rope-1]['y'] - pos['y'] == 2) \
                # or   (ropes[rope-1]['x'] - pos['x'] == 2 and ropes[rope-1]['y'] - pos['y'] == 2) :
                #     pos['x'] += 1
                #     pos['y'] += 1

                # # Move diagonal right/down
                # elif (ropes[rope-1]['x'] - pos['x'] == 2 and ropes[rope-1]['y'] - pos['y'] == -1) \
                # or   (ropes[rope-1]['x'] - pos['x'] == 1 and ropes[rope-1]['y'] - pos['y'] == -2) \
                # or   (ropes[rope-1]['x'] - pos['x'] == 2 and ropes[rope-1]['y'] - pos['y'] == -2) :
                #     pos['x'] += 1
                #     pos['y'] -= 1

                # # Move diagonal left/up
                # elif (ropes[rope-1]['x'] - pos['x'] == -2 and ropes[rope-1]['y'] - pos['y'] == 1) \
                # or   (ropes[rope-1]['x'] - pos['x'] == -1 and ropes[rope-1]['y'] - pos['y'] == 2) \
                # or   (ropes[rope-1]['x'] - pos['x'] == -2 and ropes[rope-1]['y'] - pos['y'] == 2) :
                #     pos['x'] -= 1
                #     pos['y'] += 1

                # # Move diagonal left/down
                # elif (ropes[rope-1]['x'] - pos['x'] == -2 and ropes[rope-1]['y'] - pos['y'] == -1) \
                # or   (ropes[rope-1]['x'] - pos['x'] == -1 and ropes[rope-1]['y'] - pos['y'] == -2) \
                # or   (ropes[rope-1]['x'] - pos['x'] == -2 and ropes[rope-1]['y'] - pos['y'] == -2) :
                #     pos['x'] -= 1
                #     pos['y'] -= 1

                # # Move right
                # elif ropes[rope-1]['x'] - pos['x'] == 2:
                #     pos['x'] += 1

                # # Move left
                # elif ropes[rope-1]['x'] - pos['x'] == -2:
                #     pos['x'] -= 1

                # # Move up
                # elif ropes[rope-1]['y'] - pos['y'] == 2:
                #     pos['y'] += 1

                # # Move down
                # elif ropes[rope-1]['y'] - pos['y'] == -2:
                #     pos['y'] -= 1

                # else:
                #     break

                # if rope == 9:
                #     last_rope_visited.add( (pos['x'],pos['y']) )