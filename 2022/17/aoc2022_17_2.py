"""Advent of Code: 2022.17.2"""
import sys

# Vi får en repetisjon, men hvordan finne start og stop?
# Jet stream vil repetere seg og steinene repeterer seg svært ofte.
# Når det blir et sammenfall mellom steinene og jet stream på et område
# der ingen brikker kan falle videre
# When I get the same stone at the same index in the jet stream and the stone fall to 
# rest above all previous stones (height A) and all the next stones fall to rest above A.
# For each stone that spans I want to know: jet_stream_index, height it fell to rest and type.

class Chamber:
    """ For the chamber with falling rocks """
    chamber = [ ['.' for _ in range(7)] for _ in range(4)]
    first_empty = [ 0 for _ in range(7) ] # Poenget med denne var å kunne avgjøre om jeg kan redusere 
    #highest_point = 0
    next_stone = 0 # From 0 to 4
    jet_stream_index = 0
    removed_rows = 0
    falling_stone = []
    stones_fallen = 0
    
    stone_info = [[i%5,0,0] for i in range(100000)]
    stone_nr = 0

    def __init__(self,jet_streams) -> None:
        self.jet_streams = jet_streams

    def __str__(self) -> str:
        output = ""
        for row in self.chamber[::-1]:
            output += '|' + "".join(row) + '|\n'
            #output += "".join(row) + '\n'
        output += "|-------|\n"
        return output

    # def clean_up_chamber(self):
    #     """ Remove stones that cannot interfere with hight. """
    #     pass

    def new_stone_fall(self):
        """ A new stone is spaned and dropped. """
        # Extend chamber to fit new stone
        highest_point = max(self.first_empty)
        empty_space = len(self.chamber) - highest_point
        #empty_space = len(self.chamber) - self.highest_point
        rows_needed = 4
        if self.next_stone in [1, 2]:
            rows_needed = 6
        elif self.next_stone == 3:
            rows_needed = 7
        elif self.next_stone == 4:
            rows_needed = 5

        while empty_space < rows_needed:
            self.chamber.append(['.','.','.','.','.','.','.'])
            empty_space += 1

        while empty_space > rows_needed:
            del self.chamber[-1]
            empty_space -= 1

        # Span next stone
        top = len(self.chamber) - 1
        stones = [ [[top,2],[top,3],[top,4],[top,5]],                \
                   [[top,3],[top-1,2],[top-1,3],[top-1,4],[top-2,3]],\
                   [[top,4],[top-1,4],[top-2,2],[top-2,3],[top-2,4]],\
                   [[top,2],[top-1,2],[top-2,2],[top-3,2]],          \
                   [[top,2],[top,3],[top-1,2],[top-1,3]] ]

        self.falling_stone = stones[self.next_stone]

        move_stone = True
        while move_stone:
            self.move_stone_jet()
            move_stone = self.move_stone_down()
        self.place_stone()

        self.next_stone += 1
        if self.next_stone > 4:
            self.next_stone = 0

        # Reduce chamber
        self.stones_fallen += 1
        if self.stones_fallen == 2000:
            rows_to_remove = min(self.first_empty)
            self.chamber = self.chamber[rows_to_remove:]
            self.removed_rows += rows_to_remove

            for i,_ in enumerate(self.first_empty):
                self.first_empty[i] -= rows_to_remove

            self.stones_fallen = 0

        # Stone Info index increase
        self.stone_info[self.stone_nr][1] += self.jet_stream_index
        self.stone_nr += 1

    def move_stone_jet(self):
        """ Moves the stone one time according to jet stream."""

        # Determine direction of jet stream
        move_left = True
        if self.jet_streams[self.jet_stream_index] == '>':
            move_left = False

        # Can it move, if any part of the stone hits something, then false.
        stone_moves = True
        for part in self.falling_stone:
            if move_left:
                # Does it hit the wall
                if part[1] == 0:
                    stone_moves = False
                    break

                # Does it hit another rock?
                if self.chamber[part[0]][part[1]-1] != '.':
                    stone_moves = False
                    break
            else:
                # Does it hit the wall
                if part[1] == 6:
                    stone_moves = False
                    break

                # Does it hit another rock?
                if self.chamber[part[0]][part[1]+1] != '.':
                    stone_moves = False
                    break

        # Move it
        if stone_moves:
            for part in self.falling_stone:
                if move_left:
                    part[1] -= 1
                else:
                    part[1] += 1

        # Increase the jet stream index and reset it if needed.
        self.jet_stream_index += 1
        if self.jet_stream_index == len(self.jet_streams):
            self.jet_stream_index = 0


    def move_stone_down(self) -> bool:
        """ Tries to move the stone down and return True if it managed it. """
        # Down
        # Can it move, if any part of the stone hits something, then false.
        stone_moves = True
        for part in self.falling_stone:
            # Does it hit the floor
            if part[0] == 0:
                stone_moves = False
                break

            # Does it hit a rock
            if self.chamber[part[0]-1][part[1]] != '.':
                stone_moves = False
                break

        # Move the stone
        if stone_moves:
            for part in self.falling_stone:
                part[0] -= 1

        return stone_moves

    def place_stone(self):
        """ Makes the stone part of the tower"""

        for part in self.falling_stone:
            # Update highest point if needed
            if part[0] >= self.first_empty[part[1]]:
                self.first_empty[part[1]] = part[0] + 1

            # Place part
            self.chamber[part[0]][part[1]] = '#'
        
        self.stone_info[self.stone_nr][2] = self.falling_stone[0][0] + self.removed_rows


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
    chamber = Chamber(lines[0].strip())
    for _ in range(100000):
        chamber.new_stone_fall()

    first_flat = 0
    for s in chamber.stone_info[30000:]:
        if s[0] == 0:
            first_flat = s[1]

    stone_info = []
    for i,s in enumerate(chamber.stone_info):
        if s[0] == 0 and s[1] == first_flat:
            stone_info.append([i,s[2]])
            #print("At",i,s[2])
    
    # for i,row in enumerate(chamber.chamber):
    #     print("".join(row),i)

    #print(max(chamber.first_empty)+chamber.removed_rows)
    pattern_start_height = stone_info[0][1]
    pattern_start_stones = stone_info[0][0]
    pattern_height  = stone_info[1][1] - stone_info[0][1]
    pattern_stones = stone_info[1][0] - stone_info[0][0]
    pattern_repeats = int((1000000000000 - pattern_start_stones) / pattern_stones)
    stones_left = 1000000000000 - pattern_start_stones - pattern_repeats * pattern_stones

    #print(pattern_start_height + pattern_repeats*pattern_height)
    #print(stones_left)

    height_left = chamber.stone_info[stone_info[0][0] + stones_left][2] - pattern_start_height
    #print(height_left)

    print("Tower height: ",pattern_start_height + pattern_repeats*pattern_height + height_left)
if __name__ == "__main__":
    main()
#1 000 000 000 000


# With test.txt; after 30 stones at height 49 the pattern repeats. Every 35 stone adds 53 height

# for input.txt; after 1385 stones at height 2117 the pattern repeats. Every 1730 stones adds 2 644 height.