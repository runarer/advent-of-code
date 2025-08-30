"""Advent of Code: 2024.13.1"""
import sys,re



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
    i = 0
    claw_machines = []
    while i < len(lines):
        line = lines[i].strip() + " " + lines[i+1].strip() + " " + lines[i+2].strip()
        claw_machine = re.findall(r"Button A: X\+(\d+), Y\+(\d+) Button B: X\+(\d+), Y\+(\d+) Prize: X=(\d+), Y=(\d+)",line)
        claw_machines.append(list(map(int,claw_machine[0])))
        i += 4
    

    tokens = 0
    for claw_machine in claw_machines:
        A1,A2,B1,B2,X,Y = claw_machine
        # print(f"{A1}A + {B1}B = {X}")
        # print(f"{A2}A + {B2}B = {Y}\n")

        # Solve for B
        if (Y*A1 - A2*X) % (A1*B2 - A2*B1) == 0:
            B = (Y*A1 - A2*X) // (A1*B2 - A2*B1)

            # Solve for A
            if (X-B1*B) % A1 == 0:
                A  = (X-B1*B) // A1
                tokens += A*3 + B
        #     else:
        #         print("Unsolvable")
        # else:
        #     print("Unsolvable")
    print(tokens)


if __name__ == "__main__":
    main()