"""Advent of Code: 2024.22.1"""
import sys, functools as f

def next_secret_nr(secret_nr:int) -> int:
    def mix(a:int,b:int) -> int:
        return a ^ b

    def prune(number:int) -> int:
        return (number % 16777216)
    
    next_nr = mix(secret_nr,secret_nr * 64)
    next_nr = prune(next_nr)

    next_nr = mix(next_nr,next_nr // 32)
    next_nr = prune(next_nr)

    next_nr = mix(next_nr,next_nr*2048)
    next_nr = prune(next_nr)

    return next_nr

def generate_numbers(initial, numbers):
    current = initial
    for _ in range(numbers):
        current = next_secret_nr(current)
        yield current


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
    lines = [ int(line.strip()) for line in lines]

    part1 = sum(list(generate_numbers(line,2000))[-1] for line in lines)
    print(f"Part 1: {part1}")

if __name__ == "__main__":
    main()
