"""Advent of Code: 2022.13.1"""
import sys
from enum import Enum

class Validation(Enum):    
    Valid = 0
    Invalid = 1
    Undetermined = 2

def compare(left,right):
    """Shut up"""
    print(f"- Compare {left} vs {right}")

    if isinstance(left,int) and isinstance(right,int):
        if left > right:
            print("- Right side is smaller, so inputs are not in the right order")
            return Validation.Invalid
        elif left < right:
            print("- Left side is smaller, so inputs are in the right order")
            return Validation.Valid
        else:
            return Validation.Undetermined

    elif isinstance(left,list) and isinstance(right,list):
        # is one empty?
        if len(left) == 0 and len(right) == 0:
            print("*************** Both are out of items ************")
            return Validation.Undetermined            

        if len(left) == 0:
            print("- Left side ran out of items, so inputs are in the right order")
            return Validation.Valid
        if len(right) == 0:
            print("- Right side ran out of items, so inputs are not in the right order")
            return Validation.Invalid

        smallest_list =  min(len(left),len(right))
        for i in range(smallest_list):
            compared_items = compare(left[i],right[i])
            if compared_items != Validation.Undetermined:
                return compared_items

        if len(left) == len(right):
            return Validation.Undetermined

        if len(left) == smallest_list:
            print("- Left side ran out of items, so inputs are in the right order")
            return Validation.Valid

        if len(right) == smallest_list:
            print("- Right side ran out of items, so inputs are not in the right order")
            return Validation.Invalid
        
    elif isinstance(left,list) and isinstance(right,int):
        print(f"- Mixed types; convert right to [{right}] and retry comparison")
        return compare(left,[right])

    elif isinstance(left,int) and isinstance(right,list):
        print(f"- Mixed types; convert left to [{left}] and retry comparison")
        return compare([left],right)
    else:
        print("Whut", i)

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
    lines = [line.strip() for line in lines]
    pairs = [(eval(lines[x]),eval(lines[x+1])) for x in range(0,len(lines),3)]
    
    valid_pairs = [ compare(*pair) for pair in pairs]
    answer = sum([i+1 for i in range(len(valid_pairs)) if valid_pairs[i] == Validation.Valid])
    print("Answer: ",answer)

if __name__ == "__main__":
    main()
