"""Advent of Code: 2019.1.1
    Do not need the path, just the cost.
    So for each grid, we want the smallest cost to get there from start

    When a move is made; three obstacles are placed around and 3 steps away.
    Changing direction removes obstacle.
    Continue moving in the same direction do not move the obstacle in front.
    
"""
import sys
#from queue import PriorityQueue
from dataclasses import dataclass
import heapq

@dataclass(order=True)
class Wagon:
    heat : int
    line : int
    row  : int
    came_from : str
    steps: int


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
    city_heatmap = [ [int(c) for c in line.strip()] for line in lines ]
    city_hm_w = len(city_heatmap[0])
    city_hm_h = len(city_heatmap)

    target_line = city_hm_h-1
    target_row  = city_hm_w-1

    max_cost = 90*city_hm_w*city_hm_h
    heat_cost = [ [ max_cost for _ in line ] for line in city_heatmap ]

    # For each point, I need to know the coordinates, where we came from and how many steps in that direction.
    # Do we need a priority queue based on least accumulated heat.
    #start = Wagon(0,0,0,'S',0) # Heat, line, row, from, steps.

    #next_wagon = PriorityQueue(city_hm_h*2)
    #next_wagon.put(start)

    next_wagon = []
    #heapq.heappush(next_wagon,start)
    heapq.heappush(next_wagon,Wagon(city_heatmap[1][0],1,0,'N',1))
    heapq.heappush(next_wagon,Wagon(city_heatmap[0][1],0,1,'W',1))
    heat_cost[1][0] = city_heatmap[1][0]
    heat_cost[0][1] = city_heatmap[0][1]

    #while not next_wagon.empty():
    while next_wagon:
        #cur_wagon = next_wagon.get()
        cur_wagon = heapq.heappop(next_wagon)
        #print("Cur: ",cur_wagon)

        # Next Wagons
        for line,row,direction,n_dir in [(-1,0,'S','N'),(0,1,'W','E'),(1,0,'N','S'),(0,-1,'E','W')]:
            if n_dir == cur_wagon.came_from:
                continue

            next_line = cur_wagon.line + line
            if (next_line >= city_hm_h) or (next_line < 0):
                continue

            next_row = cur_wagon.row + row
            if (next_row >= city_hm_w) or (next_row < 0):
                continue

            next_steps = cur_wagon.steps + 1 if cur_wagon.came_from == direction else 1
            if next_steps > 3:
                continue

            next_heat = cur_wagon.heat + city_heatmap[next_line][next_row]
            if next_heat < heat_cost[next_line][next_row]:
                heat_cost[next_line][next_row] = next_heat
                #next_wagon.put(e:=Wagon(next_heat,next_line,next_row,direction,next_steps))
                heapq.heappush(next_wagon,e:=Wagon(next_heat,next_line,next_row,direction,next_steps))
                #print("next_wagon",e)

            #next_wagon = Wagon( cur_wagon.heat + city_heatmap[cur_wagon.line+line][cur_wagon.row+row],\
            #                    cur_wagon.line + line, cur_wagon.row + row, direction, \
            #                    cur_wagon.steps + 1 if cur_wagon.came == direction else 0)
    print(heat_cost[-1][-1])
    for l in heat_cost:
        print(l)

        # North
        #if not ((wagon.steps == 3 and wagon.came_from == 'S') or wagon.line < 0 or wagon.came_from == 'N'):            
        #    line = wagon.line - 1
        #    row = wagon.row
        #    came_from = 'S'
        #    steps = wagon.steps + 1 if came_from == wagon.came_from else 0

        #   heat = wagon.heat + city_heatmap[line][row]
        #    if heat < heat_cost[line][row]:
        #        next_grid.put(Wagon(heat,line,row,came_from,steps))



if __name__ == "__main__":
    main()
