"""Advent of Code: 2020.25.1"""
import sys

def find_loops(key):
    """Find the loop for a key"""

    value = 1
    loops = 0
    while value != key:
        loops += 1
        value *= 7
        value = value % 20201227

    return loops





def find_encryption_key(sub_number,loops):
    """ Finds the encryption key"""
    encryption_key = 1

    for _ in range(loops):
        encryption_key *= sub_number
        encryption_key %= 20201227

    return encryption_key




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
    
    key_1 = int(lines[0].strip())
    key_2 = int(lines[1].strip())

    key_1_loops = find_loops(key_1)
    key_2_loops = find_loops(key_2)

    encryption_key_1 = find_encryption_key(key_2,key_1_loops)
    encryption_key_2 = find_encryption_key(key_1,key_2_loops)

    print(encryption_key_1)
    print(encryption_key_2)

if __name__ == "__main__":
    main()
