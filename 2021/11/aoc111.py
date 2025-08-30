import sys

def flashes_in_steps(octopuses, steps):
    def flash(x,y):
        if x < 0 or y < 0 or x >= len(octopuses) or y >= len(octopuses):
            return 0
        if octopuses[x][y] == 0: #It has flashed this step
            return 0
        if octopuses[x][y] <= 9: #Adjecent
            octopuses[x][y] += 1
        if octopuses[x][y] > 9:
            octopuses[x][y] = 0
            return flash(x-1,y-1) + flash(x-1,y) + flash(x-1,y+1) + flash(x,y-1) + flash(x,y+1) + flash(x+1,y-1) + flash(x+1,y) + flash(x+1,y+1) + 1
        return 0
    
    flashes = 0

    for _ in range(steps):
        #Step 1, increase energy
        octopuses = list(map(lambda x_line : list(map(lambda x : x + 1, x_line)), octopuses))
        #Step 2, flashes
        for x,line in enumerate(octopuses):
            for y,octopus in enumerate(line):
                if octopus > 9:
                    flashes += flash(x,y)
    return flashes

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
    
    octopuses =  [[int(c) for c in line.strip()] for line in lines]
    steps = 100
    number_of_flashes = flashes_in_steps(octopuses,steps)
    print(number_of_flashes)


if __name__ == "__main__":
    main()
