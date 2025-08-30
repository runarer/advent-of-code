"""Advent of Code: 2019.1.1"""
import sys, math

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
    times = [int(x) for x in lines[0].split(':')[1].split()]
    records = [ int(x) for x in lines[1].split(':')[1].split()]

    #wins = math.prod([ len(list(filter( lambda x: x > records[i],[ ht*(times[i]-ht) for ht in range(1,times[i]) ]))) for i in range(0,len(times))])
    wins = math.prod( len( [ c for ht in range(1,times[i]) if ( c := ht*(times[i]-ht)) > records[i] ] ) for i in range(0,len(times)))
    print(wins)



if __name__ == "__main__":
    main()
