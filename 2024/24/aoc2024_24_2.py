"""Advent of Code: 2024.24.2"""
import sys, re

class Gate:
    def __init__(self,type:str,input1:str,input2:str,output:str) -> None:
        self.input1Org = input1
        self.input2Org = input2
        self.outputOrg = output
        if type == "AND":
            self.func = lambda a,b: a and b
        elif type == "XOR":
            self.func = lambda a,b: a != b
        else:
            self.func = lambda a,b: a or b

    def setInput1(self,input:Gate) -> None:
        self.input1 = input

    def setInput2(self,input:Gate) -> None:
        self.input2 = input

    def resetInput(self) -> None:
        pass

    def get_value(self) -> bool:
        return self.func(self.input1.get_value(),self.input2.get_value())
    
class InGate(Gate):    
    def __init__(self,type:str,input1:str,input2:str,output:str,listx:list[bool],listy:list[bool]) -> None:
        self.list1 = listx
        self.list2 = listy
        if input1[0] == 'y':
            self.list1 = listy
            self.list2 = listx
            
        self.list1Index = int(input1[1:])
        self.list2Index = int(input2[1:])

        super().__init__(type,input1,input2,output)

    def get_value(self) -> bool:
        return self.func(self.list1[self.list1Index],self.list2[self.list2Index])

def split_init_and_gates(lines:list[str]) -> tuple[list[bool],list[bool], list[tuple[str,str,str,str]]]:
    initialsX = []
    initialsY = []
    gates = []

    at_gates = False
    for line in lines:
        line = line.strip()
        if at_gates:
            result = re.match(r"(...) (AND|OR|XOR) (...) -> (...)",line)
            if result:
                gates.append( (result.group(2),result.group(1),result.group(3),result.group(4)) )
        else:
            if line == "":
                at_gates = True
                continue
            _,value = line.split(": ")
            if line[0] == 'x':
                initialsX.append( True if value == '1' else False)
            elif line[0] == 'y':
                initialsY.append( True if value == '1' else False)

    # initialsX.reverse()
    # initialsY.reverse()

    return initialsX,initialsY,gates

def create_gates(in1list,in2list,out,gates_tup) -> dict[str,Gate]:
    gates:dict[str,Gate] = {}            

    # create gates
    for type,in1,in2,out in gates_tup:
        if in1[0] in ["x","y"]:
            gates[out] = InGate(type,in1,in2,out,in1list,in2list)
        else:
            gates[out] = Gate(type,in1,in2,out)
    
    # connect gates
    for gate in gates:
        if isinstance(gates[gate],InGate):
            continue
        gates[gate].setInput1(gates[gates[gate].input1Org])
        gates[gate].setInput2(gates[gates[gate].input2Org])
    
    return gates

def set_numbers(x,y,listx,listy):
    leading = '045b'
    xbit = format(x,leading)
    ybit = format(y,leading)


    for i,bit in enumerate(reversed(xbit)):
        listx[i] = bit == '1'
    for i,bit in enumerate(reversed(ybit)):
        listy[i] = bit == '1'



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
    listx,listy,gates_tup = split_init_and_gates(lines)

    # listx = [False] * initials
    # listy = [False] * initials
    listz = [False] * (len(listx) + 1)

    x = "".join('1' if v else '0' for v in reversed(listx))
    y = "".join('1' if v else '0' for v in reversed(listy))
    xint = int(x,2)
    yint = int(y,2)

    xint = 512
    yint = 1

    expected = xint + yint

    set_numbers(xint,yint,listx,listy)

    print(format(expected,'046b'))

    gates = create_gates(listx,listy,listz,gates_tup)

    output:list[Gate|None] = [None] * len(listz)
    # print(len(output))
    for s,gate in gates.items():
        if s.startswith('z'):
            output[ int(s[1:]) ] = gate

    s = ['1' if v.get_value() else '0' for v in output if v != None]
    # s.reverse()
    print("".join(reversed(s)))
    print(int("".join(reversed(s)),2))


    # print(gates)




if __name__ == "__main__":
    main()
