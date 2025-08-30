"""Advent of Code: 2019.1.1"""
import sys

class Number:
    """ A double link class. """
    def __init__(self,value,moves):
        self.value = value
        self.moves = moves
        self.prev = self
        self.next = self

    def move(self):
        """ Wraps back and forth """
        if self.moves != 0:
            self.prev.next = self.next
            self.next.prev = self.prev

            find_next = self.next
            steps = self.moves
            if steps < 0:
                while steps:
                    find_next = find_next.prev
                    steps += 1
            elif steps > 0:
                while steps:
                    find_next = find_next.next
                    steps -= 1

            self.next = find_next
            self.prev = find_next.prev
            self.prev.next = self
            self.next.prev = self

    def value_after(self,steps):
        """  Steps forward and returns value. """
        if steps == 0:
            return self.value
        lookfor = self
        while steps:
            steps -= 1
            lookfor = lookfor.next
        return lookfor.value


    def __str__(self) -> str:
        return str(self.value)

def create_list(numbers):
    """ Create a double list. """
    length_of_list = len(numbers)

    steps = numbers[0]
    if steps > 0:
        steps %= length_of_list-1
    if steps < 0:
        steps = (abs(steps) % (length_of_list-1)) * -1
    number_list = [Number(numbers[0],steps)]

    for i,number in enumerate(numbers[1:],1):
        steps = number
        if steps > 0:
            steps %= length_of_list-1
        if steps < 0:
            steps = (abs(steps) % (length_of_list-1)) * -1
        number_list.append(Number(number,steps))
        number_list[i].prev = number_list[i-1]
        number_list[i-1].next = number_list[i]

    number_list[0].prev = number_list[-1]
    number_list[-1].next = number_list[0]

    return number_list

def solve_with_oop(numbers):
    """ Use a naive OOP solution to find the right answer. Optemize later. """
    linked_list = create_list(numbers)

    for _ in range(10):
        for number in linked_list:
            number.move()

    zero = linked_list[0]
    for n in linked_list:
        if n.value == 0:
            zero = n
            break
    first = zero.value_after(1000)
    second = zero.value_after(2000)
    third = zero.value_after(3000)
    print(first,second,third)
    print(sum([first,second,third]))

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
    numbers = [ int(line.strip())*811589153 for line in lines ]

    solve_with_oop(numbers)

if __name__ == "__main__":
    main()

# Correct answers is:
# 7360 -4598 4516
# 7278