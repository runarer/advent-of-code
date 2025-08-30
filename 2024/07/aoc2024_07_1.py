"""Advent of Code: 2024.7.1"""
import sys

def apply(ans,parts):
    # This chould not occure.
    if len(parts) == 0:
        return False
    
    # Done, check if ok
    if len(parts) == 1:
        return parts[0] == ans
    
    if apply(ans-parts[-1],parts[:-1]):
        return True
    if apply(ans/parts[-1],parts[:-1]):
        return True
  

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
    equations = []
    for line in lines:
        ans,parts = line.split(':')
        ans = int(ans)
        parts = list(map(int,parts.strip().split()))
        equations.append((ans,parts))

    print(sum( ans if apply(ans,parts) else 0 for ans,parts in equations))

    # try every combinations of * and +, recursive?
    # Can start from the end and apply oposite operations one by one.



if __name__ == "__main__":
    main()
