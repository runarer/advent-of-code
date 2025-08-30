"""Advent of Code: 2022.6.2"""
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
    line = lines[0].strip()

    for i in range(14,len(line)):
        if len(set(line[i-14:i])) == 14:
            print(i)
            break


if __name__ == "__main__":
    main()
