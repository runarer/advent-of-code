"""Advent of Code: 2023.5.2
    There are two way to solve this. We can combine transformation rules into on large one-level set.
    Or we just apply them one by one to the seed ranges.

"""
import sys

def new_ranges(to_transform,transformations):
    final_transformations = []

    next_to_transform = [to_transform]
    for t_start,t_stop, offset in transformations:
        left_to_transform = next_to_transform.copy()
        next_to_transform.clear()

        while left_to_transform:
            next_start, next_stop = left_to_transform.pop(0)

            # No overlap, go to next
            if t_start > next_stop or t_stop < next_start:
                next_to_transform.append( (next_start,next_stop) )
                continue

            # There is an overlap, we need change current range
            # The whole thing is inside
            if t_start <= next_start and t_stop >= next_stop:
                final_transformations.append((next_start+offset,next_stop+offset))
                continue

            # Clip on left side
            if t_start <= next_start:
                final_transformations.append( (next_start+offset,t_stop+offset) )
                if next_start != next_stop:
                    next_to_transform.append( (t_stop+1,next_stop) )
                continue

            # Clip on right side
            if t_start <= next_stop:
                final_transformations.append( (t_start+offset,next_stop+offset) )
                if next_start != next_stop:
                    next_to_transform.append( (next_start,t_start-1) )
                continue

            # The rule tranform an inner part of the range
            if next_start > t_start and next_stop > t_stop:
                next_to_transform.append((next_start,t_start-1))
                final_transformations.append((t_start+offset,t_stop+offset))
                next_to_transform.append((t_stop+1,next_stop))
                continue

    return final_transformations + next_to_transform



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
    seeds = list(map(int,lines[0].split(':')[1].split()))
    #seed_ranges = [ (seeds[i],seeds[i+1]) for i in range(0,len(seeds),2)]
    seed_ranges = list(zip(seeds[::2],seeds[1::2]))

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

    new_seed_ranges = seed_ranges
    for m in maps:
        old_seed_ranges = new_seed_ranges.copy()
        new_seed_ranges.clear()

        for s in old_seed_ranges:
            new_seed_ranges += new_ranges(s,m)

    print(min([ x for x ,_ in new_seed_ranges]))


if __name__ == "__main__":
    main()
