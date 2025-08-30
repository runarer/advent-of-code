"""Advent of Code: 2020.12.2"""
import sys

class Ship:
    """ Ship class"""
    facings = ["east","south","west","north"]

    def __init__(self, facing, east, south):
        """How to"""
        self.facing = self.facings.index(facing)
        self.east = east
        self.south = south
        self.wp_east = 10
        self.wp_south = -1

    def move_forward(self, steps):
        """ Moves the boat to the waypoint steps times."""
        self.east += steps*self.wp_east
        self.south += steps*self.wp_south

    def move_east(self,steps):
        """move waypoint east"""
        self.wp_east += steps

    def move_south(self,steps):
        """move waypoint south"""
        self.wp_south += steps

    def move_west(self,steps):
        """move waypoint west"""
        self.wp_east -= steps

    def move_north(self,steps):
        """move waypoint north"""
        self.wp_south -= steps

    def rotate(self,degree):
        """ Rotates the facing of the waypoint relative to the ship"""
        for _ in range(int(degree/90)):
            temp = self.wp_east
            self.wp_east = -1 * self.wp_south
            self.wp_south = temp

    def move(self,move,value):
        """Preformes a movement of the ship or waypoint"""
        if move == 'F':
            self.move_forward(value)
            return
        if move == 'R':
            self.rotate(value)
            return
        if move == 'L':
            self.rotate(360 - value)
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
    #print(ship.east,ship.south)


if __name__ == "__main__":
    main()
