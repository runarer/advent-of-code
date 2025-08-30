"""Advent of Code: 2019.1.1"""
import sys

def determine_type(hand):
    return ( 2*max( (hand.count(card) for card in hand if card != '1'),default=0)*hand.count('1') + \
               sum( hand.count(card) for card in hand) )*(10000000000) + \
               sum( ord(card)*(10**((4-i)*2)) for i, card in enumerate(hand) )

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
    transl = str.maketrans("TJQKA","A1CDE")

    hands = [ [ l[0].translate(transl),int(l[1])]for line in lines if (l := line.split()) ]
    sorted_hands = sorted(hands,key=lambda x : determine_type(x[0]))

    total_winnings = 0
    for i, hand in enumerate(sorted_hands,start=1):
        total_winnings += i*hand[1]

    print(total_winnings)

if __name__ == "__main__":
    main()
