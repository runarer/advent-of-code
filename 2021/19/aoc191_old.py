import enum
import sys, re
from typing import List

def same_vector(vec1: dict, vec2: dict) -> bool:
    if vec1['x'] == vec2['x']:
        if vec1['y'] == vec2['y'] and vec1['z'] == vec2['z']:
            return True
        if vec1['y'] == vec2['z'] and vec1['z'] == vec2['y']:
            return True
    if vec1['x'] == vec2['y']:
        if vec1['y'] == vec2['x'] and vec1['z'] == vec2['z']:
            return True
        if vec1['y'] == vec2['z'] and vec1['x'] == vec2['y']:
            return True
    if vec1['x'] == vec2['z']:
        if vec1['y'] == vec2['y'] and vec1['z'] == vec2['x']:
            return True
        if vec1['y'] == vec2['x'] and vec1['z'] == vec2['y']:
            return True
    return False

def same_beacon(beacon1: List[dict], beacon2: List[dict]) -> bool:
    same = 0
    for vec1 in beacon1:
        for vec2 in beacon2:
            if same_vector(vec1,vec2):
                same += 1
    if same >= 12:
        return True
    return False

def find_distance_between(beacons: List[dict]):
    def to_positive(beacon: dict) -> dict:
        """Moves coordinate to a positive space."""
        tranformed_beacon = {}
        for axe, number in beacon.items():
            if number < 0:
                tranformed_beacon[axe] = 1000 + abs(number)
            else:
                tranformed_beacon[axe] = 1000 - number
        return tranformed_beacon

    def distance(beacon1: dict, beacon2: dict):
        dist = {}
        for axe in beacon1:
            dist[axe] = max(beacon1[axe],beacon2[axe]) - min(beacon1[axe],beacon2[axe])
        return dist

    beacons_positive = [to_positive(x) for x in beacons]
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
        scanners[scanner].append({'x': int(beacon[0]),'y': int(beacon[1]),'z': int(beacon[2]),})
        #scanners[scanner].append((int(beacon[0]),int(beacon[1]),int(beacon[2])))
        beacon_nr += 1

    return scanners

def build_scanner_map(beacons,dist_beacon):
    scanner_map = set(beacons[0])
    left_to_match = [x for x in range(1,len(beacons))]

    print(scanner_map)
    print(left_to_match)
    #for 

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
    #         print(b,":",beacon['x'],beacon['y'],beacon['z'],)
    dist_beacons = [ find_distance_between(scanner) for scanner in beacons]
    build_scanner_map(beacons,dist_beacons)
    # for s,scanner in enumerate(dist_beacons):
    #     print("--- Scanner", s,"---")
    #     for b,beacon in enumerate(scanner):
    #         print("Beacon:", b)
    #         print(beacon)

    #Compare Distance vectors for beacons

    #for all beacon n in scannner i
    #For all beacon m in scanner j, not i or previous <- double work
    #if n and m are the same -> overlap[i] = {j:[m]} and overlap[j] = {i:[n]}
    # same_beacons = [[same_beacon(b1,b2) for b2 in dist_beacons[4]] for b1 in dist_beacons[1]]
    # for i,beacon in enumerate(same_beacons):
    #     for j,same in enumerate(beacon):
    #         if same:
    #             print(beacons[0][i],beacons[1][j])
    # if same_beacons[n][m] == True, beacon n in first scanner equals beacon m in second scanner
    # same_beacons = [same_beacon(dist_beacons[0][0],b2) for b2 in dist_beacons[1]]
    # print(same_beacons)

    
    # for s1,scanner in enumerate(dist_beacons): #for each scanner
    #     for s2 in range(s1,len(dist_beacons)): #for each other scanner
    #         for i,b1 in enumerate(scanner):
    #             for j,b2 in enumerate(dist_beacons[s2]):
    #                 if same_beacon(b1,b2):
    #                     if i in overlap[s1].keys():
    #                         overlap[s1][i].append(j)
    #                     else:
    # #                         overlap[s1] = {i:j}


    # overlap = [{} for _ in dist_beacons]
    # for s1 in range(len(dist_beacons)):
    #     for s2 in range(s1+1,len(dist_beacons)):
    #         for b1 in range(len(dist_beacons[s1])):
    #             for b2 in range(len(dist_beacons[s2])):
    #                 if same_beacon(dist_beacons[s1][b1],dist_beacons[s2][b2]):
    #                     #print("True", s1,b1, " -> ",s2,b2)
    #                     if b1 in overlap[s1].keys():
    #                         overlap[s1][b1].append((s2,b2))
    #                     else:
    #                         overlap[s1][b1] = [(s2,b2)]
    #                     if b2 in overlap[s2].keys():
    #                         overlap[s2][b2].append((s1,b1))
    #                     else:
    #                         overlap[s2][b2] = [(s1,b1)]
                        

    #print(overlap[0][0][0][0])

    # # Number of beacon that not in overlap
    # nr_beacons = 0
    # for s,scanner in enumerate(beacons):
    #     for b,_ in enumerate(scanner):
    #         if b not in overlap[s].keys():
    #             nr_beacons += 1
    #         else:
    #             # Counted before?
    #             if s < overlap[s][b][0][0]:
    #                 print(s,overlap[s][b][0][0])
    #                 nr_beacons += 1
    # print(nr_beacons)

    # count beacons in overlap, delete future ones.


    #print(overlap)

    # nr_beacons = 0
    # for i in range(len(overlap)):
    #     for j in range(i+1,len(overlap)):
    #         if j in overlap[i].keys():
    #             for ol_scanner, ol_beacon in overlap[i][j]:
    #                 del overlap[ol_scanner][ol_beacon]
    #         nr_beacons += 1
    # print(nr_beacons)

if __name__ == "__main__":
    main()
