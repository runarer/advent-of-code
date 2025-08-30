"""Advent of Code: 2020.16.1"""
import sys
import re

class Validator:
    """ Validates that numbers are in sets"""
    def __init__(self,rules):
        """ Rules is a list of tuples (from,to)"""
        rules.sort()
        self.rules = rules

    def is_valid(self,number):
        """Checks if number is in sets"""
        for from_with,to_with in self.rules:
            if number < from_with:
                return False
            if number > to_with:
                continue
            return True
        return False

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

    # Read rules
    rules = []
    tickets = []

    line_nr = 0
    while lines[line_nr].strip():
        results = re.match(r"^([a-z\s]+): (\d+)-(\d+) or (\d+)-(\d+)$",lines[line_nr])
        rules.append( ( int(results.group(2)),int(results.group(3)) ))
        rules.append( ( int(results.group(4)),int(results.group(5)) ))
        line_nr += 1

    # Read "my" ticket
    my_ticket = lines[line_nr + 2].split(',')
    my_ticket = [ int(field) for field in my_ticket]

    # Read other tickets
    for line in lines[line_nr + 5:]:
        ticket = line.split(',')
        ticket = [ int(field) for field in ticket]
        tickets.append(ticket)

    # Find invalid numbers
    validaror = Validator(rules)
    invalid_nrs = [ sum([ number for number in ticket if not validaror.is_valid(number)]) \
                    for ticket in tickets ]
    print( sum(invalid_nrs) )

if __name__ == "__main__":
    main()
