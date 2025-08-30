"""Advent of Code: 2022.17.1"""
import sys

class Chamber:
    """ For the chamber with falling rocks """
    chamber = [ ['.' for _ in range(7)] for _ in range(4)]
    first_empty = [ 0 for _ in range(7) ] # Poenget med denne var å kunne avgjøre om jeg kan redusere 
    highest_point = 0
    next_stone = 0 # From 0 to 4
    jet_stream_index = 0
    removed_rows = 0
    falling_stone = []

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
    for _ in range(2022):
        chamber.new_stone_fall()
    print(max(chamber.first_empty))
    print(chamber)

if __name__ == "__main__":
    main()
