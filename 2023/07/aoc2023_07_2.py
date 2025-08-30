"""Advent of Code: 2019.1.1"""
import sys, functools

def determine_type(hand):
    type_of_hand = sum( hand.count(card) for card in hand)

    if 'J' in hand:
        js = hand.count('J')
        if js >= 4:
            type_of_hand = 25
        else:
            m = max( hand.count(card) for card in hand if card != 'J')
            type_of_hand += 2*js*m

    return type_of_hand

def card_value(card):
    return "J23456789TQKA".index(card)

def compare_hands(hand1,hand2):
    hand1_type = determine_type(hand1[0])
    hand2_type = determine_type(hand2[0])

    if hand1_type == hand2_type:
        for i in range(5):
            value1 = card_value(hand1[0][i])
            value2 = card_value(hand2[0][i])

            if value1 == value2:
                continue
            return value1 - value2
        return 0

    return hand1_type - hand2_type

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
    hands = [ [l[0],int(l[1])] for line in lines if (l := line.split()) ]
    sorted_hands = sorted(hands,key=functools.cmp_to_key(compare_hands) )

    total_winnings = 0
    for i, hand in enumerate(sorted_hands,start=1):
        total_winnings += i*hand[1]

    print(total_winnings)


if __name__ == "__main__":
    main()
