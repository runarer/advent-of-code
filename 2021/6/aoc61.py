import sys

def grow_lantern_fish(fish_pop, days):
    """Grow the fish population for a specific number of days."""
    for _ in range(days):
        new_fish = []
        for i,fish in enumerate(fish_pop):
            if fish == 0:
                fish_pop[i] = 6
                new_fish.append(8)
                continue
            fish_pop[i] -= 1
        fish_pop += new_fish
    return fish_pop

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
    # lantern_fish = grow_lantern_fish(lantern_fish,1)
    # print(len(lantern_fish))
    # print(lantern_fish)
    # lantern_fish = grow_lantern_fish(lantern_fish,1)
    # print(len(lantern_fish))
    # print(lantern_fish)
    lantern_fish = grow_lantern_fish(lantern_fish,256)
    print(len(lantern_fish))
    

if __name__ == "__main__":
    main()