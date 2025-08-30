"""AoC day 3,"""
import sys

def get_bits(filename):
    """Return a list of string made of 0 and 1s."""
    with open(filename, 'r') as file:
        return file.read().strip().split('\n')

#Find most common bit in position
def most_common_bit(position, bit_strings):
    """
    Finds the most common bit in position for a list of bit strings. 
    If tie then return 1.
    """
    ones = 0
    half = len(bit_strings)/2
    for bit_string in bit_strings:
        ones += int(bit_string[position])
    if ones > half:
        return 1
    if ones < half:
        return 0
    return 1

def calc_product(bit_strings):
    """Calculate """
    #Oxygen
    oxygen = list(bit_strings)
    i = 0
    while len(oxygen) > 1:
        bit_to_filter = most_common_bit(i,oxygen)
        oxygen = list(filter(lambda b : int(b[i]) == bit_to_filter,oxygen))
        i += 1

    #C02
    co2 = list(bit_strings)
    i = 0
    while len(co2) > 1:
        bit_to_filter = 0
        if most_common_bit(i,co2) == 0:
            bit_to_filter = 1
        co2 = list(filter(lambda b : int(b[i]) == bit_to_filter,co2))
        i += 1
    return int(oxygen[0],2) * int(co2[0],2)

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