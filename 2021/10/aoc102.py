import sys

def uncorruptioned_line(line):
    stack = []
    for c in line:
        if c in ['(','[','{','<']:
            stack.append(c)
            continue
        if c == ')':
            if stack.pop() != '(':
                return False
        if c == ']':
            if stack.pop() != '[':
                return False
        if c == '}':
            if stack.pop() != '{':
                return False
        if c == '>':
            if stack.pop() != '<':
                return False
    return True

def autocomplete_score(line):
    stack = []
    for c in line:
        if c in ['(','[','{','<']:
            stack.append(c)
            continue
        if c in [')',']','}','>']:
            stack.pop()
            continue

    print(stack)

    score = 0
    stack.reverse()
    for c in stack:
        score *= 5
        if c == '(': score += 1
        if c == '[': score += 2
        if c == '{': score += 3
        if c == '<': score += 4
    return score

def main():
    """Start"""
    #get argument
    if len(sys.argv) < 1:
        sys.exit("Usage: python " + sys.argv[0] + " filename")
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except IOError as err:
        print("{}\nError opening {}. Terminating program.".format(err, filename), file=sys.stderr)
        sys.exit(1)

    scores = []
    for line in list(filter(uncorruptioned_line, lines)):
        print(line)
        scores.append(autocomplete_score(line))
    scores.sort()
    print(scores[int(len(scores)/2)])

if __name__ == "__main__":
    main()
