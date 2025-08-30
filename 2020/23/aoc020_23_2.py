"""Advent of Code: 2020.23.2
    Drop class, bruk array av next
    så cups[1] = 2, cups[2] = 6 etc.
"""
import sys

def play(cups,start,rounds):
    """ Playes the game with cups for rounds. """
    current_cup = start

    # Pick up three cups
    for _ in range(rounds):
        picked_cups = [cups[current_cup],cups[cups[current_cup]],cups[cups[cups[current_cup]]]]
        cups[current_cup] = cups[ picked_cups[2] ]

        # Find destination cup value
        lookfor = current_cup - 1
        if lookfor == 0:
            lookfor = 1000000
        for _ in picked_cups:
            if lookfor in picked_cups:
                lookfor -= 1
                if lookfor == 0:
                    lookfor = 1000000
            else:
                break

        # Insert cups
        cups[ picked_cups[2] ] = cups[lookfor]
        cups[lookfor] = picked_cups[0]

        current_cup = cups[current_cup]




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

    nr_of_cups = 1000000
    nr_of_rounds = 10000000

    numbers = [int(x) for x in lines[0].strip()]
    cups = [0 for x in numbers]
    cups.append(0)

    for i,nr in enumerate(numbers[:-1]):
        cups[nr] = numbers[i+1]
    cups[ numbers[-1] ] = 10
    for i in range(11,nr_of_cups+1):
        cups.append(i)
    cups.append(numbers[0])

    play(cups,numbers[0],nr_of_rounds)

    # # Find answer, beginning with finding 1
    first = cups[1]
    second = cups[cups[1]]

    print(first*second)

if __name__ == "__main__":
    main()
