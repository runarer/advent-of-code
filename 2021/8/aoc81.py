import sys

def find_number_of_1478s(numbers):
    count = 0
    for number in numbers:
        length = len(number)
        if (length >= 2 and length <= 4) or length == 7:
            count += 1
    return count

def main():
    """Start"""
    #get argument
    if len(sys.argv) < 1:
        sys.exit("Usage: python " + sys.argv[0] + " filename")
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except IOError as err:
        print("{}\nError opening {}. Terminating program.".format(err, filename), file=sys.stderr)
        sys.exit(1)
    count = 0
    for line in lines:
        splitt_line = line.split('|')
        count += find_number_of_1478s(splitt_line[1].strip().split())
    print(count)

if __name__ == "__main__":
    main()