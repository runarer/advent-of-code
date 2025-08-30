"""Advent of Code: 2020.10.2"""
import sys

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

    # Do stuff with lines
    adapters = [0] + [ int(line.strip()) for line in lines]
    adapters.sort()
    adapters.append(adapters[-1] + 3)

    # Find needed adapters
    needed_adapters = []
    for i in range(1,len(adapters)):
        if adapters[i] - adapters[i-1] == 3:
            needed_adapters.append( (adapters[i-1],adapters[i]) )

    # Reduce needed adapters
    i = 1
    while True:
        #Unpack
        a,b = needed_adapters[i-1]
        c,d = needed_adapters[ i ]
        if (b == c) or (c-b == 1):
            # (a,b)(c,d) => (a,d) if b == c or (c - b) == 1
            needed_adapters = needed_adapters[0:i-1] + [(a,d)] + needed_adapters[i+1:]
        else:
            i += 1
        if i == len(needed_adapters):
            break

    # Her hadde det nok vært bedre å lage en liste for områdene der mans skal velge adaptre.
    # Dette kan lages ac needed_adapters.
    # Så kan man finne min og max ved hjelp av disse nye tuplene.

    # Find min and max adapters between each needed pair of adapters.
    start = 0
    i = 0
    poss = {1:2,2:4,3:7} # Dette er en stygg løsning. Bruk riktig utregning, men den husker jeg ikke
    combies = 1
    for needed in needed_adapters:
        end = needed[0]

        i_start = adapters.index(start)
        i_end = adapters.index(end)

        maxi = len(adapters[i_start+1:i_end])
        # mini = int(maxi/3) # For riktig utregning
        combies *= poss[maxi]

        i += 1
        start = needed[1]

    print(combies)

if __name__ == "__main__":
    main()
