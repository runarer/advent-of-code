"""Advent of Code: 2020.13.1"""
import sys

def next_depature(time, interval):
    """ Find the next depature for a bus with interval. """
    while time % interval != 0:
        time += 1

    return time

def main():
    """Start"""
    #get argument
    if len(sys.argv) < 1:
        sys.exit("Usage: python " + sys.argv[0] + " filename")
    filename = sys.argv[1]
    try:
        with open(filename, 'rt', encoding="utf-8") as file:
            lines = file.readlines()
    except IOError as err:
        print(f"{err}\nError opening {filename}. Terminating program.", file=sys.stderr)
        sys.exit(1)

    earliest_depature = int(lines[0])
    
    bus_lines = lines[1].strip().split(',')
    bus_lines = [ int(bus) for bus in bus_lines if bus != 'x']
    bus_next = [  next_depature(earliest_depature,bus) for bus in bus_lines ]
    bus_lines = list(zip(bus_next,bus_lines))
    print(bus_lines)

    wait_time, bus_id = min(bus_lines)
    wait_time -= earliest_depature


    print(bus_id*wait_time)



if __name__ == "__main__":
    main()
