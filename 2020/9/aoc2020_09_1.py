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

    invalid_number = find_invalid_number(list_of_number,5)

    print(invalid_number)

if __name__ == "__main__":
    main()
