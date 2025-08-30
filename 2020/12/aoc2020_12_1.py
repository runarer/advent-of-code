"""Advent of Code: 2020.12.1"""
import sys

class Ship:
    """ Ship class"""
    facings = ["east","south","west","north"]

    def __init__(self, facing, east, south):
        """How to"""
        self.facing = self.facings.index(facing)
        self.east = east
        self.south = south

    def move_forward(self, steps):
        """ Moves the boat in facing direction. Dette kan forenkles."""
        if self.facing == 0:
            self.move_east(steps)
        elif self.facing == 1:
            self.move_south(steps)
        elif self.facing == 2:
            self.move_west(steps)
        elif self.facing == 3:
            self.move_north(steps)

    def move_east(self,steps):
        """moves"""
        self.east += steps

    def move_south(self,steps):
        """moves"""
        self.south += steps

    def move_west(self,steps):
        """moves"""
        self.east -= steps

    def move_north(self,steps):
        """moves"""
        self.south -= steps

    def rotate(self,direction,degree):
        """ Rotates the facing of the boat but oesd not move it"""
        if direction == "left":
            degree = 360 - degree
        self.facing = (self.facing + int(degree/90)) % 4

    def move(self,move,value):
        """Preformes a movement of the ship"""
        if move == 'F':
            self.move_forward(value)
            return
        if move == 'R':
            self.rotate("right",value)
            return
        if move == 'L':
            self.rotate("left",value)
            return
        if move == 'E':
            self.move_east(value)
            return
        if move == 'S':
            self.move_south(value)
            return
        if move == 'W':
            self.move_west(value)
            return
        if move == 'N':
            self.move_north(value)

def main():
    """Start"""
    #get argument
    if len(sys.argv) < 1:
        sys.exit("Usage: python " + sys.argv[0] + " filename")
    filename = sys.argv[1]
    try:
        with open(filename, 'rt', encoding="utf-8") as file:
            lines = file.readlines()
    except IOError as err:
        print(f"{err}\nError opening {filename}. Terminating program.", file=sys.stderr)
        sys.exit(1)

    movements = [(line[0],int(line[1:])) for line in lines]

    ship = Ship("east",0,0)
    for move,value in movements:
        #print(move, value)
        ship.move(move,value)
    manhattan_dist = abs(ship.east) + abs(ship.south)
    print(ship.east,ship.south,manhattan_dist)
    #print(ship.east,ship.south,ship.facing)


if __name__ == "__main__":
    main()
