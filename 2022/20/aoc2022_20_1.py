"""Advent of Code: 2019.1.1"""
import sys

class Number:
    """ A double link class. """
    def __init__(self,value):
        self.value = value
        self.prev = self
        self.next = self

    def move(self,steps):
        """ Wraps back and forth """
        if steps != 0:
            self.prev.next = self.next
            self.next.prev = self.prev

            find_next = self.next
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
    number_list = [Number(numbers[0])]

    for i,number in enumerate(numbers[1:],1):
        number_list.append(Number(number))
        number_list[i].prev = number_list[i-1]
        number_list[i-1].next = number_list[i]
    
    number_list[0].prev = number_list[-1]
    number_list[-1].next = number_list[0]

    return number_list

def solve_with_oop(numbers):
    """ Use a naive OOP solution to find the right answer. Optemize later. """
    linked_list = create_list(numbers)

    for number in linked_list:
        number.move(number.value)

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
    numbers = [ int(line.strip()) for line in lines ]
    n_of_numbers = len(numbers)

    solve_with_oop(numbers)
    # decrypted = numbers.copy()
    
    # for number in numbers:
    #     if number == 0:
    #         continue

    #     # Find where the number is now
    #     index = decrypted.index(number)
    #     insert_after = index + number

    #     insert_after = number+index
    #     if insert_after > n_of_numbers:
    #         insert_after %= (n_of_numbers-1)
    #     elif insert_after < n_of_numbers*-1:
    #         insert_after = (abs(insert_after) % (n_of_numbers-1))*-1
    #     if insert_after < 0:
    #         insert_after = (n_of_numbers-1) + insert_after

    # #    print(number,index,insert_after)

    #     if insert_after > index:
    #         decrypted = decrypted[0:index] + decrypted[index+1:insert_after+1] + [number] + decrypted[insert_after+1:]
    #     elif insert_after == 0:
    #         decrypted = decrypted[0:index] + decrypted[index+1:] + [number]
    #     elif insert_after < index:
    #         decrypted = decrypted[0:insert_after] + [number] + decrypted[insert_after:index] + decrypted[index+1:]


        # if insert_after > n_of_numbers:
        #     insert_after %= n_of_numbers
        #     insert_after += 1
        # elif insert_after < 0:
        #     if insert_after < n_of_numbers *-1:
        #         insert_after += n_of_numbers
        #     insert_after += n_of_numbers-1

        
        # if insert_after == 0:
        #     decrypted = decrypted[0:index] + decrypted[index+1:] + [number]
        # elif insert_after < index:
        #     #move backwards
        #     #print("Backwards") # -3 at index 1, 
        #     decrypted = decrypted[0:insert_after] + [number] + decrypted[insert_after:index] + decrypted[index+1:]
        # else:
        #     #move forwards
        #     #print("Forward")
        #     decrypted = decrypted[0:index] + decrypted[index+1:insert_after+1] + [number] + decrypted[insert_after+1:]

        #print(decrypted)
        # Reduce number if needed
        # if number <= n_of_numbers*-1:
        #     number += n_of_numbers
        # if number >= n_of_numbers:
        #     numbrer -= n_of_numbers

        # Cut it in three parts.
        # insert_at = index + number
        # if insert_at < 0:
        #     insert_at += n_of_numbers
        # elif insert_at > n_of_numbers:
        #     insert_at -= n_of_numbers

        # smallest = min(index,insert_at)
        # largest = max(index,insert_at)

        # if insert_at < index:
        #     decrypted = decrypted[0:smallest] + [number] + \
        #                 decrypted[smallest:largest] + decrypted[largest+1:]
        # else:
        #     decrypted = decrypted[0:smallest] + decrypted[smallest+1:largest+1] \
        #                 + [number] + decrypted[largest+1:]

        #print(decrypted)

    # index_of_zero = decrypted.index(0)
    # first = (index_of_zero + 1000) % n_of_numbers
    # second = (index_of_zero + 2000) % n_of_numbers
    # third = (index_of_zero + 3000) % n_of_numbers
    # print(decrypted[first],decrypted[second],decrypted[third])
    # print(sum([decrypted[first],decrypted[second],decrypted[third]]))


if __name__ == "__main__":
    main()

# Correct answers is:
# 7360 -4598 4516
# 7278