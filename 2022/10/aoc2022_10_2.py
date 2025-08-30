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
    cycle = 0
    x_register = 1
    screen = [ ' ' for _ in range(240) ]

    def draw():
        sprite = [x_register-1,x_register,x_register+1]
        if cycle % 40 in sprite:
            screen[cycle] = '#'

    for line in lines:
        line = line.strip()

        if line == "noop":
            draw()
        else:
            _, value = line.split()
            draw()
            cycle += 1
            draw()
            x_register += int(value)

        cycle += 1

    print("".join(screen[0:40]   ))
    print("".join(screen[40:80]  ))
    print("".join(screen[80:120] ))
    print("".join(screen[120:160]))
    print("".join(screen[160:200]))
    print("".join(screen[200:240]))


if __name__ == "__main__":
    main()
