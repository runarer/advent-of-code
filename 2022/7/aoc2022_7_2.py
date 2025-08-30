"""Advent of Code: 2022.7.2"""
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
    lines = [ line.strip() for line in lines]

    current_directory = "/"
    directory_tree = {"/":0}
    
    for line in lines[1:]:
        if line == "$ ls" or line[0:4] == "dir ":
            continue

        elif line == "$ cd ..":
            # Change to parent directory.
            new_directory = "/".join( current_directory.split('/')[:-1] )
            if new_directory == "":
                new_directory = "/"

            # add size of current_directory to new_directory
            directory_tree[new_directory] += directory_tree[current_directory]
            current_directory = new_directory

        elif line[0:5] == "$ cd ":
            # Change to and create a new directory
            if current_directory != "/":
                current_directory += "/"
            current_directory += line[5:]
            directory_tree[current_directory] = 0

        else:
            # File, only intrested in size
            size = int(line.split()[0])
            directory_tree[current_directory] += size

    # need to move out of current_directory and up to root.
    # This should be a function since it is the same code as above.
    for _ in current_directory.split('/')[1:]:
        new_directory = "/".join( current_directory.split('/')[:-1] )
        if new_directory == "":
            new_directory = "/"

        # add size of current_directory to new_directory
        directory_tree[new_directory] += directory_tree[current_directory]
        current_directory = new_directory

    total_used_space = directory_tree["/"]
    free_space = 70000000 - total_used_space
    needed_space = 30000000 - free_space

    smallest_dir = list(filter(lambda x: x >= needed_space, directory_tree.values()))
    print(min(smallest_dir))

if __name__ == "__main__":
    main()
