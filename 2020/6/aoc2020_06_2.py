""" Advent of Code: 2020.6.2

    Read lines as lists
    Transforme to set
    combine sets
    set to list, length of set is number

"""
import sys

def create_groups(lines):
    """ Create groups """
    groups = []
    group = set()
    first = True
    for line in lines:
        if line.strip():
            if first:
                group = set( line.strip() )
                first = False
            else:
                group.intersection_update( set( line.strip() ) )
        else:
            if group:
                groups.append(group)
            group = set()
            first = True
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
    yes_answers = [ len(group) for group in groups]
    total_yes_answers = sum(yes_answers)
    print(total_yes_answers)

if __name__ == "__main__":
    main()
