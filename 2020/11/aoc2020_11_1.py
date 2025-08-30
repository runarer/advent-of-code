"""Advent of Code: 2020.11.1"""
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

    # Create starting map
    floor_map = ['.'*(len(lines[0]) + 1)] \
        + [ "".join(['.']+['#' if c == 'L' else c for c in line.strip()]+['.']) for line in lines] \
        + ['.'*(len(lines[0]) + 1)]

    changed = True
    new_floor_map = floor_map.copy()
    nr_rows  = len(floor_map) - 1
    nr_seats = len(floor_map[1]) - 1
    while changed:
        changed = False
        for i in range(1,nr_rows):
            new_floor_map[i] = "."
            for j in range(1,nr_seats):
                if floor_map[i][j] == '.':
                    new_floor_map[i] += "."
                    continue

                # Apply rules
                seats_nearby =   floor_map[i-1][j-1] + floor_map[i-1][j] + floor_map[i-1][j+1] \
                               + floor_map[i][j+1] + floor_map[i][j-1] \
                               + floor_map[i+1][j-1] + floor_map[i+1][j] + floor_map[i+1][j+1]
                taken_seats = seats_nearby.count('#')
                if floor_map[i][j] == 'L' and taken_seats == 0:
                    new_floor_map[i] += '#'
                    changed = True
                    continue
                if floor_map[i][j] == '#' and taken_seats >= 4:
                    new_floor_map[i] += 'L'
                    changed = True
                    continue
                new_floor_map[i] += floor_map[i][j]
            new_floor_map[i] += "."
        floor_map = new_floor_map.copy()

    seats_taken = sum(map(lambda s : s.count('#'), floor_map))
    print(seats_taken)

if __name__ == "__main__":
    main()
