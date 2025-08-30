import sys, re

def run_instuctions(instructions):
    reactor = set()

    for inst,(x1,x2),(y1,y2),(z1,z2) in instructions:
        new_block = {(x,y,z) for x in range(x1,x2+1) for y in range(y1,y2+1) for z in range(z1,z2+1) }
        if inst == "on":
            # Add to reactor
            reactor.update(new_block)
        else:
            # remove new_block from reactor
            reactor.difference_update(new_block)

    return reactor

def create_instructions(lines):
    instructions = []
    
    for line in lines:
        matches = re.match(r"(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)",line)

        # For 221
        if int(matches[2]) > 50 or int(matches[2]) < -50:
            continue
        
        instruction = (matches[1], \
                        (int(matches[2]),int(matches[3])), \
                         (int(matches[4]),int(matches[5])), \
                        (int(matches[6]),int(matches[7]))  \
                      )
        instructions.append(instruction)

    return instructions


def main():
    """Start"""
    #get argument
    if len(sys.argv) < 1:
        sys.exit("Usage: python " + sys.argv[0] + " filename")
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except IOError as err:
        print("{}\nError opening {}. Terminating program.".format(err, filename), file=sys.stderr)
        sys.exit(1)

    instructions = create_instructions(lines)
    reactor = run_instuctions(instructions)
    print(len(reactor))

if __name__ == "__main__":
    main()