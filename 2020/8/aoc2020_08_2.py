"""Advent of Code: 2020.8.2"""
import sys

def faulty_inst(inst):
    """f """
    instruction,executed = inst
    if not executed:
        return False
    operator,_ = instruction
    if operator in ["jmp","nop"]:
        return True

def acc_before_second_execution(program):
    """ Find the value of the acc befor any instructions are executed twice."""
    cur_inst = 0
    acc = 0
    instructions = [ (inst,False) for inst in program]
    exit_on = len(program)
    while True:
        if cur_inst == exit_on:
            return acc,True

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
    return acc,False

def possible_fault_instructions(program):
    """ Find the value of the acc befor any instructions are executed twice."""
    executed_instructions = []
    cur_inst = 0
    acc = 0
    instructions = [ (inst,False) for inst in program]
    exit_on = len(program)
    while True:
        if cur_inst == exit_on:
            break

        instruction,executed = instructions[cur_inst]
        if executed:
            break

        instructions[cur_inst] = (instruction,True)
        operator,argument = instruction

        if operator == "jmp":
            executed_instructions.append(cur_inst)
            cur_inst += argument
            continue

        if operator == "acc":
            acc += argument

        if operator == "nop":
            executed_instructions.append(cur_inst)

        cur_inst += 1
    return executed_instructions

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

    # Fix instructions
    faulty_instructions = possible_fault_instructions(instructions)
    for f_inst in faulty_instructions:
        new_program = instructions.copy()
        if new_program[f_inst][0] == "jmp":
            new_program[f_inst] = ("nop",new_program[f_inst][1])
        else:
            new_program[f_inst] = ("jmp",new_program[f_inst][1])
        acc,exited = acc_before_second_execution(new_program)
        if not exited:
            continue
        print(acc)
        break

if __name__ == "__main__":
    main()
