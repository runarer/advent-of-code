"""AoC day 1, read a file and find number of increaing measurments"""
import sys

def get_measurement(filename):
    """Return a list of measurements from given file."""
    with open(filename, 'r') as file:
        measurements = file.read().strip().split('\n')
        measurements = [int(m) for m in measurements]
        return measurements

def get_increases(measurements):
    """Compare measurements"""
    increases = 0
    for i in range(len(measurements)-1):
        increases += measurements[i] < measurements[i+1]
    return increases


def main():
    """Start"""
    #get argument
    if len(sys.argv) < 1:
        sys.exit("Usage: python aoc11.py filename")
    filename = sys.argv[1]
    measurements = []
    #Get measurements
    try:
        measurements = get_measurement(filename)
    except IOError as err:
        print("{}\nError opening {}. Terminating program.".format(err, filename), file=sys.stderr)
        sys.exit(1)
    #Find answer
    increases = get_increases(measurements)
    print("Number of increases: " + str(increases))

if __name__ == "__main__":
    main()
