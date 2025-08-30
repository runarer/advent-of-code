"""Advent of Code: 2019.1.1
    Can I use bit operations?
     A map for stones.
     A map for bulders.

     1.000.000.000

"""
import sys

def calc_load(platform):
    return sum(p.count('O')*(i+1) for i,p in enumerate(reversed(platform)))

def flip_north(platform):
    for j in range(len(platform[0])):
        next_moves_to = 0

        for i,p in enumerate(platform):
            if p[j] != '.':
                if p[j] == '#':
                    next_moves_to = i + 1
                else:
                    p[j] = '.'
                    platform[next_moves_to][j] = 'O'
                    next_moves_to += 1

def flip_east(platform):
    for r in platform:
        next_moves_to = len(r)-1

        for j in range(len(r)-1,-1,-1):
            if r[j] != '.':
                if r[j] == '#':
                    next_moves_to = j - 1
                else:
                    r[j] = '.'
                    r[next_moves_to] = 'O'
                    next_moves_to -= 1


def flip_south(platform):
    for j in range(len(platform[0])):
        next_moves_to = len(platform)-1

        for i in range(len(platform)-1,-1,-1):
            if platform[i][j] != '.':
                if platform[i][j] == '#':
                    next_moves_to = i - 1
                else:
                    platform[i][j] = '.'
                    platform[next_moves_to][j] = 'O'
                    next_moves_to -= 1

def flip_west(platform):
    for r in platform:
        next_moves_to = 0

        for j,c in enumerate(r):
            if c != '.':
                if c == '#':
                    next_moves_to = j + 1
                else:
                    r[j] = '.'
                    r[next_moves_to] = 'O'
                    next_moves_to += 1

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
    platform = [list(line.strip()) for line in lines]

    try_loops = 200
    loops = 1000000000

    loads = [ 0 for _ in range(try_loops)]

    for i,_ in enumerate(loads):
        flip_north(platform)
        flip_west(platform)
        flip_south(platform)
        flip_east(platform)

        loads[i] = calc_load(platform)

    repeats = []
    for i,l in enumerate(reversed(loads)):
        if l == loads[-1]:
            repeats.append(i)

    number_between = repeats[1] - repeats[0]
    for i,e in enumerate(repeats[1:-1],start=1):
        if repeats[i+1] - e != number_between:
            print("wrong")

    index = ( (loops-1) - (try_loops-1)  ) % number_between
    print(loads[(try_loops-number_between-1)+index])

if __name__ == "__main__":
    main()

# 98943
# 95254 Right!