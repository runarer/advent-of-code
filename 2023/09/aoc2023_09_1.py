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
    report = [ [int(nr) for nr in line.split()] for line in lines]
    extrapolated_report = []
    for line in report:
        extrapolated_line = [line]

        next_line = line
        while any( n != 0 for n in next_line):
            next_line = [ next_line[i+1] - next_line[i] for i in range(len(next_line)-1)]
            extrapolated_line.append(next_line)
        extrapolated_report.append(extrapolated_line)

    for er in extrapolated_report:
        er[-1].append(0)
        for i in range(len(er)-2,-1,-1):
            er[i].append(er[i][-1] + er[i+1][-1])

    print( sum( er[0][-1] for er in extrapolated_report) )

if __name__ == "__main__":
    main()
