"""Advent of Code: 2024.18.2"""
import sys

# this is similar to the hot springs problem from another year.
# easy to guess part 2, so solve both parts at once.

def make_pattern_dict(patterns):
    pattern_dict = {}
    for pattern in patterns:
        len_letter = len(pattern)
        if len_letter not in pattern_dict:
            pattern_dict[len_letter] = []
        pattern_dict[len_letter].append(pattern)
    return pattern_dict


def number_of_matches(design, patterns):
    index = 0
    end = len(design)
    paths = [0]*end

    while index < end:

        for pattern_group in patterns:
            matches = False
            for pattern in patterns[pattern_group]:
                if design.startswith(pattern,index):
                    matches = True
                    break
            if matches:
                if index == 0:
                    paths[index + pattern_group - 1] = 1 if matches else 0
                else:
                    paths[index + pattern_group - 1] += paths[index-1] * (1 if matches else 0)
        
        index += 1

    return paths[end-1]

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
    patterns = list(map(str.strip, lines[0].strip().split(',')))
    patterns = make_pattern_dict(patterns)

    desired_designs = [ line.strip() for line in lines[2:]]

    matches = [ number_of_matches(design, patterns) for design in desired_designs]

    valid_designs = sum( 1 if match > 0 else 0 for match in matches)
    total_matches = sum(matches)

    print(f"Part 1: {valid_designs}")
    print(f"Part 2: {total_matches}")


if __name__ == "__main__":
    main()
