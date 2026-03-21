"""    
    Skritt vil være Even eller Odd. Trenger kun nye skritt utover. 


    Viktige observasjoner:
        Input er 131x131.
        Det er 65 tegn fra sentrum til alle fire sider.
        Antall skritt som skal taes er 26501365.
        Hvis vi tar 26501365 mod 131 så får vi 65.
        Siden vi begynner i senter av første så får slutter vi på kanten
        av de siste kvadratet.

        Det er 14 kvadrat med ulike steps: 
            CenterNorth = 5522, CenterEast = 5534, CenterSouth = 5518, CenterWest = 5506,
            Fulleven = 7335, FullOdd = 7320 (center is fullodd),
            NorthEastTiny = 935, NorthEastChipped = 6427, SouthEastTiny = 931, SouthEastChipped = 6427,
            NorthWestTiny = 932, NorthWestChipped = 6415, SouthWestTiny = 937, SouthWestChipped = 6411,
        Disse kan kalkuleres og totalen kan så regnes ut.

    Research:
        For å få noe å sammenligne resultater med så laget jeg en 
        5x5 versjon av kartet. Denne ble input på en kjøring med 
        65+131+131 steg. 
        Alle step ble markert med en 'O' og skrevet ut i en fil.
        Filen var kun for å se at ting var riktig.
        Antall Oer ble så telt for hvert av de 25 kvadratene.
        Disse tallene er alt som kreves for å regne ut totalen, men ideen
        er å bruke disse til å sjekke at utregningene er riktige.

"""
import sys

def countOs(lines, startRow,startCol):
    return sum( line[startCol:startCol+131].count('O') for line in lines[startRow:startRow+131])

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

    # lines = [list(line.strip()) for line in lines]
    lines = [list(line.strip()*5) for line in lines*5]

    # with open("output.txt","w") as f:
    #     for line in lines:
    #         f.write(line+'\n')

    # Do stuff with lines
    rocks = set()
    start = None

    for i,line in enumerate(lines):
        for j,c in enumerate (line):
            start = (327,327)
            # if c == 'S':
            #     start = (i,j)
            #     print(start)
            # elif c == '#':
            if c == '#':
                rocks.add( (i,j) )

    steps = set()
    steps.add(start)
    for _ in range(65+131+131):
        next_steps = set()

        for s in steps:
            for ns in [(s[0]-1,s[1]),(s[0],s[1]+1),(s[0]+1,s[1]),(s[0],s[1]-1)]:
                if ns[0] < 0 or ns[0] >= len(lines) or ns[1] < 0 or ns[1] >= len(lines):
                    continue
                if ns not in rocks:
                    next_steps.add(ns)
        steps = next_steps

    print(len(steps))

    for (l,r) in steps:
        if lines[l][r] == '#':
            print("ERROR")
        lines[l][r] = 'O'

    for row in range(5):
        for col in range(5):
            os = countOs(lines,131*row,131*col)
            print(f"Row: {row}; Col: {col}; Steps {os}")

    # with open("allsteps.txt", 'w') as f:
    #     for li in lines:
    #         f.write("".join(li)+'\n')


if __name__ == "__main__":
    main()
