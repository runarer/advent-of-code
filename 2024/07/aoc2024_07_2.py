"""Advent of Code: 2024.7.2"""
import sys

def apply(ans,parts):
    # This should not occure.
    if len(parts) == 0:
        return False
    
    # Done, check if ok
    if len(parts) == 1:
        return parts[0] == ans
    
    if apply(ans-parts[-1],parts[:-1]):
        return True
    
    if ans%parts[-1] == 0:
        if apply(ans//parts[-1],parts[:-1]):
            return True
    
    a = str(ans)
    b = str(parts[-1])    
    if a.endswith(b) and a != b:        
        return apply(int(a.removesuffix(b)),parts[:-1])
                

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

if __name__ == "__main__":
    main()
