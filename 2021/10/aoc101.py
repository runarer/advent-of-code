import sys

def find_corruption_score(line):
    def score(character):
        if character == ')': return 3
        if character == ']': return 57
        if character == '}': return 1197
        if character == '>': return 25137
        return 0

    stack = []
    for c in line:
        if c in ['(','[','{','<']:
            stack.append(c)
            continue        
        if c == ')':
            if stack.pop() != '(':
                return score(c)
        if c == ']':
            if stack.pop() != '[':
                return score(c)
        if c == '}':
            if stack.pop() != '{':
                return score(c)
        if c == '>':
            if stack.pop() != '<':
                return score(c)
    return 0


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
    #Make border of 'X's    
    score = 0
    for line in lines:
        score += find_corruption_score(line.strip())
    print(score)


if __name__ == "__main__":
    main()
