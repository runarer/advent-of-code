"""Advent of Code: 2023.24.2

"""
import sys

def dot(a:list[int],b:list[int]) -> int:
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

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
    hails = [ list(map(int,line.strip().replace('@',',').split(','))) for line in lines]

    org = hails[0]
    second = [ b-a for a,b in zip(org,hails[1])]
    third = [ b-a for a,b in zip(org,hails[3])]
    forth = [ b-a for a,b in zip(org,hails[2])]

    # Find plane defined by origo (first) and a line (second).
    B0 = second[0:3]
    B1 = [ a+b for a,b in zip(B0,second[3:]) ]

    plane_norm = [B0[1]*B1[2]-B0[2]*B1[1],B0[2]*B1[0]-B0[0]*B1[2],B0[0]*B1[1]-B0[1]*B1[0]]

    # Find where and when two points (third and forth) intersects with the plane.
    cp = third[0:3]
    cv = third[3:]
    third_d = dot([B0[0]-cp[0],B0[1]-cp[1],B0[2]-cp[2]],plane_norm) // dot(cv,plane_norm)

    dp = forth[0:3]
    dv = forth[3:]
    forth_d = dot([B0[0]-dp[0],B0[1]-dp[1],B0[2]-dp[2]],plane_norm) // dot(dv,plane_norm)

    third_p = [ a+b*third_d for a,b in zip(cp,cv) ]
    forth_p = [ a+b*forth_d for a,b in zip(dp,dv) ]

    first_p = third_p
    first_d = third_d
    second_p = forth_p

    if third_d > forth_d:
        first_p = forth_p
        first_d = forth_d
        second_p = third_p

    # Divide directional vector of the line on the plane by the time units 
    # between the two points.
    divider = max(third_d,forth_d) - min(third_d,forth_d)

    # Find direction of line between the two points.    
    rock_v = [ (b-a)//divider for a,b in zip(first_p,second_p) ]
    # rock_v_orginal = [ a+b for a,b in zip(rock_v,org[3:]) ]

    # Go backwards
    start = [ a-first_d*b for a,b in zip(first_p,rock_v) ]
    start_orginal = [ a+b for a,b in zip(start,org[:3]) ]

    print(sum(start_orginal))

if __name__ == "__main__":
    main()

# 2165326700354558 :  to high
# 664822352550558
