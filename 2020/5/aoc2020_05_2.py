"""Advent of Code: 2020.1.1"""
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

    boarding_passes = [[ 0 if x in ('F','L') else 1 for x in line.strip()] for line in lines]
    boarding_passes = ["".join([str(elem) for elem in b_pass]) for b_pass in boarding_passes]
    boarding_passes = [(int(b_pass[0:7],2),int(b_pass[7:10],2)) for b_pass in boarding_passes]

    seat_numbers = [ (b_pass[0] * 8) + b_pass[1] for b_pass in boarding_passes]
    seat_numbers.sort()

    first_seat = min(seat_numbers)

    for i,seat in enumerate(seat_numbers):
        if i + first_seat != seat:
            print(seat-1)
            sys.exit(0)


if __name__ == "__main__":
    main()
