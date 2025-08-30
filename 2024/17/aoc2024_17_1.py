"""Advent of Code: 2024.10.1"""
import sys

class StrangeComputer:
    def __init__(self,init_A,init_B,init_C,init_program) -> None:
        self.regA = init_A
        self.regB = init_B
        self.regC = init_C
        self.program = init_program
        self.halt_at = len(self.program)
        self.pointer = 0
        self.output = ""

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
        if self.pointer >= self.halt_at:
            return False
        
        opcode = self.program[self.pointer]
        operand = self.program[self.pointer+1]

        if opcode == 0:
            self.adv(operand)
        elif opcode == 1:
            self.bxl(operand)
        elif opcode == 2:
            self.bst(operand)
        elif opcode == 3:
            self.jnz(operand)            
        elif opcode == 4:
            self.bxc(operand)
        elif opcode == 5:
            self.out(operand)
        elif opcode == 6:
            self.bdv(operand)
        elif opcode == 7:
            self.cdv(operand)
        else:
            print("Whut!")
            return False

        self.pointer += 2
        return True
    
    # 0
    def adv(self,operand):
        operand = self.combo(operand)
        self.regA = self.regA // (2**operand)

    # 1
    def bxl(self,operand):
        self.regB ^= operand

    # 2
    def bst(self,operand):
        operand = self.combo(operand)
        self.regB = operand % 8

    # 3
    def jnz(self,operand):
        if self.regA != 0:
            self.pointer = operand
            self.pointer -= 2

    # 4
    def bxc(self,operand):
        self.regB ^= self.regC

    # 5
    def out(self,operand):
        operand = self.combo(operand)
        self.output += "," + str(operand%8)

    # 6
    def bdv(self,operand):
        operand = self.combo(operand)
        self.regB = self.regA // (2**operand)

    # 7
    def cdv(self,operand):
        operand = self.combo(operand)
        self.regC = self.regA // (2**operand)

    def __str__(self):
        return self.output[1:]
    
    def run(self):
        while self.step():
            continue

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

    computer = StrangeComputer(register_A,register_B,register_C,program)
    # computer = StrangeComputer(2024,0,0,[0,1,5,4,3,0])
    computer.run()
    print(computer)
    # print(computer.regB)

if __name__ == "__main__":
    main()
