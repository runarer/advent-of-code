"""Advent of Code: 2020.1.1"""
import sys

class Cup:
    """ A class for a circular linked list. """
    value = 0
    next = None

    def __init__(self,value):
        self.value = value

    def __str__(self):
        return str(self.value)




def play(cups,rounds):
    """ Playes the game with cups for rounds. """
    current_cup = cups[0]

    # Pick up three cups
    for _ in range(rounds):
        picked_cups = current_cup.next
        current_cup.next = picked_cups.next.next.next

        # Find destination cup value
        lookfor = current_cup.value - 1
        if lookfor == 0:
            lookfor = 9
        for _ in [1,2,3]:
            if picked_cups.value == lookfor or picked_cups.next.value == lookfor \
                                            or picked_cups.next.next.value == lookfor:
                lookfor -= 1
                if lookfor == 0:
                    lookfor = 9

        # Find destination cup
        destination_cup = current_cup.next
        while destination_cup.value != lookfor:
            destination_cup = destination_cup.next

        # Insert cups
        picked_cups.next.next.next = destination_cup.next
        destination_cup.next = picked_cups

        current_cup = current_cup.next




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

    cups = [Cup(int(x)) for x in lines[0].strip()]

    # Create circle
    cups[-1].next = cups[0]
    prev = cups[0]
    for cup in cups[1:]:
        prev.next = cup
        prev = cup

    play(cups,100)

    # Find answer, beginning with finding 1
    cur = cups[0]
    one = None
    for _ in cups:
        if cur.value == 1:
            break
        cur = cur.next

    # Find order of labels, cur is 1
    one = cur
    cur = one.next
    labels = ""
    while  cur != one:
        labels += str(cur.value)
        cur = cur.next

    print(labels)

if __name__ == "__main__":
    main()
