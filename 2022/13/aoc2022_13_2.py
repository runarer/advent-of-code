"""Advent of Code: 2022.13.2"""
import sys
from functools import cmp_to_key

def compare(left,right):
    """Shut up"""

    if isinstance(left,int) and isinstance(right,int):
        if left > right:
            return -1
        elif left < right:
            return 1
        else:
            return 0

    elif isinstance(left,list) and isinstance(right,list):
        # is one empty?
        if len(left) == 0 and len(right) == 0:
            return 0

        if len(left) == 0:
            return 1
        if len(right) == 0:
            return -1

        smallest_list =  min(len(left),len(right))
        for i in range(smallest_list):
            compared_items = compare(left[i],right[i])
            if compared_items != 0:
                return compared_items

        if len(left) == len(right):
            return 0

        if len(left) == smallest_list:
            return 1

        if len(right) == smallest_list:
            return -1

    elif isinstance(left,list) and isinstance(right,int):
        return compare(left,[right])

    elif isinstance(left,int) and isinstance(right,list):
        return compare([left],right)
    else:
        print("Whut")

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
    lines = [eval(line.strip()) for line in lines if line != '\n']

    lines.append([[2]])
    lines.append([[6]])

    # Kan sortere lines med compare() som algoritme    
    sorted_packages = sorted(lines, key=cmp_to_key(compare),reverse=True)

    first = 0
    second = 0
    for i,package in enumerate(sorted_packages):
        # print(i, package)
        if package == [[2]]:
            first = i + 1
            continue
        if package == [[6]]:
            second = i + 1
            break

    print(first*second)


if __name__ == "__main__":
    main()
