"""Advent of Code: 2020.19.2

0: 8 11
8: 42 | 42 8            => 42 42 42 42 42; en serie med minst en 42
11: 42 31 | 42 11 31    => 42 42 42 31 31 31; like mange 42 som 31, 42er etterfulgt av 31er

Så godkjente stringer er en serie med 42 etterfulgt av 31, hvor antallet 31 er maks en 
mindre en 42er.

Alle 42 og 31 er 8 lange.
Message må være mod av 8. Alle er det.

Kan splitte message opp i 8 tegns stringer og matche mot 42 og 31.

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
            new_strings = [a+b for a in new_strings for b in ret_strings]

        all_strings += new_strings

    return list(set(all_strings))

def match_message(message, list_42, list_31):
    """ Matches message to 42 and 31s"""
    message_parts = len(message)

    # A message must have at least 3 parts
    if message_parts < 3:
        return False

    # Does it start with at least 2 42?
    if message[0] not in list_42 or message[1] not in list_42:
        return False

    match_to_42 = 2
    mp_index = 2

    # Match 42's
    while message[mp_index] in list_42:
        mp_index += 1
        match_to_42 += 1
        # Did we reach end of message?
        if mp_index == message_parts:
            return False

    # Match 31's, need to be at least one.
    if message[mp_index] not in list_31:
        return False
    mp_index += 1
    match_to_31 = 1

    for message_part in message[mp_index:]:
        if message_part not in list_31:
            break
        match_to_31 += 1

    # Did we match the hole message?
    if match_to_42 + match_to_31 != len(message):
        return False

    # Is the combination of 31 and 42 right?
    if match_to_42 - match_to_31 < 1:
        return False

    # We have a match
    return True

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
    split_messages = [[ message[i:i+8] for i in range(0,len(message),8)] for message in messages]

    strings_42 = translate('42',rules)
    strings_31 = translate('31',rules)

    valid_messages = [mesg for mesg in split_messages if match_message(mesg,strings_42,strings_31)]
    print(len(valid_messages))


if __name__ == "__main__":
    main()
