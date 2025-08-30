"""Advent of Code: 2019.1.1"""
import sys

def find_numbers(line):

    if not (line[2].isdigit() or line[3].isdigit() or line[4].isdigit()):
        return []

    if line[2].isdigit() and line[3].isdigit() and line[4].isdigit():
        return [int(line[2:5:])]

    if line[3].isdigit():
        if line[4].isdigit():
            if line[5].isdigit():
                return [int(line[3:6:])]
            else:
                return [int(line[3:5:])]
        elif line[2].isdigit():
            if line[1].isdigit():
                return [int(line[1:4:])]
            else:
                return [int(line[2:4:])]
        else:
            return [int(line[3])]

    numbers = []
    if line[2].isdigit():
        if line[1].isdigit():
            if line[0].isdigit():
                numbers.append(int(line[0:3:]))
            else:
                numbers.append(int(line[1:3:]))
        else:
            numbers.append(int(line[2]))

    if line[4].isdigit():
        if line[5].isdigit():
            if line[6].isdigit():
                numbers.append(int(line[4:]))
            else:
                numbers.append(int(line[4:6:]))
        else:
            numbers.append(int(line[4]))

    return numbers

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
    engine_schematic = ["".join([ '.' for _ in range( len(lines[0])+1 ) ])] \
                     + ['.' + line.strip() + '.' for line in lines]         \
                     + ["".join([ '.' for _ in range( len(lines[0])+1 ) ])]

    sum_of_gear_ratios = 0

    for i, line in enumerate(engine_schematic[1:-1],start=1):
        gear_pos = 0
        while gear_pos >= 0:
            gear_pos = line.find('*',gear_pos+1)

            if gear_pos < 0:
                break

            numbers = find_numbers(engine_schematic[i-1][gear_pos-3:gear_pos+4:]) \
                    + find_numbers(engine_schematic[i  ][gear_pos-3:gear_pos+4:]) \
                    + find_numbers(engine_schematic[i+1][gear_pos-3:gear_pos+4:])

            if len(numbers) == 2:
                sum_of_gear_ratios += numbers[0]*numbers[1]

    print(sum_of_gear_ratios)


if __name__ == "__main__":
    main()
