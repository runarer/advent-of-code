"""Advent of Code: 2019.1.1"""
import sys, functools as ft

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
    report = [ [int(nr) for nr in line.split()] for line in lines]
    extrapolated_report = []
    for line in report:
        e_line = [line]

        while any(e_line[-1]):
            e_line.append( [ s-f for f,s in zip(e_line[-1],e_line[-1][1:]) ] )
        extrapolated_report.append(e_line)

    fin_sum = sum( ft.reduce(lambda x,y: y[0] - x, reversed(er),0) for er in extrapolated_report)

    print(fin_sum)


if __name__ == "__main__":
    main()


        #extrapolated_line = [line]
        
        #next_line = line
        #while any(next_line):
        #    next_line = [ next_line[i+1] - next_line[i] for i in range(len(next_line)-1)]
        #    extrapolated_line.append(next_line)
        #extrapolated_report.append(extrapolated_line)


    #final_sum = 0
    #for er in extrapolated_report:
        #er[-1].insert(0,0)
        #for i in range(len(er)-2,-1,-1):
        #    er[i].insert(0,er[i][0] - er[i+1][0])        
        #final_sum += ft.reduce(lambda x,y: y[0] - x, reversed(er),0)

    #print( sum( er[0][0] for er in extrapolated_report) )