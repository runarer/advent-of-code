"""Advent of Code: 2024.24.1"""
import sys, re

def split_init_and_gates(lines:list[str]) -> tuple[dict[str,bool], list[tuple[str,str,str,str]]]:
    initials = {}
    gates = []

    at_gates = False
    for line in lines:
        line = line.strip()
        if at_gates:
            result = re.match(r"(...) (AND|OR|XOR) (...) -> (...)",line)
            if result:
                in1 = result.group(1)
                in2 = result.group(3)
                out = result.group(4)

                if in1 not in initials:
                    initials[in1] = None
                if in2 not in initials:
                    initials[in2] = None
                if out not in initials:
                    initials[out] = None

                gates.append( (result.group(2),in1,in2,out) )
        else:
            if line == "":
                at_gates = True
                continue
            result = line.split(": ")

            initials[result[0]] = result[1] == '1'
    return initials,gates

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
    initials,gates = split_init_and_gates(lines)

    # print(initials)

    while gates:
        inst,in1,in2,out = gates.pop(0)

        if initials[in1] != None and initials[in2] != None:
            if inst == "AND":
                initials[out] = initials[in1] and initials[in2]
            elif inst == "XOR":
                initials[out] = initials[in1] != initials[in2]
            else: # OR
                initials[out] = initials[in1] or initials[in2]
        else:
            gates.append((inst,in1,in2,out))

    result = [ (i,v) for i,v in initials.items() if i.startswith('z')]
    result.sort(reverse=True)
    bit = "".join(['1' if v else '0' for _,v in result])
    part1 = int(bit,2)

    print(f"Part 1: {part1}")




if __name__ == "__main__":
    main()
