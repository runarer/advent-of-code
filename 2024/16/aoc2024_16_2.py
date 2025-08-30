"""Advent of Code: 2024.16.1
    This code is just terribly organized. It got worse with part 2.
    Good Job!
"""
import sys
from queue import PriorityQueue, Queue
    
directions = {"North":(-1,0),"East":(0,1),"South":(1,0),"West":(0,-1)}

# For each block(or node) keep a list of parent { (row,col,score) : [(row,col)] }


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
    maze = [ [ c for c in line.strip() ] for line in lines ]
    start = (0,0)
    end = (0,0)
    
    # Find start, find end
    for row, line in enumerate(maze):
        if 'S' in line:
            start = (row,line.index('S'))
        if 'E' in line:
            end = (row,line.index('E'))

    unvisited = PriorityQueue()
    unvisited.put( (0,start,'East',0,0) )
    scores = {d:[ [1000000000 for _ in line] for line in maze] for d in directions.keys()}

    parent = {(start[0],start[1],0):[(0,0,0)]}

    while unvisited:
        score,block, direction, steps, turns = unvisited.get()

        if block == end:
            print(score,steps,turns)

            backtrack_list = [(block[0],block[1],score)]            
            all_blocks = set()

            while backtrack_list:
                curr = backtrack_list.pop(0)

                if curr == (0,0,0):
                    break
                
                all_blocks.add( (curr[0],curr[1]) )

                parents = parent[curr]
                for p in parents:
                    backtrack_list.append(p)
            print(len(all_blocks))
            break
        
        for new_direction, offset in directions.items():
            # is this a wall
            new_location = (block[0]+offset[0],block[1]+offset[1])

            if maze[new_location[0]][new_location[1]] == '#':
                continue
            
            cost = score + 1
            new_steps = steps + 1
            new_turns = turns

            # Dette kan forenkles ved å bruke 0,1,2,3 for directions.
            # Double turn are turn-around and should not happend.
            if direction != new_direction:
                if  direction == "North":
                    if new_direction == "South":
                        continue
                    else:
                        cost += 1000
                        new_turns += 1
                elif  direction == "East":
                    if new_direction == "West":
                        continue
                    else:
                        cost += 1000
                        new_turns += 1
                elif  direction == "South":
                    if new_direction == "North":
                        continue
                    else:
                        cost += 1000
                        new_turns += 1
                elif  direction == "West":
                    if new_direction == "East":
                        continue
                    else:
                        cost += 1000
                        new_turns += 1

            curr = (new_location[0],new_location[1],cost)
            par = (block[0],block[1],score)
            if curr in parent:
                parent[curr].append(par)
            else:
                parent[curr] = [par]

            if cost < scores[new_direction][new_location[0]][new_location[1]]:
                scores[new_direction][new_location[0]][new_location[1]] = cost
                unvisited.put((cost,new_location,new_direction,new_steps,new_turns))


if __name__ == "__main__":
    main()
