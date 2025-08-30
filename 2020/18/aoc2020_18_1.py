"""Advent of Code: 2020.1.1"""
import sys

def evaluate_exp(exp):
    """Parses and evaluare an expression"""
    results = exp.pop(0)
    if results == '(':
        results = evaluate_exp(exp)
    else:
        results = int(results)
    operator = ''

    # first = True

    while exp:
        cur = exp.pop(0)
        if cur == ' ':
            continue
        if cur == '(':
            cur = evaluate_exp(exp)
        if cur == ')':
            return results
        if cur == '+' or cur == '*':
            operator = cur
            continue
        # if first:
        #     results = cur
        #     first = False
        #     continue
        if operator == '+':
            results += int(cur)
            continue
        if operator == '*':
            results *= int(cur)

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

    sums = [ evaluate_exp( list(line.strip()) ) for line in lines ]

    print(sum(sums))


if __name__ == "__main__":
    main()
