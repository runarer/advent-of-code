"""Advent of Code: 2019.1.1"""
import sys

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
    cycle = 1
    x_register = 1
    signal_sample_set = { x + 20 : 0 for x in range(0,201,40)}

    def sample():
        if cycle in signal_sample_set.keys():
            signal_sample_set[cycle] = cycle * x_register

    for line in lines:
        line = line.strip()

        if line == "noop":
            sample()
        else:
            _, value = line.split()
            sample()
            cycle += 1
            sample()
            x_register += int(value)

        cycle += 1


    print(sum(signal_sample_set.values()))

if __name__ == "__main__":
    main()
