"""Advent of Code: 2024.17.2

    Instead of writing a simulator, I can use the code as an algorithm.
    This could be a meatprogramming task sutable for C++, with consteval and such.

    A New aproach. Start at the end and find out what initial value can create 0 as
    output. Then try to understand what the program does to the values and if it can
    be reversed.

"""
import sys

def StrangeComputer(init_A,init_B,init_C,init_program):
    regA = init_A
    regB = init_B
    regC = init_C
    program = init_program
    output_pointer = 0
    output = []

    while True:
        if init_A % 100000000 == 0:
            print(init_A)

        # 2,4 bst combo(4)
        regB = regA % 8
        
        # 1,1 bxl 1
        regB ^= 1
        
        
        # 7,5 cdv combo(5)
        regC = regA // (2**regB)
        
        
        # 4,0 bxc (0 is ignored)
        regB ^= regC
        

        # 0,3 adv combo(3)
        regA = regA // 8

        
        # 1,6 bxl 6
        regB ^= 6
        

        # 5,5 out combo(5) -> out regB
        # This prints the mod 8 of the content in regB
        # We need to print 2,4,1,1,7,5,4,0,0,3,1,6,5,5,3,0 in that order
        # regB need to be (something*8)+2 then, (something*8)+4
        output_value = regB % 8
        # print(output_value)
        if output_value == program[output_pointer]:
            output.append(output_value)
            output_pointer += 1
        else:
            init_A += 1
            regA = init_A
            regB = init_B
            regC = init_C
            output_pointer = 0
            output.clear()       
        
        # 3,0 jnz 0
        # This jumbs to the start if regA != 0
        # So when regA is 0 we are done.
        if regA == 0:
            if output == program:
                break
            else:
                init_A += 1
                regA = init_A
                regB = init_B
                regC = init_C
                output_pointer = 0
                output.clear()
    
    return init_A

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
    register_A = int(lines[0].strip().split()[2])
    register_B = int(lines[1].strip().split()[2])
    register_C = int(lines[2].strip().split()[2])

    program = list(map(int,lines[4].strip().split()[1].split(',')))

    print(register_A,register_B,register_C)
    print(program)
    # print(StrangeComputer(register_A,register_B,register_C,program))
    print(StrangeComputer(1700000000,register_B,register_C,program))

if __name__ == "__main__":
    main()
