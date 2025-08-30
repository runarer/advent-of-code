"""Advent of Code: 2019.1.1"""
import sys
import re

class Sensor:
    """Class for sensors"""
    def __init__(self,x,y,beacon_x,beacon_y):
        self.x = x
        self.y = y
        self.beacon_x = beacon_x
        self.beacon_y = beacon_y

        self.reach = abs(x-beacon_x)+abs(y-beacon_y)
        self.y_max = y + self.reach
        self.y_min = y - self.reach

    def __str__(self):
        return f"Sensor at ({self.x},{self.y}) sees beacon at ({self.beacon_x},{self.beacon_y}) at a distance {self.reach}"

    def do_it_reach(self,y_value):
        """ Return True if sensor can see y_value"""
        return y_value <= self.y_max and y_value >= self.y_min

    def reach_at(self,y_value):
        """ Return a tuple of start and end for reach at y """
        # at y_min or y_max there are one point (x,y+reach)
        # at y_min+1 or y_max-1 there are two more points (x-1,y+reach)(x,y+reach)(x+1,y+reach)
        # Im only intrested in x values on outer parts.
        # Get smallest of y_min 
        points_from_border = min(abs(self.y_min-y_value),abs(self.y_max-y_value))
        border_start_x = self.x - points_from_border
        border_end_x = self.x + points_from_border

        return (border_start_x,border_end_x)

    # def rotate_45(self):
    #     """Something"""
    #     # sensor forblir
    #     # Beacon blir top right corner
    #     # Find top right corner
    #     top_right = (self.beacon_x,self.beacon_y)
    #     if self.beacon_x > self.x:
    #         if self.beacon_y < self.y:
    #             top_right = (self.beacon_x,self.beacon_y + ( self.reach - (self.beacon_x-self.x) ))
    #     else:
    #         if self.beacon_y > self.y:
    #             top_right = (self.beacon_x + abs(self.x-self.beacon_x),self.beacon_y)
    #         else:
    #             top_right = (self.beacon_x + abs(self.x-self.beacon_x),self.beacon_y + abs(self.y-self.beacon_y))

    #     #top_right = (self.beacon_x,self.beacon_y)
    #     botttom_left = (self.x - abs(top_right[0]-self.x),top_right[1] - abs(top_right[1] - self.y))
    #     #bottom_right = (top_right[0],top_right[1] - (top_right[1] - self.y)*2)
    #     #top_left = (self.x - (top_right[0]-self.x)*2, top_right[1])
    #     #botttom_left = (top_left[0],bottom_right[1])
    #     return (top_right[0],top_right[1],botttom_left[0],botttom_left[1])


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
    #lines = [ line.strip() for line in lines ]

    sensors = []

    for line in lines:
        results = re.match(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)",line.strip())
        if results:
            # numbers = map(int,results.groups())
            # sensor_x,sensor_y,beacon_x,beacon_y = list(numbers)
            sensor_x,sensor_y,beacon_x,beacon_y = results.groups()
            # sensors[(int(sensor_x),int(sensor_y))] = (int(beacon_x),int(beacon_y))
            sensors.append(Sensor(int(sensor_x),int(sensor_y),int(beacon_x),int(beacon_y)))
        else:
            print("No regex match for: ",line)

    # max_coordiante = 4000000
    # max_coordiante = 20

    blocks = []
    triangles = []

    # For each sensor get boxes and triangles, do not include that that's outside of search area
    # 
    # For each block remove overlap. Create new blocks as needed.
    # 
    # For each triangle, remove overlap with blocks, create new triangle and blocks as needed.

    

    # for i in range(max_coordiante):
    #     start = 0
    #     end = max_coordiante
    #     check_after = []

    #     for sensor in sensors:
    #         if sensor.do_it_reach(i):
    #             sensor_start,sensor_end = sensor.reach_at(2000000)


    # # Now I need to figure out the overlaps
    # # If one part is completle within another. Remove it from the list
    # print(coverage)
    # non_overlapping_parts = []
    # overlap = True
    # while overlap:
    #     start = coverage[0][0]
    #     end = coverage[0][1]
    #     del coverage[0]
    #     overlap = False

    #     print("Testing: ",start,end)
    
    #     for part in coverage:
    #         # if start and end are completly in part, break
    #         if start >= part[0] and end <= part[1]:
    #             overlap  = True
    #             break
    #         elif start < part[0] and (end >= part[0] or end >= part[1]):
    #             coverage.append((start,max(end,part[1])))
    #             overlap = True
    #             break
    #         elif start > part[0] and end >= part[1]:
    #             coverage.append((part[0],max(end,part[1])))
    #             overlap = True
    #             break
    #     else:
    #         non_overlapping_parts.append((start,end))

    # print(non_overlapping_parts)
    # start,end = non_overlapping_parts[0]
    # print(abs(end-start))

if __name__ == "__main__":
    main()
