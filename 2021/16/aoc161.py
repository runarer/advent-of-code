import sys
from typing import Protocol, Tuple, List

class Node(Protocol):
    def evaluate(self) -> int: pass

class Leaf:
    def __init__(self, value: int):
        self.value = int(value,2)

    def evaluate(self) -> int:
        return self.value

#operator kan være en funksjon
class Root:
    def __init__(self, operator: chr, nodes: List[Node]):
        self.nodes = nodes
        self.operator = operator

    def evaluate(self) -> int:
        return sum([node.evaluate() for node in self.nodes])

sum_version_nr = 0

def parse(bit_string: str) -> Tuple[Node,int]:
    version = int(bit_string[:3],2)
    type_id = int(bit_string[3:6],2)

    global sum_version_nr
    sum_version_nr += version

    # Value
    if type_id == 4:
        value = ""
        for i in range(6,len(bit_string),5):
            value += bit_string[i+1:i+5]
            if bit_string[i] == '0':
                return Leaf(value),i+5
            
    # Operators
    ## Number of bits.
    if bit_string[6] == '0':
        #Number of bits that is the subpackages.
        number_of_bits = int(bit_string[7:22],2)
        start_of_substring = 22
        end_of_substring = start_of_substring + number_of_bits
        sub_packages = bit_string[start_of_substring:end_of_substring]

        packages: List[Node] = []
        bits_parsed = 0
        while bits_parsed < number_of_bits :
            next_package, last_end = parse(sub_packages[bits_parsed:])
            bits_parsed += last_end
            packages.append(next_package)

        return Root(str(int(type_id)),packages),number_of_bits+22

    ## Number of packages
    if bit_string[6] == '1':
        number_of_packages = int(bit_string[7:18],2)
        start_of_substring = 18
        sub_packages = bit_string[start_of_substring:]

        packages: List[Node] = []
        packages_parsed = 0
        bits_parsed = 0
        while packages_parsed < number_of_packages:
            next_package, last_end = parse(sub_packages[bits_parsed:])
            bits_parsed += last_end
            packages.append(next_package)
            packages_parsed += 1

        return Root(str(int(type_id)),packages), bits_parsed+18

    return Leaf("0110"),-1

def to_bit_string(string : str):
    hex_dict = {'0': "0000",'1': '0001','2': '0010','3': '0011',
                '4': '0100','5': '0101','6': '0110','7': '0111',
                '8': '1000','9': '1001','A': '1010','B': '1011',
                'C': '1100','D': '1101','E': '1110','F': '1111'}

    bit_string = ""
    for character in string:
        bit_string += hex_dict[character]

    return bit_string

def main():
    """Start"""
    #get argument
    if len(sys.argv) < 1:
        sys.exit("Usage: python " + sys.argv[0] + " filename")
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as file:
            line = file.readline().strip()
    except IOError as err:
        print("{}\nError opening {}. Terminating program.".format(err, filename), file=sys.stderr)
        sys.exit(1)

    bit_string = to_bit_string(line)    
    _,_ = parse(bit_string)
    print(sum_version_nr)

if __name__ == "__main__":
    main()
