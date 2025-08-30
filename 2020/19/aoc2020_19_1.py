"""Advent of Code: 2020.19.1
    Dette er en håpløs løsning. Burde lage en parser med reglene.
"""
import sys

def translate(rule,rules):
    """Returns a list of strings"""
    all_strings = []

    # If we are at the bottom
    if len(rules[rule]) == 1:
        if len(rules[rule][0]) == 1:
            if rules[rule][0][0].isalpha():
                return [rules[rule][0]]

    for one_of_rule in rules[rule]:
        new_strings = []
        for sub_rule in one_of_rule:
            if not new_strings:
                new_strings = translate(sub_rule,rules)
                continue
            ret_strings = translate(sub_rule,rules)
            new_strings = [a+b for a in new_strings for b in ret_strings] # replace with a function

        all_strings += new_strings

    return list(set(all_strings))


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

    rules = [line.strip().split(": ") for line in lines if line[0].isnumeric()]

    new_rules = {}
    for rule in rules:
        if rule[1][0] == '"' and rule[1][2] == '"':
            new_rules[ rule[0] ] = [rule[1][1]]
            continue
        new_rules[ rule[0] ] = []
        for pos in rule[1].split(" | "):
            new_rules[rule[0]].append(pos.split())
    rules = new_rules

    messages = [line.strip() for line in lines if line.strip().isalpha()]
    messages.sort()
    print(len(messages))

    valid_strings = translate('0',rules)
    valid_strings.sort()
    print(len(valid_strings))

    valid_messages = 0
    for message in messages:
        if message in valid_strings:
            valid_messages += 1
    print(valid_messages)


if __name__ == "__main__":
    main()
