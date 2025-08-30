import sys

def calc_height_risk(h_map):
    last = len(h_map) - 1
    sum_of_risk_levels = 0
    #calc top
    if h_map[0][0] < h_map[1][0] and h_map[0][0] < h_map[0][1]:
        sum_of_risk_levels += h_map[0][0]+1
    for i in range(1,last):
        if h_map[0][i] < h_map[0][i-1] and h_map[0][i] < h_map[1][i] and h_map[0][i] < h_map[0][i+1]:
            sum_of_risk_levels += h_map[0][i]+1
    if h_map[0][last] < h_map[1][last] and h_map[0][last] < h_map[0][last-1]:
        sum_of_risk_levels += h_map[0][last]+1
    #calc line
    for l_nr in range(1,last):
        if h_map[l_nr][0] < h_map[l_nr+1][0] and h_map[l_nr][0] < h_map[l_nr][1] and h_map[l_nr][0] < h_map[l_nr-1][0]:
            sum_of_risk_levels += h_map[l_nr][0]+1
        for i in range(1,last):
            if h_map[l_nr][i] < h_map[l_nr][i-1] and h_map[l_nr][i] < h_map[l_nr][i+1] and h_map[l_nr][i] < h_map[l_nr+1][i] and h_map[l_nr][i] < h_map[l_nr-1][i]:
                sum_of_risk_levels += h_map[l_nr][i]+1
        if h_map[l_nr][last] < h_map[l_nr-1][last] and h_map[l_nr][last] < h_map[l_nr][last-1] and h_map[l_nr][last] < h_map[l_nr+1][last]:
            sum_of_risk_levels += h_map[l_nr][last]+1     
    #calc bottom
    if h_map[last][0] < h_map[last-1][0] and h_map[last][0] < h_map[last][1]:
        sum_of_risk_levels += h_map[last][0]+1
    for i in range(1,last):
        if h_map[last][i] < h_map[last][i-1] and h_map[last][i] < h_map[last-1][i] and h_map[last][i] < h_map[last][i+1]:
            sum_of_risk_levels += h_map[last][i]+1
    if h_map[last][last] < h_map[last-1][last] and h_map[last][last] < h_map[last][last-1]:
        sum_of_risk_levels += h_map[last][last]+1

    return sum_of_risk_levels

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

    height_map = [[int(c) for c in line.strip()] for line in lines]
    sum_of_risk_levels = calc_height_risk(height_map)
    print(sum_of_risk_levels)


if __name__ == "__main__":
    main()
