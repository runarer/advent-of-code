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
    numbers = {"one" : 1, "two" : 2, "three" : 3, "four" : 4, "five" : 5,
               "six" : 6, "seven" : 7, "eight" : 8, "nine" : 9 }
    sum = 0
    for line in lines:
        found_first = False
        while not found_first:
            for s, d in numbers.items():
                if line.startswith(s):
                    found_first = True
                    sum += d*10
                    break
            if not found_first and line[0].isdigit():
                sum += int(line[0])*10
                found_first = True
            else:
                line = line[1:]
        
        found_last = False
        while not found_last:
            for s, d in numbers.items():
                if line.endswith(s):
                    found_last = True
                    sum += d
                    break
            if not found_last and line[-1].isdigit():
                sum += int(line[-1])
                found_last = True
            else:
                line = line[:-1]
    print(sum)
    

if __name__ == "__main__":
    main()


# endwith one in dict, no, pop and is popped a digit, no, continue.