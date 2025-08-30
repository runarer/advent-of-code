"""Advent of Code: 2020.17.1"""
import sys

class SatCore:
    """ddd"""

    def __init__(self,initial_state):
        self.core = {}
        self.x_start = 0
        self.x_end = len(initial_state)-1
        self.y_start = 0
        self.y_end = self.x_end
        self.z_start = 0
        self.z_end = 1
        self.w_start = 0
        self.w_end = 1

        for y,row in enumerate(initial_state):
            for x,col in enumerate(row.strip()):
                if col == '#':
                    self.core[(x,y,0,0)] = True

    def cycle(self):
        """ Runs a cycle for the core."""
        new_core = {}

        for w in range(self.w_start-1,self.w_end+2):
            for z in range(self.z_start-1,self.z_end+2):
                for y in range(self.y_start-1,self.y_end+2):
                    for x in range(self.x_start-1,self.x_end+2):
                        active_neighbors = self.active_neighbors(x,y,z,w)

                        if active_neighbors == 3:
                            new_core[(x,y,z,w)] = True
                            continue
                        if active_neighbors == 2 and self.is_active(x,y,z,w):
                            new_core[(x,y,z,w)] = True
                            continue

        # Update dims and core
        self.x_start -= 1
        self.x_end += 1
        self.y_start -= 1
        self.y_end += 1
        self.z_start -= 1
        self.z_end += 1
        self.w_start -= 1
        self.w_end += 1
        self.core = new_core

    def active_neighbors(self,x,y,z,w):
        """Return the number of active neighbors"""
        ac_neighbors = 0

        for ws in [-1,0,1]:
            for zs in [-1,0,1]:
                for ys in [-1,0,1]:
                    for xs in [-1,0,1]:
                        if self.is_active(x+xs,y+ys,z+zs,w+ws):
                            ac_neighbors += 1

        if self.is_active(x,y,z,w):
            ac_neighbors -= 1

        return ac_neighbors

    def active_cubes(self):
        """Return the number of active cubes in the core """
        active_cubes = len(self.core)

        # for y in range(self.cols):
        #     for x in range(self.rows):
        #         if (x,y,0,0) in self.core:
        #             active_cubes -= 1

        # active_cubes = 0
        
        # for cube in self.core:
        #     x,y,z,w = cube
        #     if z == 0 and w == 0:
        #         active_cubes += 1
        #         continue
        #     if z == w:
        #         active_cubes += 4
        #         continue
        #     active_cubes += 2

        return active_cubes

    def is_active(self,x, y, z, w):
        """ Return the status of one cell"""
        # z = abs(z)
        # w = abs(w)
        if (x,y,z,w) not in self.core:
            return False
        return self.core[(x,y,z,w)]

    def __str__(self):
        string = f"Rows: {abs(self.x_start)+self.x_end}\nCols: {abs(self.y_start)+self.y_end}\n"
        for w in range(self.w_start,self.w_end):
            for z in range(self.z_start,self.z_end):
                string += f"Z={z} W={w}\n"
                for y in range(self.y_start,self.y_end):
                    for x in range(self.x_start,self.x_end):
                        if (x,y,z,w) in self.core:
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
    #print(core)
    print(core.active_cubes())
    #print(len(core.core))

if __name__ == "__main__":
    main()
