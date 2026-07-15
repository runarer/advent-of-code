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
    def last_digit(s:int) -> int:
        return int(str(s)[-1])

    first_sn = initial
    first_ld = last_digit(first_sn)

    second_sn = next_secret_nr(first_sn)
    second_ld = last_digit(second_sn)

    third_sn = next_secret_nr(second_sn)
    third_ld = last_digit(third_sn)

    forth_sn = next_secret_nr(third_sn)
    forth_ld = last_digit(forth_sn)

    first_change = second_ld - first_ld
    second_change = third_ld - second_ld
    third_change = forth_ld - third_ld

    last_sn = forth_sn
    last_ld = forth_ld

    for _ in range(numbers):
        next_sn = next_secret_nr(last_sn)
        next_ld = last_digit(next_sn)
        last_change = next_ld - last_ld

        yield ((first_change,second_change,third_change,last_change),next_ld)

        first_change = second_change
        second_change = third_change
        third_change = last_change
        

        last_ld = next_ld
        last_sn = next_sn

def create_seller_table(initial_nr:int,numbers:int) -> dict[tuple[int,int,int,int],int]:
    table = {}

    for changes, bananas in generate_numbers(initial_nr,numbers-3):
        # monkey takes the first occurence of change, so skip later ones
        if changes in table:
            continue
        table[changes] = bananas

    return table

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

    # create table for all the sellers with changes and bananas at change
    sellers = [ create_seller_table(line,2000) for line in lines ]

    # make a set of all changes
    all_changes = set( change for seller in sellers for change in seller)

    # check all changes for the best one
    max_bananas = 0
    for change in all_changes:
        bananas = sum( seller[change] for seller in sellers if change in seller)
        max_bananas = max(max_bananas,bananas)

    print(f"Part 2: {max_bananas}")

if __name__ == "__main__":
    main()
