"""Advent of Code: 2024.7.1"""
import sys
from itertools import combinations
from itertools import chain
 
def get_antinodes(antenna1,antenna2):
    ax,ay = antenna1
    bx,by = antenna2

    antinode_ax = ax + -1*(bx - ax)
    antinode_ay = ay + -1*(by - ay)
    antinode_bx = bx + -1*(ax - bx)
    antinode_by = by + -1*(ay - by)

    return ((antinode_ax,antinode_ay),(antinode_bx,antinode_by))

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
            antinode1,antinode2 = get_antinodes(antenna1,antenna2)
            # print(antenna1,antenna2,antinode1,antinode2)
            if 0 <= antinode1[0] < width and 0 <= antinode1[1] < height:
                antinodes.add(antinode1)
            if 0 <= antinode2[0] < width and 0 <= antinode2[1] < height:
                antinodes.add(antinode2)      
            
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
