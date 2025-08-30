"""Advent of Code: 2024.11.2"""
import sys

calculated = {}

def blinks(stone,blinks_left):
    calculated.clear()
    return blink(stone,blinks_left)

def blink(stone,blinks_left):
    if blinks_left == 0:
        return 1

    if (stone,blinks_left) in calculated:
        return calculated[(stone,blinks_left)]

    if stone == 0:
        digits = blink(1,blinks_left-1)
        calculated[(stone,blinks_left)] = digits
        return digits
    
    stone_str = str(stone)
    stone_digits = len(stone_str)
    if stone_digits % 2 == 0:
        split_at = stone_digits//2

        left_digits = blink(int(stone_str[:split_at]),blinks_left-1)
        right_digits = blink(int(stone_str[split_at:]),blinks_left-1)    

        digits = left_digits + right_digits
        calculated[(stone,blinks_left)] = digits
        return digits  
    
    digits = blink(stone*2024,blinks_left-1)
    calculated[(stone,blinks_left)] = digits
    return digits    
    


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
    stones = list(map(int,lines[0].strip().split()))

    print(sum(blinks(stone,75) for stone in stones))
    

    # The behavior of the stones will always be the same and they are independent from the
    # beginning and when split. So 0 becomes 1, then 2024 into 20 and 24. These are turned into 
    # 2, 0, 2, 4 
    # -> 4048, 1, 4048, 8096 
    # -> 40 , 48, 2024, 40, 48, 80, 96
    # -> 4, 0, 4, 8, 20, 24, 4, 0, 4, 8, 8, 0, 9, 6

    # This need some kind of memoizzas.
    # Can keep record of number and steps. so digit[0] [1,1,1,2,4,4,]
    # This thing is a tree, and I can go depth-first on the left side. this will populate the
    # memoization



if __name__ == "__main__":
    main()