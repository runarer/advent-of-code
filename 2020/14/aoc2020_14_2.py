"""Advent of Code: 2020.14.2"""
import sys
import re

def addresses(addr,mask):
    """Lager alle mulige addresser basert på addr og mask"""
    if len(mask) == 1:
        if mask[0] == '0':
            return [ addr[0] ]
        if mask[0] == '1':
            return [ '1' ]
        return ['1','0']

    if mask[0] == '0':
        addrs = addresses(addr[1:],mask[1:])
        for i,new_addr in enumerate(addrs):
            addrs[i] = addr[0] + new_addr
        return addrs

    if mask[0] == '1':
        addrs = addresses(addr[1:],mask[1:])
        for i,new_addr in enumerate(addrs):
            addrs[i] = '1' + new_addr
        return addrs

    addrs = addresses(addr[1:],mask[1:])
    new_addresses = []
    for i,new_addr in enumerate(addrs):
        new_addresses.append('1' + new_addr)
        new_addresses.append('0' + new_addr)

    return new_addresses

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
    cur_mask = ""

    for line in lines:
        if line[:4] == "mask":
            cur_mask = line[7:-1]
        else:
            results = re.match(r"^mem\[(\d+)\] = (\d+)$",line)
            addr = format( int(results.group(1)),"036b" )
            value = int(results.group(2))

            mem_addresses = addresses(addr,cur_mask)

            for address in mem_addresses:
                mem[address] = value

    total_value = sum( mem.values() )
    print(total_value)

if __name__ == "__main__":
    main()
