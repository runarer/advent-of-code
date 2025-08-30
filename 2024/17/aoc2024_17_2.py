"""Advent of Code: 2024.17.2

    I think this need to be brute forced.
    If first output do not match, end simulation and so on.

    We always print the value of reg B

"""
import sys

class StrangeComputer:
    def __init__(self,init_A,init_B,init_C,init_program) -> None:
        self.regA = init_A
        self.regB = init_B
        self.regC = init_C
        self.program = init_program
        self.halt_at = len(self.program)
        self.pointer = 0
        self.output_pointer = 0
        self.output = []

    def combo(self, instruction):
        if instruction < 4: 
            return instruction
        if instruction == 4:
            return self.regA
        if instruction == 5:
            return self.regB
        if instruction == 6:
            return self.regC
        
        print("Whut, combo not valid.")
        return -1

    def step(self):
        
        opcode = self.program[self.pointer]
        operand = self.program[self.pointer+1]

        if opcode == 0:
            operand = self.combo(operand)
            self.regA = self.regA // (2**operand)
        elif opcode == 1:
            self.regB ^= operand
        elif opcode == 2:
            operand = self.combo(operand)
            self.regB = operand % 8
        elif opcode == 3:
            if self.regA != 0:
                self.pointer = operand
                self.pointer -= 2            
        elif opcode == 4:
            self.regB ^= self.regC
        elif opcode == 5:
            operand = self.combo(operand) % 8
            if operand != self.program[self.output_pointer]:
                return False
            self.output.append(operand)
            self.output_pointer += 1
        elif opcode == 6:
            operand = self.combo(operand)
            self.regB = self.regA // (2**operand)
        elif opcode == 7:
            operand = self.combo(operand)
            self.regC = self.regA // (2**operand)
        else:
            print("Whut!")
            return False

        self.pointer += 2
        return True
    
    def get_output(self):
        return self.output
    
    def run(self):
        
        while True:
            res = self.step()
            if not res:
                return False
            
            if self.pointer >= self.halt_at:
                return True

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

    output = []
    register_A = 0

    while output != program:
        register_A += 1
        computer = StrangeComputer(register_A,register_B,register_C,program)
        res = computer.run() # Can make this return true for successfull halt and false for other shit.
        
        if res:
            output = computer.get_output()
        
        if register_A % 1000000 == 0:
            print(register_A)
        
        # print(output)
    print(register_A)

if __name__ == "__main__":
    main()

# can start at 550000000