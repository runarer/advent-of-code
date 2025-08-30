import sys

def grow_lantern_fish(fish_pop, days):
    """Grow the fish population for a specific number of days."""
    fish_at_each_stage = [0,0,0,0,0,0,0,0,0]
    for fish in fish_pop:
        fish_at_each_stage[fish] += 1

    for _ in range(days):
        parents = fish_at_each_stage[0]
        #move down
        for day in range(len(fish_at_each_stage)-1):
            fish_at_each_stage[day] = fish_at_each_stage[day+1]
        #new fish
        fish_at_each_stage[8] = parents
        fish_at_each_stage[6] += parents
    return sum(fish_at_each_stage)

def main():
    """Start"""
    #get argument
    if len(sys.argv) < 1:
        sys.exit("Usage: python " + sys.argv[0] + " filename")
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as file:
            lantern_fish = file.readline().strip().split(',')
    except IOError as err:
        print("{}\nError opening {}. Terminating program.".format(err, filename), file=sys.stderr)
        sys.exit(1)
    
    for i,fish in enumerate(lantern_fish):
        lantern_fish[i] = int(fish)

    lantern_fish = grow_lantern_fish(lantern_fish,256)
    print(lantern_fish)
    

if __name__ == "__main__":
    main()