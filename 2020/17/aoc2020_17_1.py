"""Advent of Code: 2020.17.1"""
import sys

class SatCore:
    """ddd"""

    def __init__(self,initial_state):
        self.core = {}
        self.rows = len(initial_state)
        self.cols = self.rows
        self.height = 1

        for y,row in enumerate(initial_state):
            for x,col in enumerate(row.strip()):
                if col == '#':
                    self.core[(x,y,0)] = True
                # else:
                #     self.core[(x,y,0)] = False

    def cycle(self):
        """ Runs a cycle for the core."""
        new_core = {}

        for z in range(self.height+1):
            for y in range(-1,self.cols+1):
                for x in range(-1,self.rows+1):
                    active_neighbors = self.active_neighbors(x,y,z)

                    if active_neighbors == 3:
                        new_core[(x+1,y+1,z)] = True
                        continue
                    if active_neighbors == 2 and self.is_active(x,y,z):
                        new_core[(x+1,y+1,z)] = True
                        continue

                    # new_core[(x+1,y+1,z)] = False

        # Update dims and core
        self.cols += 2
        self.rows += 2
        self.height += 1
        self.core = new_core

    def active_neighbors(self,x,y,z):
        """Return the number of active neighbors"""
        ac_neighbors = 0

        for zs in [-1,0,1]:
            for ys in [-1,0,1]:
                for xs in [-1,0,1]:
                    if self.is_active(x+xs,y+ys,z+zs):
                        ac_neighbors += 1

        if self.is_active(x,y,z):
            ac_neighbors -= 1

        return ac_neighbors

    def active_cubes(self):
        """Return the number of active cubes in the core """
        active_cubes = len(self.core)*2

        for y in range(self.cols):
            for x in range(self.rows):
                if (x,y,0) in self.core:
                    active_cubes -= 1

        return active_cubes

    def is_active(self,x, y, z):
        """ Return the status of one cell"""
        z = abs(z)
        if (x,y,z) not in self.core:
            return False
        return self.core[(x,y,z)]

    def __str__(self):
        string = f"Rows: {self.rows}\nCols: {self.cols}\n"
        for z in range(self.height):
            if z == 0:
                string += f"Z={z}\n"
            else:
                string += f"Z={z}/-{z}\n"
            for y in range(self.cols):
                for x in range(self.rows):
                    #if self.core[(x,y,z)]:
                    if (x,y,z) in self.core:
                        string += '#'
                    else:
                        string += '.'
                string += '\n'
            string += '\n'
        return string

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

    core = SatCore(lines)
    core.cycle()
    core.cycle()
    core.cycle()
    core.cycle()
    core.cycle()
    core.cycle()
    print(core.active_cubes())

if __name__ == "__main__":
    main()
