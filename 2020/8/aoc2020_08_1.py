"""Advent of Code: 2020.1.1"""
import sys

def acc_before_second_execution(program):
    """ Find the value of the acc befor any instructions are executed twice."""
    cur_inst = 0
    acc = 0
    instructions = [ (inst,False) for inst in program]
    while True:
        instruction,executed = instructions[cur_inst]
        if executed:
            break

        instructions[cur_inst] = (instruction,True)
        operator,argument = instruction

        if operator == "jmp":
            cur_inst += argument
            continue

        if operator == "acc":
            acc += argument

        cur_inst += 1
    return acc

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

    # Create list of instructions.
    instructions = []
    for line in lines:
        operator,argument = line.strip().split()
        instructions.append( (operator,int(argument)))

    # Execute instructions
    acc = acc_before_second_execution(instructions)
    print(acc)


if __name__ == "__main__":
    main()
