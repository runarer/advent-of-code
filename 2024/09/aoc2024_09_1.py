"""Advent of Code: 2024.9.1"""
import sys

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
    line = lines[0].strip()
    disk_map = [int(c) for c in line]
    total_disk_size = sum(disk_map)
    filesystem = []

    file_id = 0
    file = True
    for c in disk_map:
        if file:
            filesystem += [file_id]*c
            file = False
            file_id += 1
        else:
            filesystem += [-1]*c
            file = True
    
    # Can rearrange stuff
    start = filesystem.index(-1)
    end = len(filesystem)-1
    while start< end:
        if filesystem[end] != -1:
            # Move to start
            filesystem[start],filesystem[end] = filesystem[end],filesystem[start]
            start = filesystem.index(-1,start)
        end -= 1
    

    # Calculate checksun
    position = 0
    checksum = 0
    while filesystem[position] >= 0:
        checksum += position * filesystem[position]
        position += 1
    print(checksum)
        






if __name__ == "__main__":
    main()
