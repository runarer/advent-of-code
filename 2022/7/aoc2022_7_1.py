"""Advent of Code: 2022.7.1"""
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

    # This can be solved with a hashmap where file/dir name is the key and a files value is its size.
    # The value for a dir is another hashmap.

    # what about absolut dir path and their size?

    current_directory = "/"
    directory_tree = {"/":0}
    for line in lines[1:]:
        if line == "$ ls" or line[0:4] == "dir ":
            # Populate hashmap? No just ignore.
            # print("ls or dir",current_directory)
            continue
        elif line == "$ cd ..":
            # Change to parent directory. But how? Use some search for last '/' from current_directory[1:]?
            new_directory = "/".join( current_directory.split('/')[:-1] )
            if new_directory == "":
                new_directory = "/"

            # add size of current_directory to new_directory
            directory_tree[new_directory] += directory_tree[current_directory]
            current_directory = new_directory

            # print("$ cd ..",current_directory)
        elif line[0:5] == "$ cd ":
            # Change to and create a new directory
            if current_directory != "/":
                current_directory += "/"
            current_directory += line[5:]
            directory_tree[current_directory] = 0

            # print("$ cd ", current_directory)
        else:
            # File, only intrested in size
            # print("file")
            size = int(line.split()[0])
            directory_tree[current_directory] += size

    # print(directory_tree)

    sum_small_dirs = sum(filter(lambda x: x < 100000,directory_tree.values()))
    print(sum_small_dirs)

if __name__ == "__main__":
    main()
