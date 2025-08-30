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
    list1 = []
    list2= []

    for line in lines:
        a,b = line.split()
        list1.append(int(a))
        list2.append(int(b))
    
    print(sum(abs(a-b) for a,b in zip(sorted(list1),sorted(list2))))

if __name__ == "__main__":
    main()
