"""Advent of Code: 2019.1.1"""
import sys

def find_rows(pattern):
    rows = 0

    # Find potesial reflections
    count_rows = 1
    length = len(pattern)

    for i in range(length-1):
        if pattern[i] == pattern[i+1]:
            reflection = True

            check1 = i
            check2 = i + 1
            while check1 and check2 < length-1:
                check1 -= 1
                check2 += 1
                if pattern[check1] != pattern[check2]:
                    reflection = False
                    break
            if reflection:
                rows = count_rows
                print("Horizontal reflections")
        count_rows += 1

    return rows

def find_cols(pattern):
    cols = 0
    length = len(pattern[0])
    depth = len(pattern)
    count_cols = 0

    for i in range(length-1):
        count_cols += 1
        reflection = True
        ref_len = min(i+1,length-i-1)

        for j in range(depth):
            check1 = i
            check2 = i+1
            for _ in range(ref_len):
                if pattern[j][check1] != pattern[j][check2]:
                    reflection = False
                    break
                check1 -= 1
                check2 += 1

        if reflection:
            cols = count_cols
            print("Vertical reflections")

    return cols

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
    patterns = [[]]
    pattern_index = 0
    for line in lines:
        if (l := line.strip()):
            patterns[pattern_index].append(l)
        else:
            patterns.append([])
            pattern_index += 1

    summarization = 0
    for pattern in patterns:
        print(pattern)
        cols = find_cols(pattern)
        rows = 0
        if cols == 0:
            rows = find_rows(pattern)
        summarization += cols + rows*100

    print(summarization)



if __name__ == "__main__":
    main()
