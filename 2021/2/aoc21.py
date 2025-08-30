"""AoC day 2, read a file and find depth and horizontal position of submarine. 
   Answer is a product of these."""
import sys

def get_movements(filename):
    """Return a list of measurements from given file."""
    with open(filename, 'r') as file:
        return file.read().strip().split('\n')

def calc_product(movements):
    """Calculate posistions and return a product of them."""
    horizontal = 0
    depth = 0
    for mov in movements:
        movement = mov.strip().split(' ')
        if movement[0] == "forward":
            horizontal += int(movement[1])
        elif movement[0] == "down":
            depth += int(movement[1])
        else:
            depth -= int(movement[1])
    return horizontal * depth


def main():
    """Start"""
    #get argument
    if len(sys.argv) < 1:
        sys.exit("Usage: python " + sys.argv[0] + " filename")
    filename = sys.argv[1]
    try:
        movements = get_movements(filename)
    except IOError as err:
        print("{}\nError opening {}. Terminating program.".format(err, filename), file=sys.stderr)
        sys.exit(1)
    #Find answer
    product = calc_product(movements)
    print("Product of position: " + str(product))

if __name__ == "__main__":
    main()