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
    cards = [1 for _ in range(len(lines))]

    for card_nr, line in enumerate(lines):
        winning_numbers_str, card_numbers_str = line.split(':')[1].split("|")
        winning_numbers = {int(n) for n in winning_numbers_str.split()}
        card_numbers = {int(n) for n in card_numbers_str.split()}

        new_cards = len(winning_numbers & card_numbers)

        for i in range( card_nr+1, min(card_nr+new_cards+1,len(cards)) ):
            cards[i] += cards[card_nr]

    print(sum(cards))


if __name__ == "__main__":
    main()
