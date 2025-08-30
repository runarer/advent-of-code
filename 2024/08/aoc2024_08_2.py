"""Advent of Code: 2024.7.1"""
import sys
from itertools import combinations
from itertools import chain

# Change this to return a list of antinodes
def get_antinodes(antenna1,antenna2,height,width):
    antinodes = set()
    antinodes.add(antenna1)
    # add antenna1 to a set

    ax,ay = antenna1
    bx,by = antenna2

    dist_x = (bx - ax)
    dist_y = (by - ay)

    # Subtract distance from a until outside the map
    next_x = ax - dist_x
    next_y = ay - dist_y
    while 0 <= next_x < height and 0 <= next_y < width:
        antinodes.add((next_x,next_y))
        next_x -= dist_x
        next_y -= dist_y 

    # Add the distance to a until outside the map
    next_x = ax + dist_x
    next_y = ay + dist_y
    while 0 <= next_x < height and 0 <= next_y < width:
        antinodes.add((next_x,next_y))
        next_x += dist_x
        next_y += dist_y

    return antinodes

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
    height = len(lines)
    width = len(lines[0])-1 # DAMN YOU NEW LINE!

    freqencies = {}
    for row,line in enumerate(lines):
        for col,character in enumerate(line.strip()):
            if character != '.':
                if character in freqencies:
                    freqencies[character].append((row,col))
                else:
                    freqencies[character] = [(row,col)]

    # For each frequency, find all pairs    
    antinodes = set()
    for frequency,antennas in freqencies.items():
        for antenna1, antenna2 in combinations(antennas,2):
            antinodes |= set( get_antinodes(antenna1,antenna2,height,width) )
            
    # print(antinodes)
    # for row in range(height):
    #     for col in range(width):                           
    #         if (row,col) in antinodes:
    #             print("#",end='')
    #         else:
    #             print('.',end='')
    #     print()

    print(len(antinodes))        

    # For each pair, calculate (use rotation?) antinodes.
                

    # For each frequence, first one makes pairs with all the others, then the second makes pair with all left and so on.
    # The placement of the antinodes are based on the placement of the pair of antennas in relations to each other.



if __name__ == "__main__":
    main()
