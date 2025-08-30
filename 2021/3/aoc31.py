"""AoC day 3,"""
import sys

def get_bits(filename):
    """Return a list of string made of 0 and 1s."""
    with open(filename, 'r') as file:
        return file.read().strip().split('\n')

def calc_product(bit_strings):
    """Calculate """
    gamma_rate = ""
    epsilon_rate = ""
    bits = [0,0,0,0,0,0,0,0,0,0,0,0]
    for bit_string in bit_strings:
        for i in range(12):
            bits[i] += int(bit_string[i])
    print(bits)
    for i,_ in enumerate(bits):
        if bits[i] > len(bit_strings)/2:
            gamma_rate += '1'
            epsilon_rate += '0'
        else:
            gamma_rate += '0'
            epsilon_rate += '1'
    
    #print(int(gamma_rate,2))
    #print(int(epsilon_rate,2))
    return int(gamma_rate,2) * int(epsilon_rate,2)


def main():
    """Start"""
    #get argument
    if len(sys.argv) < 1:
        sys.exit("Usage: python " + sys.argv[0] + " filename")
    filename = sys.argv[1]
    try:
        bit_strings = get_bits(filename)
    except IOError as err:
        print("{}\nError opening {}. Terminating program.".format(err, filename), file=sys.stderr)
        sys.exit(1)
    #Find answer
    product = calc_product(bit_strings)
    print("Product of position: " + str(product))

if __name__ == "__main__":
    main()