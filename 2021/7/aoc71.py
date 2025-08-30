import sys

def find_least_fuel(submarines):
    min_pos = min(submarines)
    max_pos = max(submarines)

    min_fuel = 0
    for submarine in submarines:
        min_fuel += abs(min_pos-submarine)

    for pos in range(min_pos+1,max_pos):
        fuel_used = 0
        for submarine in submarines:
            fuel_used += abs(pos-submarine)
        if fuel_used < min_fuel:
            min_fuel = fuel_used
        print(fuel_used)

    return min_fuel

def main():
    """Start"""
    #get argument
    if len(sys.argv) < 1:
        sys.exit("Usage: python " + sys.argv[0] + " filename")
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as file:
            crab_in_submarines = file.read().strip().split(',')
    except IOError as err:
        print("{}\nError opening {}. Terminating program.".format(err, filename), file=sys.stderr)
        sys.exit(1)

    crab_in_submarines = [int(x) for x in crab_in_submarines]
    print(find_least_fuel(crab_in_submarines))

if __name__ == "__main__":
    main()
