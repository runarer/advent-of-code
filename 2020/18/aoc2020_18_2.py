"""Advent of Code: 2020.18.2"""
import sys

def evaluate(exp):
    """ Deals with parenteces """
    expr = []

    while exp:
        cur = exp.pop(0)
        if cur == ')':
            break
        if cur == '(':
            expr.append( evaluate(exp) )
        else:
            expr.append(cur)

    return evaluate_sub(expr)

def evaluate_sub(exp):
    """ Evaluate expressions without parenteces. """
    results = int(exp.pop(0))
    operator = ''

    while exp:
        cur = exp.pop(0)
        if cur == '+':
            operator = cur
            continue
        if cur == '*':
            results *= evaluate_sub(exp)
            return results
        if operator == '+':
            results += int(cur)
            continue

    return results


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

    sums = [ list(line.strip()) for line in lines ]
    sums = [ [char for char in line if char != ' '] for line in sums]
    sums = [ evaluate(exp) for exp in sums ]
    print(sum(sums))


if __name__ == "__main__":
    main()
