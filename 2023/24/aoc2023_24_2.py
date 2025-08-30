"""Advent of Code: 2023.24.2

    Do any line run in parallel?
    Do any lines intersect?
    This will give a plane. 
    All other lines must intersect this plane at some point.

    Can I solve for each axis by them self?


    Hvis vi vet hvor fort linjen beveger seg og når hvert haggel treffes, så kan
    vi finne posisjonen.

    Vi bruteforce direction vector for linjen. Men kun for X og Y.
    Isteden for en linje som treffer alle andre linjer, så gjøres dette om til
    et punkt der alle linjene møtes. Ved å trekke fra den vectoren vi bruteforcer fra
    haggellinjenes directional vector så vil linjene bevege seg mot punktet.
    En linje vil krysse alle andre linjer ved dette punktet. 

    Skjekk for at:
     - Ingen linjer er parallelle.
     - Ingen linjer krysses i fortid.
     - At punktet som krysses er på samme sted som forrige kryssning.

     - Z-Aksen må så finnes, og kontrolleres at alle treffer samme punkt.

    Hva med å bruke den siste linjen som ble skjekket, altså den første som ikke passet,
    som den første til å bli skjekket med neste vektor. Eller som linjen som skjekkes opp mot
    alle de andre. Da må vi håndtere listen med linjer som en sirkulær liste. Husk å ikke 
    skjekke mot seg selv, men å stoppe når man kommer ditt.
"""
import sys
from math import isclose, gcd
from fractions import Fraction as frac

type Hail = tuple[int,int,int,int,int,int]

def find_cross_point(hail_one:Hail,hail_two:Hail) -> tuple[int,int]:
    a,b,_,c,d,_ = hail_one
    e,f,_,g,h,_ = hail_two

    # Are they parallel
    divider = h*c - g*d

    if divider == 0:
        print("Parallell")
        return None

    # if d == 0 or c == 0:
    #     return None
    # print(a,b,c,d,"|",e,f,g,h)
    s = ((e-a)*d - (f-b)*c)/divider
    # print(frac(((e-a)*d - (f-b)*c),divider))
    # print(s)

    return (int(e+s*g),int(f+s*h))
    # return (e+s*g,f+s*h)

def in_future(hail:Hail,point:tuple[int,int]):
    # Find next point on line, C, by adding directional, B, vector with point vector, A.
    # If CB is bigger than AB then we are moving away from point.
    
    # PROBLEM: Hva hvis et steg går forbi krysspunktet?
    # Eller, hvis krysspunktet er det samme som hail punktet.
    
    # behind =  False
    a,b,_,c,d,_ = hail
    e,f = point

    # if (e < a and c < 0) or (f < b and d < 0):
    #     return False
    # return True

    if c > 0 and d > 0:
        return e > a and f > b

    if c < 0 and d < 0:
        return e < a and f < b

    if c > 0 and d < 0:
        return e > a and f < b

    if c < 0 and d > 0:
        return e < a and f > b

def do_they_cross(hail_one:Hail,hail_two:Hail) -> tuple[bool,tuple[int,int]]:
    cross_point = find_cross_point(hail_one,hail_two)
    # print(cross_point)
    # print(f"Hailstone A: {hail_one}")
    # print(f"Hailstone B: {hail_two}")
    # print(f"Cross point: {cross_point}")

    found_crosspoint = False
    # Parallel
    if not cross_point:
        # print("Parallell")
        return (found_crosspoint,cross_point)

    # In past
    if not in_future(hail_one,cross_point):
        # print("Not in future 1")
        return (found_crosspoint,cross_point)

    if not in_future(hail_two,cross_point):
        # print("Not in future 2")
        return (found_crosspoint,cross_point)

    # print("OK")

    # # Parallel
    # if cross_point:
    #     if in_future(hail_one,cross_point) and in_future(hail_two,cross_point):
    #         found_crosspoint = True

    return (found_crosspoint,cross_point)


def sub_vec(hail:Hail,vector:(tuple[int,int,int])) -> Hail:
    return (hail[0],hail[1],hail[2],hail[3]- vector[0],hail[4]- vector[1],hail[5]- vector[2])

def find_vector(hailstorms:list[Hail]):
    vec_found = False

    point = (0,0)
    vec = (0,0,0)

    for i in range(1,1000):
        for j in range(1,1000):
            for vector in [(i,j,0),(-i,j,0),(i,-j,0),(-i,-j,0)]:
                hail_one = None
                hail_two = None

                first_i = 0
                for i,hail in enumerate(hailstorms):
                    hail_one = sub_vec(hail,vector)

                    if hail_one[3] == 0 or hail_one[4] == 0:
                        hail_one = None
                        continue

                    first_i = i
                    break

                for i,hail in enumerate(hailstorms[first_i+1:],start=first_i+1):
                    hail_two = sub_vec(hail,vector)

                    if hail_two[3] == 0 or hail_two[4] == 0:
                        hail_two = None
                        continue
                    first_i = i
                    break

                if hail_one and hail_two:
                    cross,point = do_they_cross(hail_one,hail_two)

                    if not cross:
                        continue

                    tests = 1
                    for hail in hailstorms[first_i+1:]:
                        hail_i = sub_vec(hail,vector)

                        if hail_i[3] == 0 or hail_i[4] == 0:
                            continue

                        cross_i,point_i = do_they_cross(hail_one,hail_i)
                        # print(cross,point,point_i)

                        # if (not cross_i) or point != point_i:
                        if (not cross_i) or not (isclose(point[0],point_i[0],rel_tol=0.02) and isclose(point[1],point_i[1],rel_tol=0.02)):
                            vec_found = False
                            break
                        vec_found = True
                        tests += 1
                        if tests > 1:
                            print("Test",tests)

                    # TESTING
                    # if vector[0] == -3 and vector[1] == 1:
                    #     print("\t",do_they_cross(hail_one,sub_vec(hailstorms[2],vector)))
                    #     print("\t",do_they_cross(hail_one,sub_vec(hailstorms[3],vector)))

                if vec_found:
                    break
            if vec_found:
                break
        if vec_found:
            break
    if vec_found:
        return (point[0],point[1],0,vec[0],vec[1],vec[2])
    return None

def create_search_space(hailstorms:list[Hail]) -> list[list[int]]:
    x_velocity = { v : [] for v in set( h[3] for h in hailstorms )}
    y_velocity = { v : [] for v in set( h[4] for h in hailstorms )}
    z_velocity = { v : [] for v in set( h[5] for h in hailstorms )}

    for hail in hailstorms:
        x_velocity[hail[3]].append(hail[0])
        y_velocity[hail[4]].append(hail[1])
        z_velocity[hail[5]].append(hail[2])

    return [list(x_velocity.values()),list(y_velocity.values()),list(z_velocity.values())]

    # x_space = set()
    # y_space = set()
    # z_space = set()

    # for same_velocity in x_velocity.values():
    #     if len(same_velocity) == 1:
    #         continue
    #     if not x_space:
    #         diff = same_velocity[0] - same_velocity[1]
    #         x_space = 

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
    # print(create_search_space(hails))

    print(find_vector(hails))

if __name__ == "__main__":
    main()
