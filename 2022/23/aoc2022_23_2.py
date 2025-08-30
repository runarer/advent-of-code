"""Advent of Code: 2019.1.1"""
import sys

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

    collitions = set()
    proposals = {}

    directions = [0,1,2,3]

    need_to_move = True
    rounds = 0
    while need_to_move:
        rounds += 1
        need_to_move = False        
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

    print(rounds)

if __name__ == "__main__":
    main()
