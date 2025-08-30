"""Advent of Code: 2020.11.2"""
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
    nr_rows  = len(floor_map)
    nr_seats = len(floor_map[1])
    print(nr_rows,nr_seats)
    while changed:
        changed = False
        for i in range(1,nr_rows):
            new_floor_map[i] = "."
            for j in range(1,nr_seats):
                if floor_map[i][j] == '.':
                    new_floor_map[i] += "."
                    continue

                # Apply rules
                taken_seats = 0

                # Check left
                for m in range(1,j):
                    check_j = j - m
                    if floor_map[i][check_j] == '#':
                        taken_seats += 1
                        break
                    if floor_map[i][check_j] == 'L':
                        break

                # Check right
                for m in range(j+1,nr_seats):
                    if floor_map[i][m] == '#':
                        taken_seats += 1
                        break
                    if floor_map[i][m] == 'L':
                        break

                # Check above
                for m in range(1,i):
                    check_i = i - m
                    if floor_map[check_i][j] == '#':
                        taken_seats += 1
                        break
                    if floor_map[check_i][j] == 'L':
                        break

                # Check below
                for m in range(i+1,nr_rows):
                    if floor_map[m][j] == '#':
                        taken_seats += 1
                        break
                    if floor_map[m][j] == 'L':
                        break

                # Check top-left
                for m in range(1,nr_seats):
                    check_i = i - m
                    check_j = j - m
                    if check_i == 0 or check_j == 0:
                        break
                    if floor_map[check_i][check_j] == '#':
                        taken_seats += 1
                        break
                    if floor_map[check_i][check_j] == 'L':
                        break

                # Check top-right
                for m in range(1,nr_seats):
                    check_i = i - m
                    check_j = j + m
                    if check_i == 0 or check_j == nr_seats:
                        break
                    if floor_map[check_i][check_j] == '#':
                        taken_seats += 1
                        break
                    if floor_map[check_i][check_j] == 'L':
                        break

                # Check Diagnal bottom-left
                for m in range(1,nr_seats):
                    check_i = i + m
                    check_j = j - m
                    if check_i == nr_rows or check_j == 0:
                        break
                    if floor_map[check_i][check_j] == '#':
                        taken_seats += 1
                        break
                    if floor_map[check_i][check_j] == 'L':
                        break

                # Check Diagnal bottom-right
                for m in range(1,nr_seats):
                    check_i = i + m
                    check_j = j + m
                    if check_i == nr_rows or check_j == nr_seats:
                        break
                    if floor_map[check_i][check_j] == '#':
                        taken_seats += 1
                        break
                    if floor_map[check_i][check_j] == 'L':
                        break

                if floor_map[i][j] == 'L' and taken_seats == 0:
                    new_floor_map[i] += '#'
                    changed = True
                    continue
                if floor_map[i][j] == '#' and taken_seats >= 5:
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
