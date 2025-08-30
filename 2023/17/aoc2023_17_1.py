"""Advent of Code: 2019.1.1
    Do not need the path, just the cost.
    So for each grid, we want the smallest cost to get there from start

    When a move is made; three obstacles are placed around and 3 steps away.
    Changing direction removes obstacle.
    Continue moving in the same direction do not move the obstacle in front.
    
"""
import sys
from queue import PriorityQueue

type HeatMap = list[list[int]]

class DistanceMap:
    def __init__(self,m:HeatMap) -> None:
        self.heat_map = m
        self.height = len(m)
        self.width = len(m[0])

    def dist(self,row:int,col:int) -> int:
        return (self.height - row - 1) + (self.width - col - 1)
    
    def make_neighbors(self,row:int,col:int) -> list[tuple[int,int]]:
        return [ (a,b) for a,b in [(row+1,col),(row,col-1),(row,col+1),(row,col-1)]
                 if (-1 < a < self.height) and (-1 < b < self.width)]

    def n_make_neighbors(self,f_row:int,f_col:int,row:int,col:int) -> list[tuple[int,int]]:
        neighbors = []
        if f_row == row:
            if f_col < col:
                # Moves to right
                neighbors = [(row-1,col),(row-1,col+1),(row-1,col+2),(row+1,col),(row+1,col+1),(row+1,col+2)]
            else:
                # Moves to left
                neighbors = [(row-1,col),(row-1,col-1),(row-1,col-2),(row+1,col),(row+1,col-1),(row+1,col-2)]
        else:
            if f_row < row:
                # Moves down
                neighbors = [(row,col-1),(row+1,col-1),(row+2,col-1),(row,col+1),(row+1,col+1),(row+2,col+1)]
            else:
                # Moves up
                neighbors = [(row,col-1),(row-1,col-1),(row-2,col-1),(row,col+1),(row-1,col+1),(row-2,col+1)]
        return [ (a,b) for a,b in neighbors if (-1 < a < self.height) and (-1 < b < self.width)]

    def goal(self) -> tuple[int,int]:
        return (self.height-1,self.width-1)
    
    def cost(self,row:int,col:int) -> int:
        return self.heat_map[row][col]
    
    def n_cost(self,f_row:int,f_col:int,row:int,col:int,to_row:int,to_col:int) -> int:
        cost = self.heat_map[to_row][to_col]
        if f_row == row:
            j = -1 if f_col < col else 1
            cost += sum( self.heat_map[row][i] for i in range(to_col,col,j) )
        else:
            j = -1 if f_row < row else 1
            cost += sum( self.heat_map[i][col] for i in range(to_row,row,j) )
        # if f_row == row:
        #     if f_col < col:
        #         # Moves to right
        #         cost += sum( self.heat_map[row][i] for i in range(to_col,col,-1) )
        #     else:
        #         # Moves to left
        #         cost += sum( self.heat_map[row][i] for i in range(to_col,col) )
        # else:
        #     if f_row < row:
        #         # Moves down
        #         cost += sum( self.heat_map[i][col] for i in range(to_row,row,-1) )
        #     else:
        #         # Moves up
        #         cost += sum( self.heat_map[i][col] for i in range(to_row,row) )
        return cost

    # def set_from(self,came_from:dict[tuple[int,int],tuple[int,int]],row:int,col:int,to_row:int,to_col:int) -> None:
    #     f_row,f_col = came_from[(row,col)]

    #     if f_row == row:
    #         prev = (row,to_col)
    #         came_from[(to_row,to_col)] = prev

    #         i = -1 if f_col < col else 1

    #         while prev != (row,col):
    #             n = (prev[0],prev[1]+i)
    #             came_from[prev] = n
    #             prev = n
    #     else:
    #         prev = (to_row,col)
    #         came_from[(to_row,to_col)] = (to_row,col)

    #         i = -1 if f_row < row else 1

    #         while prev != (row,col):
    #             n = (prev[0]+i,prev[1])
    #             came_from[prev] = n
    #             prev = n

def set_from(came_from:dict[tuple[int,int],tuple[int,int]],row:int,col:int,to_row:int,to_col:int) -> None:
    prev = (row,col)
    f_row,f_col = came_from[prev]
    i = 0
    j = 0

    if f_row == row:
        prev = (row,to_col)
        i = -1 if f_col < col else 1
    else:
        prev = (to_row,col)
        j = -1 if f_row < row else 1

    came_from[(to_row,to_col)] = prev

    while prev != (row,col):
        # print(prev)
        n = (prev[0]+j,prev[1]+i)
        came_from[prev] = n
        prev = n

def set_cost_so_far(cost_so_far:dict[tuple[int,int],int],f_row:int,f_col:int,row:int,col:int,to_row:int,to_col:int) -> None:
    pass

def a_star(heatmap:HeatMap) -> int:
    d = DistanceMap(heatmap)
    next_sqr = PriorityQueue()
    goal = d.goal()
    came_from : dict[tuple[int,int],tuple[int,int]] = {(0,0):(0,0)}
    cost_so_far : dict[tuple[int,int],int] = {(0,0):0}
    done = set()

    # Add the starting square
    next_sqr.put((d.dist(0,0),(0,0)))

    while not next_sqr.empty():
        pri,cur_sqr = next_sqr.get()
        #print(cur_sqr,pri)


        # An old entry that was replaced with a higher priority
        if cur_sqr in done:
            continue

        if cur_sqr == goal:
            break

        # Make neighbors
        for n in d.make_neighbors(*cur_sqr):
            if n == came_from[cur_sqr]:
                continue

            # Add to queue
            new_cost = cost_so_far[cur_sqr] + d.cost(*n)

            if n not in cost_so_far or new_cost < cost_so_far[n]:
                cost_so_far[n] = new_cost
                priority = new_cost + d.dist(*n)
                next_sqr.put((priority,n))
                came_from[n] = cur_sqr

        done.add(cur_sqr)

    return came_from

def dijkstra(heatmap:HeatMap):
    d = DistanceMap(heatmap)
    frontier = PriorityQueue()

    frontier.put((heatmap[1][0],(1,0)))
    frontier.put((heatmap[0][1],(0,1)))
    came_from = {(1,0):(0,0),(0,1):(0,0)}
    cost_so_far = { (1,0): heatmap[1][0], (0,1): heatmap[0][1]}

    goal = d.goal()

    # draws_left = 4

    while not frontier.empty():# and draws_left > 0:
        # draws_left -= 1
        _,current = frontier.get()

        if current == goal:
            break

        for n in d.n_make_neighbors(*came_from[current],*current):
            # if current == (1,1): print(current,n,came_from)
            new_cost = cost_so_far[current] + d.n_cost(*came_from[current],*current,*n)
            if n not in cost_so_far or new_cost < cost_so_far[n]:
                cost_so_far[n] = new_cost
                priority = new_cost
                frontier.put((priority,n))
                set_from(came_from,*current,*n)

    return came_from, cost_so_far

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
    city_heatmap : HeatMap = [ [int(c) for c in line.strip()] for line in lines ]
    city_hm_w : int = len(city_heatmap[0])
    city_hm_h : int = len(city_heatmap)

    target_line = city_hm_h-1
    target_row  = city_hm_w-1

    came_from,cost_so_far = dijkstra(city_heatmap)

    # print(came_from)
    # print(cost_so_far)


    # d = DistanceMap(city_heatmap)
    # came_from = {(0,0):(0,0),(0,1):(0,0),(1,0):(0,0),(1,1):(1,0)}
    # d.set_from(came_from,*(1,1),*(2,2))
    # print(came_from)

    # path = a_star(city_heatmap)
    # # print(len(path))

    prev = (12,12)
    while prev != (0,0):
        print(prev)
        prev = came_from[prev]


if __name__ == "__main__":
    main()
