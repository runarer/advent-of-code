"""
    Advent of Code: 2019.18.2

    Need to work with lines.

    Walls are a set and inside can be created by a breadth first filling algoritm.
    Just need to know a square inside, is (1,1) inside?

    Find square inside:
        index(#).walls
    
"""
import sys
import itertools as it

# Hjelpefunksjoner:

# return overlap range for two range objects or None if no ovelap
# does not handle step!=1
def range_intersect(r1, r2):
    return range(max(r1.start,r2.start), min(r1.stop,r2.stop)) or None

def combine_ranges(r1,r2):
    if any((r1[0] < r2[0] < r1[1], r1[0] < r2[1] < r1[1], r2[0] < r1[0] < r2[1], r2[0] < r1[1] < r2[1])):
        return (min(r1[0],r2[0]),max(r1[1],r2[1]))
    return None

# Gitt en liste med ranges, kombiner overlap.
# Returnerer en ny liste, 
# def combine_ranges(ranges):
#     new_ranges = []
#     old_ranges = ranges.copy()

#     while old_ranges:
#         cur_range = old_ranges.pop()
#         for next_range in old_ranges:
#             if cur_range[1] < next_range[0]:
#                 continue

# Gitt en range og en liste med range, kombiner rangen inn i listen
# slik at det ikke blir noe overflødig.

def shoelace(points):
    double_sum = 0

    for point1, point2 in it.pairwise(points):
        double_sum += (point1[0]*point2[1])-(point1[1]*point2[0])

    return double_sum / 2


def calc_volum2(h_walls,vertical_walls):
    volum = 0
    
    horizontal_walls = h_walls.copy()
    
    walls_to_calc = list(sorted(horizontal_walls.keys()))

    while walls_to_calc:
        wall1 = walls_to_calc.pop()
        wall2 = walls_to_calc[-1]-1

        if walls_to_calc:
            for start,stop in horizontal_walls[wall2]:
                pass

    return volum

def calc_volum(horizontal_walls,vertical_walls):
    volum = 0

    for wall1,wall2 in it.pairwise(sorted(horizontal_walls.keys())):
        print(wall1,wall2)
        for start,stop in horizontal_walls[wall1]:

            # Square
            if (start,stop) in horizontal_walls[wall2]:
                volum += abs(stop - start) * abs(wall2 - wall1)
                horizontal_walls[wall2].remove((start,stop))
                print("Square")
                continue

            # Top hat
            if (wall1,wall2) in vertical_walls[start] and (wall1,wall2) in vertical_walls[stop]:
                volum += abs(stop - start) * (abs(wall2 - wall1))
                print("Top Hat")
 
                first_part = None
                second_part = None
                for wall in horizontal_walls[wall2]:
                    if wall[1] == start:
                        first_part = wall
                        continue
                    if wall[0] == stop:
                        second_part = wall
                horizontal_walls[wall2].remove(first_part)
                horizontal_walls[wall2].remove(second_part)
                horizontal_walls[wall2].append( (first_part[0],second_part[1]) )
                continue


            a = (wall1,start)
            b = (wall1,stop)
            c = (wall2,start)
            d = (wall2,stop)
            print(f"Box ({a}) to ({b})")
            print(f"    ({c}) to ({d})")

            print('\t',vertical_walls[start])
            print('\t',vertical_walls[stop])

            # Calculate volum
            #volum += abs(max(start,stop) - min(start,stop))*abs(wall2-wall1-1)
            #print("\t",start,stop)
            # Add new walls to horizontal_walls[wall2], 
            #horizontal_walls[wall2].append( (start,stop) )

    return volum

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
    instructions =  [ (int(l[2][2:-2],16),l[2][-2]) for line in lines if (l:= line.strip().split())]
    #instructions = [(20000,'0'),(40000,'1'),(10000,'0'),(90000,'1'),(40000,'2'),(90000,'3'),(10000,'0'),(40000,'3')]

    #horizontal_walls = {}
    #vertical_walls = {}


    next_point = (1,1)
    walls = []

    for length,direction in instructions:
        #print(length,direction)
        #next_point = next_point
        if direction == '0': # R
            next_point = (next_point[0],next_point[1]+length)
            # if to[0] in horizontal_walls:
            #     horizontal_walls[ to[0] ].append( (start[1],to[1]) )
            # else:
            #     horizontal_walls[ to[0] ] = [ (start[1],to[1]) ]
            # start = to
        elif direction == '1':# D
            next_point = (next_point[0]+length,next_point[1])
            # if to[1] in vertical_walls:
            #     vertical_walls[ to[1] ].append( (start[0],to[0]) )
            # else:
            #     vertical_walls[ to[1] ] = [ (start[0],to[0]) ]
            # start = to
        elif direction == '2': # L
            next_point = (next_point[0],next_point[1]-length)
            # if to[0] in horizontal_walls:
            #     horizontal_walls[ to[0] ].append( (to[1],start[1]) )
            # else:
            #     horizontal_walls[ to[0] ] = [ (to[1],start[1]) ]
            # start = to
        else: #'3' U
            next_point = (next_point[0]-length,next_point[1])
            # print(to)
            # if to[1] in vertical_walls:
            #     vertical_walls[ to[1] ].append( (to[0],start[0]) )
            # else:
            #     vertical_walls[ to[1] ] = [ (to[0],start[0]) ]
            # start = to
        walls.append(next_point)
    #print(instructions)
    print(walls)
    print(shoelace(walls))
    #print(vertical_walls)
    #print()
    #print(horizontal_walls)
    #print(vertical_walls.keys())

    #print(calc_volum(horizontal_walls,vertical_walls))

    # if (c := combine_ranges((1,3),(0,6))):
    #     print("New: ",c)
    # else:
    #     print("No overlap")
    # if (c := combine_ranges((-3,4),(0,6))):
    #     print("New: ",c)
    # else:
    #     print("No overlap")

if __name__ == "__main__":
    main()

            # for check1,check2 in horizontal_walls[wall2]:
            #     if check1 == start:
            #         if check2 == stop:
            #             # We got full square.
            #             horizontal_walls[wall2].remove( (check1,check2) )
            #             break
            #         start_something = True

            #     elif check1 == stop:
            #         something_start = True

            #     if check2 == start:
            #         something_stop = True
            #     elif check2 == stop:
            #         something_stop = True

            #     if something_start and stop_something:
            #         # A box above a wall.
    
    # tt = {'a':(23,34),'b':(67,45),'c':(2,1),'d':(4,6)}
    # if 34 in ( x for _,x in tt.values()):
    #     print("Found")
