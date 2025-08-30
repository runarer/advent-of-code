import sys, re
from typing import Deque, List, Tuple

Rs:List[List[List[int]]] = [[[ 1, 0, 0],[ 0, 1, 0],[ 0, 0, 1]],[[ 0, 0, 1],[ 0, 1, 0],[-1, 0, 0]], #1,6 and 1,2
                            [[-1, 0, 0],[ 0, 1, 0],[ 0, 0,-1]],[[ 0, 0,-1],[ 0, 1, 0],[ 1, 0, 0]], #1,5 and 1,4
                            [[-1, 0, 0],[ 0,-1, 0],[ 0, 0, 1]],[[ 0, 0, 1],[ 0,-1, 0],[ 1, 0, 0]], #3,5 and 3,2
                            [[ 1, 0, 0],[ 0,-1, 0],[ 0, 0,-1]],[[ 0, 0,-1],[ 0,-1, 0],[-1, 0, 0]], #3,6 and 3,4
                            [[ 0, 1, 0],[-1, 0, 0],[ 0, 0, 1]],[[ 0, 0, 1],[-1, 0, 0],[ 0,-1, 0]], #5,1 and 5,2
                            [[ 0,-1, 0],[-1, 0, 0],[ 0, 0,-1]],[[ 0, 0,-1],[-1, 0, 0],[ 0, 1, 0]], #5,3 and 5,4
                            [[ 0, 1, 0],[ 1, 0, 0],[ 0, 0,-1]],[[ 0, 0, 1],[ 1, 0, 0],[ 0, 1, 0]], #6,1 and 6,2
                            [[ 0,-1, 0],[ 1, 0, 0],[ 0, 0, 1]],[[ 0, 0,-1],[ 1, 0, 0],[ 0,-1, 0]], #6,3 and 6,4
                            [[ 0, 1, 0],[ 0, 0,-1],[-1, 0, 0]],[[ 0,-1, 0],[ 0, 0,-1],[ 1, 0, 0]], #4,1 and 4,3
                            [[-1, 0, 0],[ 0, 0,-1],[ 0,-1, 0]],[[ 1, 0, 0],[ 0, 0,-1],[ 0, 1, 0]], #4,5 and 4,6
                            [[ 0, 1, 0],[ 0, 0, 1],[ 1, 0, 0]],[[ 1, 0, 0],[ 0, 0, 1],[ 0,-1, 0]], #2,1 and 2,6
                            [[ 0,-1, 0],[ 0, 0, 1],[-1, 0, 0]],[[-1, 0, 0],[ 0, 0, 1],[ 0, 1, 0]]] #2,3 and 2,5

def multiplie(R: List[List[int]], vec: Tuple[int,int,int]) -> Tuple[int,int,int]:
    new_x = R[0][0]*vec[0] + R[0][1]*vec[1] + R[0][2]*vec[2]
    new_y = R[1][0]*vec[0] + R[1][1]*vec[1] + R[1][2]*vec[2]
    new_z = R[2][0]*vec[0] + R[2][1]*vec[1] + R[2][2]*vec[2]
    return (new_x,new_y,new_z)

def add_vectors(vec1: Tuple[int,int,int], vec2: Tuple[int,int,int]) -> Tuple[int,int,int]:
    return (vec1[0] + vec2[0], vec1[1] + vec2[1], vec1[2] + vec2[2])

def sub_vectors(vec1: Tuple[int,int,int], vec2: Tuple[int,int,int]) -> Tuple[int,int,int]:
    return (vec1[0] + ((-1)*vec2[0]), vec1[1] + ((-1)*vec2[1]), vec1[2] + ((-1)*vec2[2]))

def translate(R:List[List[int]], t:Tuple[int,int,int], point:Tuple[int,int,int]) -> Tuple[int,int,int]:
    return add_vectors(multiplie(R,point),t)

def find_t(R:List[List[int]], v:Tuple[int,int,int], u:Tuple[int,int,int]) -> Tuple[int,int,int]:
    t_x = v[0] - (u[0]*R[0][0]) - (u[1]*R[0][1]) - (u[2]*R[0][2])
    t_y = v[1] - (u[0]*R[1][0]) - (u[1]*R[1][1]) - (u[2]*R[1][2])
    t_z = v[2] - (u[0]*R[2][0]) - (u[1]*R[2][1]) - (u[2]*R[2][2])
    return (t_x,t_y,t_z)

def same_vector(vec1: Tuple[int,int,int], vec2: Tuple[int,int,int]) -> bool:
    if vec1[0] == vec2[0]:
        if vec1[1] == vec2[1] and vec1[2] == vec2[2]:
            return True
        if vec1[1] == vec2[2] and vec1[2] == vec2[1]:
            return True
    if vec1[0] == vec2[1]:
        if vec1[1] == vec2[0] and vec1[2] == vec2[2]:
            return True
        if vec1[1] == vec2[2] and vec1[0] == vec2[1]:
            return True
    if vec1[0] == vec2[2]:
        if vec1[1] == vec2[1] and vec1[2] == vec2[0]:
            return True
        if vec1[1] == vec2[0] and vec1[2] == vec2[1]:
            return True
    return False

def same_beacon(beacon1: List[Tuple[int,int,int]], beacon2: List[Tuple[int,int,int]]) -> bool:
    # Count how many has been checked and if it less than 12 left, abort. Account for found.
    # Can i do the same for inner for loop? No
    left_to_check = len(beacon1)
    same = 0
    
    for vec1 in beacon1:
        for vec2 in beacon2:
            if same_vector(vec1,vec2):
                same += 1
        left_to_check -= 1

        #Check if i can get 12 matches
        if left_to_check + same < 12:
            return False

    return True

def find_distance_between(beacons: List[Tuple[int,int,int]]):
    def to_positive(number: int) -> int:
        if number < 0:
            number = 1000 + abs(number)
        else:
            number = 1000 - number
        return number

    def to_pos_beacon(beacon: Tuple[int,int,int]) -> Tuple[int,int,int]:
        """Moves coordinate to a positive space."""
        return (to_positive(beacon[0]),to_positive(beacon[1]),to_positive(beacon[2]))

    def distance(beacon1: Tuple[int,int,int], beacon2: Tuple[int,int,int]):
        dist0 = max(beacon1[0],beacon2[0]) - min(beacon1[0],beacon2[0])
        dist1 = max(beacon1[1],beacon2[1]) - min(beacon1[1],beacon2[1])
        dist2 = max(beacon1[2],beacon2[2]) - min(beacon1[2],beacon2[2])
        return (dist0,dist1,dist2)

    beacons_positive = [to_pos_beacon(x) for x in beacons]
    return [[ distance(b1,b2) for b2 in beacons_positive] for b1 in beacons_positive]

def build_beacon_lists(lines:List[str]):
    scanners = []
    scanner = -1
    beacon_nr = 0

    for line in lines:
        if line == '\n':
            continue

        new_scanner = re.match(r"--- scanner (\d+) ---", line)
        if new_scanner:
            scanner = int(new_scanner.group(1))
            scanners.append([]) # Do i need this
            beacon_nr = 0
            continue

        #We have a beacon for scanner
        beacon = line.strip().split(',')
        scanners[scanner].append((int(beacon[0]),int(beacon[1]),int(beacon[2])))
        beacon_nr += 1

    return scanners

def check_for_overlap(dist_scanner1, dist_scanner2):
    """Check if scanner1 and scanner2 overlap. If so,
    return true and list of tuples of matches,"""
    matches : Tuple[int,int] = []
    matched = False

    for i, beacon1 in enumerate(dist_scanner1):
        #Here I end up checking beacons that has already been matched
        for j,beacon2 in enumerate(dist_scanner2):
            if same_beacon(beacon1,beacon2):
                matches.append((i,j))
    if matches:
        matched = True

    return matched, matches
    
# def check_for_overlap(dist_scanner1, dist_scanner2):
#     """Check if scanner1 and scanner2 overlap. If so,
#     return true and list of tuples of matches,
#     Very few overlaps, so this optimalization is not needed."""
#     matches : Tuple[int,int] = []
#     matched = False
#     to_match = {x for x in range(len(dist_scanner2))}
#     for i, beacon1 in enumerate(dist_scanner1):
#         #Here I end up checking beacons that has already been matched
#         to_remove = []
#         for j in to_match:
#             if same_beacon(beacon1,dist_scanner2[j]):
#                 matches.append((i,j))
#                 to_remove.append(j)
#         for j in to_remove:
#             to_match.remove(j)
#     if matches:
#         matched = True

#     return matched, matches

# def build_scanner_map(beacons,dist_beacons):
#     scanner_map = beacons[0]
#     scanner_map_dist = dist_beacons[0]
#     left_to_match = {x for x in range(1,len(beacons))}
#     #scanner_positions: List[Tuple[int,int,int]] = [(0,0,0) for _ in range(len(beacons))]

#     overlaps = {}
#     for cur_scanner in range(len(beacons)): #For all scanners
#         matched:List[int] = []
#         for match_with in left_to_match:
#             if cur_scanner == match_with:
#                 continue
#             overlap, matches = check_for_overlap(dist_beacons[cur_scanner], dist_beacons[match_with])
#             if not overlap:
#                 continue
#             # We have overlap,
#             matched.append(match_with)
#             overlaps[(cur_scanner,match_with)] = matches
#             # so translate beacons[match_with] to scanner_map 
#             # and insert them. 
#             # Update scanner_map_distance
#         for match in matched:
#             left_to_match.remove(match)
#         cur_scanner += 1
#     print(overlaps)

def build_scanner_map(beacons,dist_beacons):
    # scanner_map = beacons[0]
    # scanner_map_dist = dist_beacons[0]
    #left_to_match = {x for x in range(1,len(beacons))}
    #scanner_positions: List[Tuple[int,int,int]] = [(0,0,0) for _ in range(len(beacons))]

    overlaps = [ {} for x in range(len(beacons))]
    for cur_scanner in range(len(beacons)): #For all scanners
        matched:List[int] = []
        
        for match_with in range(1,len(beacons)):
            if cur_scanner == match_with:
                continue
            overlap, matches = check_for_overlap(dist_beacons[cur_scanner], dist_beacons[match_with])
            if not overlap:
                continue
            # We have overlap,
            matched.append(match_with)
            overlaps[cur_scanner][match_with] =  matches

        # for match in matched:
        #     left_to_match.remove(match)
        cur_scanner += 1

    #Translate, move to own function?
    next_to_translate = Deque([0])
    #scanners = [(0,0,0) for _ in range(len(beacons))] #trernger jeg dette?


    for i,v in enumerate(overlaps):
        print(i)
        print(v)

    done = [0]
    while next_to_translate:
        scanner = next_to_translate.popleft()

        for new_scanner,matching_beacons in overlaps[scanner].items():
            print("Scanner",scanner,"overlaps with",new_scanner)
            t, R = find_t_and_R(beacons[scanner],beacons[new_scanner],matching_beacons)
            #scanners[new_scanner] = t # change, it is t i think
            
            #Translate
            for i,point in enumerate(beacons[new_scanner]):
                beacons[new_scanner][i] = translate(Rs[R],t,point)

            if new_scanner in done or new_scanner in next_to_translate:
                continue
            done.append(scanner)
            next_to_translate.append(new_scanner)
            



    #print(overlaps)

# def find_t_and_R(beacons_000, beacons_unknown, matching_beacons) -> Tuple[Tuple[int,int,int],int]:
#     """ Prøver alle R for å finne en som gir samme t til alle punktene.
#         Kan det være at flere R kan gi en t?
#     """
#     for R in range(len(Rs)):
#         v0,u0 = matching_beacons[0]
#         t = find_t(Rs[R],beacons_000[v0],beacons_unknown[u0])
#         #print("R",R,"  t",t)

#         for v,u in matching_beacons[1:]:
#             if t != find_t(Rs[R],beacons_000[v],beacons_unknown[u]):
#                 R += 1
#                 break
            
#             return (t,R)
#     print("FEIL")


def find_t_and_R(beacons_000, beacons_unknown, matching_beacons) -> Tuple[Tuple[int,int,int],int]:
    """ Prøver alle R for å finne en som gir samme t til alle punktene.
        Kan det være at flere R kan gi en t?
    """
    found_Rs = []
    found_ts = []
    for R in range(len(Rs)):
        v0,u0 = matching_beacons[0]
        t = find_t(Rs[R],beacons_000[v0],beacons_unknown[u0])
        #print("R",R,"  t",t)

        for v,u in matching_beacons[1:]:
            if t != find_t(Rs[R],beacons_000[v],beacons_unknown[u]):
                R += 1
                break
        else:
            found_Rs.append(R)
            found_ts.append(t)
            
    print(found_Rs)
    return (found_ts[0],found_Rs[0])
    print("FEIL")

# def build_scanner_map(beacons,dist_beacons):
#     scanner_map = beacons[0]
#     scanner_map_dist = dist_beacons[0]
#     left_to_match = {x for x in range(1,len(beacons))}
#     #scanner_positions: List[Tuple[int,int,int]] = [(0,0,0) for _ in range(len(beacons))]

#     overlaps = {}
#     for cur_scanner in range(len(beacons)): #For all scanners
#         for match_with in range(cur_scanner+1,len(beacons)): #Try to match with everyone but it self and previous
#             overlap, matches = check_for_overlap(dist_beacons[cur_scanner], dist_beacons[match_with])
#             if not overlap:
#                 continue
#             # We have overlap,
#             overlaps[(cur_scanner,match_with)] = matches

#             # so translate beacons[match_with] to scanner_map 

#             # and insert them. 
#             # Update scanner_map_distance
#         cur_scanner += 1
#     print(overlaps)

def main():
    """Start"""
    #get argument
    if len(sys.argv) < 1:
        sys.exit("Usage: python " + sys.argv[0] + " filename")
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except IOError as err:
        print("{}\nError opening {}. Terminating program.".format(err, filename), file=sys.stderr)
        sys.exit(1)

    beacons = build_beacon_lists(lines)
    # for s,scanner in enumerate(beacons):
    #     print("--- Scanner", s,"---")
    #     for b,beacon in enumerate(scanner):
    #         print(b,":",beacon[0],beacon[1],beacon[2],)
    dist_beacons = [ find_distance_between(scanner) for scanner in beacons]
    build_scanner_map(beacons,dist_beacons)

    all_unique_beacons = set()
    for scanner in beacons:
        all_unique_beacons.update(scanner)
    print(len(all_unique_beacons))
    
    # with open("beacons1.txt",'w') as fileout:
    #     for beacon in all_unique_beacons:
    #         fileout.write(str(beacon[0])+"," + str(beacon[1]) + "," + str(beacon[2]) + '\n')
    
if __name__ == "__main__":
    main()
