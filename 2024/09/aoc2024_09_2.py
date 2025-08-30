"""Advent of Code: 2024.9.2
    Denne løsningen er ikke rask nok.
"""
import sys

def find_next_file(filesystem,end):
    file_end = end
    while filesystem[file_end] == -1:
        file_end -= 1
    file_id = filesystem[file_end]
    file_start = file_end
    while filesystem[file_start - 1] == file_id:
        file_start -= 1
    file_size = file_end - file_start + 1

    return (file_start,file_end,file_size,file_id)

def find_space(filesystem,begin,size):
    last_index = len(filesystem) - 1
    try:
        space_start = filesystem.index(-1,begin)
    except ValueError:
        return -1
    
    space_end = space_start
    while space_end + 1 <= last_index and filesystem[space_end + 1] == -1:
        space_end += 1
    space_size = space_end - space_start + 1
    # print("ss:",space_size,size)
    if space_size < size:        
        return find_space(filesystem,space_end+1,size)

    return space_start

def move(filesystem,to_start,from_start,size):
    for i in range(size):
        filesystem[to_start+i],filesystem[from_start+i] = filesystem[from_start+i],filesystem[to_start+i]


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
    old_filesystem = []
    
    file_id = 0
    file = True
    for c in disk_map:
        if file:
            old_filesystem += [file_id]*c
            file = False
            file_id += 1
        else:
            old_filesystem += [-1]*c
            file = True
    new_filesystem = old_filesystem.copy()

    # Can rearrange stuff
    absolute_start = new_filesystem.index(-1)
    file_start = len(old_filesystem)

    while absolute_start< file_start:
        file_start,file_end,file_size,file_id = find_next_file(old_filesystem,file_start-1)
        
        space_start = find_space(new_filesystem,absolute_start,file_size)        
        if space_start == -1:
            continue
        
        if space_start < file_start:
            move(new_filesystem,space_start,file_start,file_size)
        
        absolute_start = new_filesystem.index(-1,absolute_start)

    # Calculate checksun
    print(sum(i*v if v != -1 else 0 for i,v in enumerate(new_filesystem)))


if __name__ == "__main__":
    main()
