"""Advent of Code: 2022.4.2"""
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
    overlapping_pairs = len(lines)
    for line in lines:
        elf1, elf2 = line.strip().split(',')
        elf1_start, elf1_stop = map(int, elf1.split('-'))
        elf2_start, elf2_stop = map(int, elf2.split('-'))        
        if elf2_stop < elf1_start or elf2_start > elf1_stop:
            overlapping_pairs -= 1


    # Do stuff with lines
    # pairs = [ [first.split('-'), second.split('-')] for line in lines for first,second in [line.strip().split(',')] ]
    # pairs = [[ [int(s) for s in elf] for elf in pair ] for pair in pairs]

    # overlapping_pairs = len(pairs)
    # for elf1,elf2 in pairs:
    #     elf1_start,elf1_stop = elf1
    #     elf2_start,elf2_stop = elf2
    #     if (elf2_start < elf1_start and elf2_stop < elf1_start) or (elf2_start > elf1_stop and elf2_stop > elf1_stop):
    #         print(elf1,elf2)
    #         overlapping_pairs -= 1

    print(overlapping_pairs)


if __name__ == "__main__":
    main()
