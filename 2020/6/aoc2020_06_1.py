""" Advent of Code: 2020.6.1

    Read lines as lists
    Transforme to set
    combine sets
    set to list, length of set is number

"""
import sys

def create_groups(lines):
    """ Create groups """
    groups = []
    group = ""
    for line in lines:
        if line.strip():
            group += line.strip()
        else:
            groups.append(group)
            group = ""
    groups.append(group)

    return groups

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

    groups = create_groups(lines)
    yes_answers = [ len(set(group)) for group in groups]
    total_yes_answers = sum(yes_answers)
    print(total_yes_answers)


if __name__ == "__main__":
    main()
