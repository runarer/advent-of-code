"""Advent of Code: 2019.1.1"""
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
    seeds = map(int,lines[0].split(':')[1].split())
    maps = []
    current_map = []
    for line in lines[2:]:
        if line[0].isalpha():
            continue

        if line == "\n":
            maps.append(current_map)
            current_map = []
            continue

        destination, source, length = map(int,line.split())
        current_map.append((source,source+length-1,destination-source))
    maps.append(current_map)
    
    #print(maps)

    final_locations = []

    for seed in seeds:
        location = seed
        for dest_map in maps:
            for start,stop,offset in dest_map:
                #print(f'Seed {seed} to {location} ({start},{stop},{offset})')
                if start <= location <= stop:                    
                    location += offset
                    #print(f'Seed {seed} to {location} ({start},{stop},{offset})')
                    break
        final_locations.append(location)
        #print(f'Seed:{seed} to {location})')
    print(min(final_locations))

if __name__ == "__main__":
    main()
