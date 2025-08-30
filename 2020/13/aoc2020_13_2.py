"""Advent of Code: 2020.13.2"""
import sys

def next_depature(time, interval):
    """ Find the next depature for a bus with interval. """
    while time % interval != 0:
        time += 1

    return time

def merge_buses(bus_1,bus_2):
    """Merges to buses into one new bus"""
    bus_1_round_time, bus_1_time = bus_1
    bus_2_round_time, bus_2_time = bus_2

    while bus_1_time != bus_2_time:
        while bus_1_time < bus_2_time:
            bus_1_time += bus_1_round_time
        while bus_2_time < bus_1_time:
            bus_2_time += bus_2_round_time

    return (bus_1_round_time*bus_2_round_time,bus_1_time)

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

    bus_lines = lines[1].strip().split(',')

    bus_depature = list(zip( bus_lines,range(len(bus_lines)) ))
    bus_depature = [ (int(bus_id),-1*offset) for bus_id,offset in bus_depature if bus_id != 'x' ]

    buses = bus_depature.copy()
    while len(buses) > 1:
        new_buses = []
        while len(buses) > 1:
            new_buses.append(merge_buses(buses.pop(0),buses.pop(0)))
        buses += new_buses
    
    print(buses[0][1])


if __name__ == "__main__":
    main()
