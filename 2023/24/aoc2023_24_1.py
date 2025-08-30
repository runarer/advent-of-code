"""Advent of Code: 2019.1.1"""
import sys

type Hail = tuple[int,int,int,int,int,int]

def find_cross_point(hail_one:Hail,hail_two:Hail) -> tuple[int,int]:    
    a,b,_,c,d,_ = hail_one
    e,f,_,g,h,_ = hail_two

    # Are they parallel
    divider = h*c - g*d
    if divider == 0:
        return None

    s = (((e-a)/c - (f-b)/d)*d*c)/divider

    return (e+s*g,f+s*h)

def in_future(hail:Hail,point:tuple[int,int]):
    # Find next point on line, C, by adding directional, B, vector with point vector, A.
    # If CB is bigger than AB then we are moving away from point.
    
    # PROBLEM: Hva hvis et steg går forbi krysspunktet?
    # Eller, hvis krysspunktet er det samme som hail punktet.
    a,b,_,c,d,_ = hail
    e,f = point

    if c > 0 and d > 0:
        return e > a and f > b

    if c < 0 and d < 0:
        return e < a and f < b

    if c > 0 and d < 0:
        return e > a and f < b

    if c < 0 and d > 0:
        return e < a and f > b

def cross_in_box(point,min_value,max_value):
    return (min_value <= point[0] <= max_value) and (min_value <= point[1] <= max_value)

def do_they_cross(hail_one:Hail,hail_two:Hail) -> bool:
    cross_point = find_cross_point(hail_one,hail_two)

    # Parallel
    if not cross_point:
        return False

    # In past
    if not in_future(hail_one,cross_point):
        return False

    if not in_future(hail_two,cross_point):
        return False

    # Outside of box
    if not cross_in_box(cross_point,200000000000000,400000000000000):
        return False

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
    hails = [ tuple(map(int,line.strip().replace('@',',').split(','))) for line in lines]

    crosses = 0
    for i,hail_one in enumerate(hails[:-1]):
        for hail_two in hails[i+1:]:
            if do_they_cross(hail_one,hail_two):
                crosses += 1

    print( crosses )

if __name__ == "__main__":
    main()

# Too low: 11638