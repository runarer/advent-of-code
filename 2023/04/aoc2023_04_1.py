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

    total_sum = 0

    # Do stuff with lines
    for line in lines:
        winning_numbers_str, card_numbers_str = line.split(':')[1].split("|")
        winning_numbers = {int(n) for n in winning_numbers_str.split()}
        card_numbers = {int(n) for n in card_numbers_str.split()}

        power = len(winning_numbers & card_numbers) - 1
        if power >= 0:
            total_sum += 2**power

        print(f"{winning_numbers} | {card_numbers} : {power} : {total_sum}")
    print(total_sum)


if __name__ == "__main__":
    main()
