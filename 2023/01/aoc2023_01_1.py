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
    sum = 0
    for line in lines:
        # find numbers
        digits = [ c for c in line if c.isdigit() ]
        if len(digits) == 1:
            sum += int(""+digits[0]+digits[0])
        else:
            sum += int(""+digits[0]+digits[-1])
       
    print(sum)

    # A better way to do this is to loop from front until number
    # and loop from back until number, and the add these.
    sum = 0
    for line in lines:        
        for d in line:
            if d.isdigit():
                sum += int(d)*10
                break                
        for d in reversed(line):
            if d.isdigit():
                sum += int(d)
                break
    print(sum)

if __name__ == "__main__":
    main()
