import sys

def find_taxi_value(point1, point2):
    return abs(point1[0]-point2[0]) + abs(point1[1]-point2[1]) + abs(point1[2]-point2[2])

def main():
    """Start"""
    #get argument
    if len(sys.argv) < 1:
        sys.exit("Usage: python " + sys.argv[0] + " filename")
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except IOError as err:
        print("{}\nError opening {}. Terminating program.".format(err, filename), file=sys.stderr)
        sys.exit(1)

    beacons = [ x.strip().split(",") for x in lines]
    beacons = [[int(x) for x in beacon] for beacon in beacons]

    largest = 0
    cor1 = []
    cor2 = []
    for beacon1 in beacons:
        for beacon2 in beacons:
            taxi_value = find_taxi_value(beacon1,beacon2)
            if taxi_value > largest:
                largest = taxi_value
                cor1 = beacon1
                cor2 = beacon2

    print(largest,cor1,cor2)

if __name__ == "__main__":
    main()
