"""Advent of Code: 2019.1.1"""
import sys

# def print_elves(elves):
#     for i in range(12):
#         line = ""
#         for j in range(14):
#             if (j,i) in elves:
#                 line += '#'
#             else:
#                 line += '.'
#         print(line)

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
    lines = [line.strip() for line in lines]
    elves = set()

    for i,line in enumerate(lines):
        for j, char in enumerate(line):
            if char == '#':
                elves.add((j,i))
    # print_elves(elves)
    collitions = set()
    proposals = {}

    directions = [0,1,2,3]

    need_to_move = True
    for _ in range(10):
    #while need_to_move:
        need_to_move = False
        #print(directions)
        # Create all proposals for this round.
        for elf in elves:
            x,y = elf
            # Does it need to move
            surrounding_tiles = {(x,y-1),(x,y+1),(x+1,y),(x-1,y),(x+1,y+1),(x-1,y+1),(x+1,y-1),(x-1,y-1)}
            if surrounding_tiles.isdisjoint(elves):
                continue
            
            need_to_move = True

            # Can it move?
            tiles = [{(x+1,y-1),(x,y-1),(x-1,y-1)},{(x+1,y+1),(x,y+1),(x-1,y+1)},{(x-1,y+1),(x-1,y),(x-1,y-1)},{(x+1,y+1),(x+1,y),(x+1,y-1)}]
            moves = [(x,y-1),(x,y+1),(x-1,y),(x+1,y)]
            
            for direction in directions:
                if tiles[direction].isdisjoint(elves):
                    if moves[direction] in collitions:
                        break
                    if moves[direction] in proposals:
                        collitions.add(moves[direction])
                        del proposals[moves[direction]]
                        break
                    proposals[moves[direction]] = elf
                    break

        # Make the moves.
        for move_to,elf in proposals.items():
            elves.remove(elf)
            elves.add(move_to)
        proposals.clear()
        collitions.clear()

        temp = directions.pop(0)
        directions.append(temp)
        # print("////////////////////////////")
        # print_elves(elves)

        # Find smallest and largest x and y
    max_x = 0
    min_x = 1000000
    max_y = 0
    min_y = 1000000
    for elf in elves:
        x,y = elf
        max_x = max(max_x,x)
        min_x = min(min_x,x)
        max_y = max(max_y,y)
        min_y = min(min_y,y)        
    # This gives size of square
    square_size = (max_x - min_x + 1) * (max_y - min_y + 1)
    # print(max_x,min_x,max_y,min_y)
    # Subtract number of elves.
    ground_tiles = square_size - len(elves)
    print("Ground tiles:",ground_tiles)

if __name__ == "__main__":
    main()
