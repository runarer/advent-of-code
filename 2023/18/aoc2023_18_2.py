"""
    Advent of Code: 2019.18.2

    Need to work with lines.

    
"""
import sys
import itertools as it

def shoelace(points):
    double_sum = 0

    for point1, point2 in it.pairwise(points):
        double_sum += (point1[0]*point2[1])-(point1[1]*point2[0])

    return abs(double_sum / 2)

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
    instructions =  [ (int(l[2][2:-2],16),l[2][-2]) for line in lines if (l:= line.strip().split())]

    # Koordinatenen skal være yttersida av grøfta. Starter med en kubikk.
    # Hvis man står i en 1x1m grav og ser mot øst, så er (1,1) i hjørnet bak deg på
    # venstre side. Yttersida er på venstre side. (1,2) er venstre side foran deg.

    # Når man bygger opp polygonet rundt graven så må man vite neste instruksjon,
    # slik at man kan avgjøre hvor yttersida er.

    start = (1,1)
    calc_starts_at = (1,2)
    walls = [(1,1)]

    for cur_inst, next_inst in it.pairwise(instructions):
        next_point = None

        if cur_inst[1] == '0': # R
            if next_inst[1] == '1': # D
                next_point = (calc_starts_at[0],calc_starts_at[1]+cur_inst[0])
                calc_starts_at = (calc_starts_at[0]+1,calc_starts_at[1]+cur_inst[0])
            elif next_inst[1] == '3': # U
                next_point = (calc_starts_at[0],calc_starts_at[1]+cur_inst[0]-1)
                calc_starts_at = next_point
            else:
                print("If If '0' next_inst[1]")
        elif cur_inst[1] == '1':# D
            if next_inst[1] == '2': # L
                next_point = (calc_starts_at[0]+cur_inst[0],calc_starts_at[1])
                calc_starts_at = (calc_starts_at[0]+cur_inst[0],calc_starts_at[1]-1)
            elif next_inst[1] == '0': # R
                next_point = (calc_starts_at[0]+cur_inst[0]-1,calc_starts_at[1])
                calc_starts_at = next_point
            else:
                print("If If '1' next_inst[1]")
        elif cur_inst[1] == '2': # L
            if next_inst[1] == '3': # U
                next_point = (calc_starts_at[0],calc_starts_at[1]-cur_inst[0])
                calc_starts_at = (calc_starts_at[0]-1,calc_starts_at[1]-cur_inst[0])
                #outside = 'R'
            elif next_inst[1] == '1': # D
                next_point = (calc_starts_at[0],calc_starts_at[1]-cur_inst[0]+1)
                calc_starts_at = next_point
            else:
                print("If If '2' next_inst[1]")
        elif cur_inst[1] == '3': #'3' U
            if next_inst[1] == '0': # R
                next_point = (calc_starts_at[0]-cur_inst[0],calc_starts_at[1])
                calc_starts_at = (calc_starts_at[0]-cur_inst[0],calc_starts_at[1]+1)
            elif next_inst[1] == '2': # L
                next_point = (calc_starts_at[0]-cur_inst[0]+1,calc_starts_at[1])
                calc_starts_at = next_point
            else:
                print("If If '3' next_inst[1]")
        else:
            print("Wrong inst code")

        walls.append(next_point)
    walls.append(start)

    print(shoelace(walls))
    

if __name__ == "__main__":
    main()
