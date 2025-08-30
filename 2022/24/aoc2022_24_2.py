"""Advent of Code: 2019.1.1"""
import sys
# Seperate line and colums, can create functions to give blizzard positions in x minutes at coordiate x,y
# class

# Hva med minutes_until_free(row,col,minutes)?

# Er det egentlig mange veier eller bare noen få.
# Unngå kantene, kill path når man ikke kan flytte seg og det kommer en blizzard

# Bredde først blir for stort. Må enten finne måter å kutte dybde først søkenen eller en helt annen
# strategi. Som å finne når hver tile er ledig. Og jobbe bakfra.



class FlatArea:
    """ A class representing the flat area. """
    def __init__(self,blizzard_map) -> None:
        self.blizzard_map = blizzard_map
        self.map_height = len(blizzard_map)
        self.map_width = len(blizzard_map[0])
        self.flat_width = len(blizzard_map[0]) - 2
        self.flat_height = len(blizzard_map) - 2
        self.target_tile = (self.flat_height,self.flat_width)
        self.shortest_path = self.map_height * self.map_width

        self.blizzards_going_right = [ [i for i,c in enumerate(line) if c == '>'] for line in blizzard_map ]
        self.blizzards_going_left = [ [i for i,c in enumerate(line) if c == '<'] for line in blizzard_map ]
        self.blizzards_going_down = [ [ i for i in range(1,self.map_height-1) if self.blizzard_map[i][j] == 'v' ] for j in range(self.map_width) ]
        self.blizzards_going_up = [ [ i for i in range(1,self.map_height-1) if self.blizzard_map[i][j] == '^' ] for j in range(self.map_width) ]

    def is_tile_free(self,row,col,minute) -> bool:
        """ Finds out if there is an blizzard on tile in minutes"""

        # print(row,col,minute)

        if row in [-1,0,self.map_height-1] or col in [-1,0,self.map_width-1]:
            return False

        round_time_hor = (minute % self.flat_width)
        round_time_ver = (minute % self.flat_height)

        right_time_point = col - round_time_hor
        if right_time_point <= 0:
            right_time_point += self.flat_width
        # print((row,col),right_time_point,self.blizzards_going_right[row])
        if right_time_point in self.blizzards_going_right[row]:
            return False


        left_time_point = col + round_time_hor
        if left_time_point > self.flat_width:
            # left_time_point = left_time_point - (self.map_width-left_time_point)
            left_time_point -= self.flat_width
            #print(left_time_point)
        #print((row,col),left_time_point,self.blizzards_going_left[row])
        if left_time_point in self.blizzards_going_left[row]:
            return False

        down_time_point = row - round_time_ver
        if down_time_point <= 0:# self.flat_height:
            down_time_point += self.flat_height
        #print((row,col),down_time_point,self.blizzards_going_down[col])
        if down_time_point in self.blizzards_going_down[col]:
            return False

        up_time_point = row + round_time_ver       
        if up_time_point > self.flat_height:
            up_time_point -= self.flat_height
        #print((row,col),up_time_point,self.blizzards_going_up[col])
        if up_time_point in self.blizzards_going_up[col]:
            return False

        return True

    # def walk(self,row,col,minute):
    #     """ Depth first search for target tile. """
    #     # Lose conditions
    #     ## This path can't be shorter than a allready found path.
    #     if minute >= self.shortest_path:
    #         return []

    #     ## This path cannot reach the target in remaining time
    #     fastest_possibel = (self.flat_height-row) + (self.flat_width-col)
    #     if self.shortest_path < minute + fastest_possibel:
    #         return []

    #     # Win condition
    #     if (row,col) == self.target_tile:
    #         self.shortest_path = min(minute,self.shortest_path)
    #         print("Won -------------------->",minute)
    #         return [(row,col)]

    #     best_path = []
    #     next_moves = [n for n in [(row,col+1),(row+1,col),(row-1,col),(row,col-1)] if self.is_tile_free(*n,minute+1)]
    #     for next_move in next_moves:
    #         a_path = self.walk(*next_move,minute+1)
    #         if a_path:
    #             best_path = [(row,col)] + a_path
        
    #     if not best_path:
    #         # Can we wait?
    #         if self.is_tile_free(row,col,minute+1):
    #             a_path = self.walk(row,col,minute+1)
    #             if a_path:
    #                 best_path = [(row,col)] + a_path

    #     return best_path

    # def draw_blizzards(self,minutes):
    #     """ Draw the blizzards for given minutes """

    #     for minute in range(1,minutes+1):
    #         print("Minute:",minute)
    #         first_line = [ '#' for _ in range(self.map_width)]
    #         first_line[1] = '.'
    #         flat_area = [["#"] + ['B' for _ in range(self.map_width-2)] + ["#"] for _ in range(self.map_height-2)]
    #         flat_area.insert(0,first_line)
            
    #         for i in range(1,self.map_height-1):
    #             for j in range(1,self.map_width-1):
    #                 if self.is_tile_free(i,j,minute):
    #                     flat_area[i][j] = '.'
            
    #         last_line = [ '#' for _ in range(self.map_width)]
    #         last_line[-2] = '.'
    #         flat_area.append(last_line)

    #         for line in flat_area:
    #             print("".join(line))
    #         print("\n")

    def walk_set(self,init_row,init_col,init_minute):
        """ Uses set to do a wide-first-search. """
        expedition = set()
        expedition.add((init_row,init_col))
        minute = init_minute

        while self.target_tile not in expedition:
            expedition_moves = set()
            minute += 1
            for tile in expedition:
                row,col = tile
                expedition_moves.update([n for n in [(row,col+1),(row+1,col),(row,col),\
                                                     (row-1,col),(row,col-1)] if self.is_tile_free(*n,minute)])
            expedition = expedition_moves
            if not expedition:
                return 0
        
        return minute


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
    lines = [line.strip() for line in lines]
    flat_area = FlatArea(lines)
    first_trip = flat_area.walk_set(1,1,1) + 1
    print(first_trip)

    flat_area.target_tile = (1,1)
    minutes = first_trip + 1
    second_trip = 0
    while second_trip == 0:
        # Do we need to wait?    
        while not flat_area.is_tile_free(*flat_area.target_tile,minutes):
            minutes += 1
        second_trip = flat_area.walk_set(flat_area.flat_height,flat_area.flat_width,minutes)
        minutes += 1
    second_trip += 1 # Found target, move off flat area
    
    print(second_trip)

    flat_area.target_tile = (flat_area.flat_height,flat_area.flat_width)
    minutes = second_trip + 1
    third_trip = 0
    while third_trip == 0:
        # Do we need to wait?    
        while not flat_area.is_tile_free(*flat_area.target_tile,minutes):
            minutes += 1
        third_trip = flat_area.walk_set(1,1,minutes)
        minutes += 1
    third_trip += 1 # Found target, move off flat area

    print(third_trip)


if __name__ == "__main__":
    main()
