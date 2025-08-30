"""Advent of Code: 2019.1.1"""
import sys

def find_numerical(string, start):
    for i in range(start,len(string)):
        if string[i].isdigit():
            return i
    return -1

def has_symbol(string,start,end):
    pos = start
    while pos <= end:
        if string[pos] != '.' and not string[pos].isdigit():
            return True
        pos += 1
    return False

def find_number_end(string,start):
    while string[start].isdigit():
        start += 1
    return start


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

    # Add a border around map
    engine_schematic = ["".join([ '.' for _ in range( len(lines[0])+1 ) ])] \
                     + ['.' + line.strip() + '.' for line in lines]         \
                     + ["".join([ '.' for _ in range( len(lines[0])+1 ) ])]

    part_sum = 0
    for line_nr, line in enumerate(engine_schematic[1:-1:],start=1):
        # search for numeric
        number_pos = 1
        number = 0
        while number_pos > 0:
            number_pos = find_numerical(line,number_pos)
            if number_pos < 0:
                break

            number_end = find_number_end(line,number_pos)

            # is valid number
            number = int(line[number_pos:number_end:])
            if any([ has_symbol( engine_schematic[line_nr + i], number_pos-1, number_end) for i in range(-1,2)]):
                print(f'Valid part {number}')
                part_sum += number
            else:
                print(f'Not a part {number}')

            number_pos = number_end + 1

    print(part_sum)            




if __name__ == "__main__":
    main()
