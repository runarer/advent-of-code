"""Advent of Code: 2020.14.1"""
import sys
import re

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

    mem = {}

    cur_mask_on  = 0
    cur_mask_off = 0

    for line in lines:
        if line[:4] == "mask":
            #print(line[7:-1])
            cur_mask_on  = int( "".join( [ '0' if bit == 'X' else bit for bit in line[7:-1]] ),2 )
            cur_mask_off = int( "".join( [ '1' if bit == 'X' else bit for bit in line[7:-1]] ),2 )
            #print(cur_mask_on)
            #print(cur_mask_off)
        else:
            results = re.match(r"^mem\[(\d+)\] = (\d+)$",line)
            addr = int(results.group(1))
            value = int(results.group(2))

            # Apply masks
            value = value | cur_mask_on
            value = value & cur_mask_off

            mem[addr] = value

    total_value = sum( mem.values() )

    print(total_value)

if __name__ == "__main__":
    main()
