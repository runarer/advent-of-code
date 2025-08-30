"""AoC day 3,"""
import sys

def get_points(filename):
    """Return a list of 2 2d points."""
    points = []
    with open(filename, 'r') as file:
        for line in file.readlines():
            point = line.strip().replace(" -> ",',').split(',')
            for i, value in enumerate(point):
                point[i] = int(value)
            points.append(point)
    return points

def create_map(points):
    sea_floor_map = [[0 for x in range(1000)] for y in range(1000)]
    for point in points:
        if point[1] == point[3]:
            add = 1
            if point[0] > point[2]:
                add = -1
            for i in range(abs(point[0]-point[2])+1):
                sea_floor_map[point[0]+add*i][point[1]] += 1
            continue
        if point[0] == point[2]:
            add = 1
            if point[1] > point[3]:
                add = -1
            for i in range(abs(point[1]-point[3])+1):
                sea_floor_map[point[0]][point[1]+add*i] += 1
            continue        
    return sea_floor_map

def find_big_points(sea_floor_map):
    count = 0
    for x in sea_floor_map:
        for y in x:
            if y > 1:
                count += 1
    return count


def main():
    """Start"""
    #get argument
    if len(sys.argv) < 1:
        sys.exit("Usage: python " + sys.argv[0] + " filename")
    filename = sys.argv[1]
    try:
        points = get_points(filename)
    except IOError as err:
        print("{}\nError opening {}. Terminating program.".format(err, filename), file=sys.stderr)
        sys.exit(1)
    #Find answer
    sea_floor_map = create_map(points)
    print("Number of overlaps: ",find_big_points(sea_floor_map))


if __name__ == "__main__":
    main()
