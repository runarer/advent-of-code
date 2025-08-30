"""Advent of Code: 2020.9.1"""
import sys

def find_invalid_number(numbers,size_of_preamble):
    """ Find an invalid number in a list"""
    preamble = numbers[0:size_of_preamble]

    for number_to_check in numbers[size_of_preamble:]:
        valid = False

        for x in preamble:
            for y in preamble:
                if x == y:
                    continue
                if x + y == number_to_check:
                    valid = True
                    break
            if valid:
                break

        if not valid:
            return number_to_check

        valid = False

        preamble.pop(0)
        preamble.append(number_to_check)
    return 0

def find_continues_row(numbers, number):
    """ Find a list of continues number that add up to number"""
    sublist = [ numbers[0] ]
    end = 1
    sum_of_sublist = numbers[0]

    while sum_of_sublist != number:
        # If sum is to small; add number
        if sum_of_sublist < number:
            sublist.append( numbers[end] )
            end += 1

        # If sum to large; remove number
        elif sum_of_sublist > number:
            sublist.pop(0)

        sum_of_sublist = sum(sublist)

    return sublist

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

    list_of_number = [ int(line.strip()) for line in lines]

    invalid_number = find_invalid_number(list_of_number,25)
    row = find_continues_row(list_of_number,invalid_number)
    weakness = min(row) + max(row)

    print(weakness)

if __name__ == "__main__":
    main()
