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
        if border_start_x < 0:
            border_start_x = 0
        border_end_x = self.x + points_from_border
        if border_end_x < 0:
            border_end_x = 0

        return (border_start_x,border_end_x)

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
    for i in range(4000000):
        coverage = [sensor.reach_at(i) for sensor in sensors if sensor.do_it_reach(i)]

        # Now I need to figure out the overlaps
        # If one part is completle within another. Remove it from the list
        #print(coverage)
        non_overlapping_parts = []
        while coverage:
            start = coverage[0][0]
            end = coverage[0][1]
            del coverage[0]

            for part in coverage:
                # if start and end are completly in part, break
                if start >= part[0] and end <= part[1]:            
                    break
                elif start <= part[0] and end >= part[1]:
                    coverage.append((start,end))
                    break
                elif start < part[0] and (end >= part[0] or end >= part[1]):
                    coverage.append((start,max(end,part[1])))                    
                    break
                elif start > part[0] and start <= part[1] and end >= part[1]:
                    coverage.append((part[0],max(end,part[1])))                    
                    break
            else:
                non_overlapping_parts.append((start,end))
        
        if len(non_overlapping_parts) > 1:
            answer = (max(non_overlapping_parts[0][0],non_overlapping_parts[1][0])-1)*4000000 + i
            print(answer)
            break


if __name__ == "__main__":
    main()
