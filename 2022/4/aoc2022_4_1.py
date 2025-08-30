"""Advent of Code: 2022.4.1"""
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
    overlapping_pairs = 0
    for line in lines:
        elf1, elf2 = line.strip().split(',')
        elf1_start, elf1_stop = map(int, elf1.split('-'))
        elf2_start, elf2_stop = map(int, elf2.split('-'))
        if (elf1_start >= elf2_start and elf1_stop <= elf2_stop) or (elf2_start >= elf1_start and elf2_stop <= elf1_stop):
            overlapping_pairs += 1

    # pairs = [ [first.split('-'), second.split('-')] for line in lines for first,second in [line.strip().split(',')] ]
    # #pairs = [ int(s) for pair in pairs for elf in pair for s in elf]
    # pairs = [[ [int(s) for s in elf] for elf in pair ] for pair in pairs]
    # #pairs = [[ [int(s) for s in elf] for elf in [first.split('-'), second.split('-')] ] for first,second in [line.strip().split(',') for line in lines]]
    # #print(pairs)
    # #assignments = [ assignment for pair in pairs for assignment in pair ] # for pair in d: for assignment in pair: append(assignment)
    # #print(assignments)

    # overlapping_pairs = 0
    # for elf1,elf2 in pairs:
    #     elf1_start,elf1_stop = elf1
    #     elf2_start,elf2_stop = elf2
    #     if (elf1_start >= elf2_start and elf1_stop <= elf2_stop) or (elf2_start >= elf1_start and elf2_stop <= elf1_stop):
    #         print(elf1,elf2)
    #         overlapping_pairs += 1

    print(overlapping_pairs)



if __name__ == "__main__":
    main()
