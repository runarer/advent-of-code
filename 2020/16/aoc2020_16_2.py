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

    def is_all_valid(self,numbers):
        """Check if all numbers in a list is valid"""
        for number in numbers:
            if not self.is_valid(number):
                return False
        return True

def all_in_range(ranges,numbers):
    """ss"""
    ff_range,fs_range = ranges[0]
    sf_range,ss_range = ranges[1]

    for number in numbers:
        if (ff_range <= number <= fs_range) or (sf_range <= number <= ss_range):
            continue
        else:
            return False
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

    # Read rules
    rules = []
    tickets = []
    fields = {}
    field_nrs = []

    line_nr = 0
    while lines[line_nr].strip():
        results = re.match(r"^([a-z\s]+): (\d+)-(\d+) or (\d+)-(\d+)$",lines[line_nr])
        name = results.group(1)
        first_range = ( int(results.group(2)),int(results.group(3)) )
        second_range = ( int(results.group(4)),int(results.group(5)) )
        rules.append(first_range )
        rules.append(second_range)

        fields[name] = (first_range,second_range)

        line_nr += 1

    # Read "my" ticket
    my_ticket = lines[line_nr + 2].split(',')
    my_ticket = [ int(field) for field in my_ticket]

    # Read other tickets
    for line in lines[line_nr + 5:]:
        ticket = line.split(',')
        ticket = [ int(field) for field in ticket]
        tickets.append(ticket)

    # Remove invalid tickets
    validaror = Validator(rules)
    tickets = [ticket for ticket in tickets if validaror.is_all_valid(ticket)]

    # create filed numbers
    for field in my_ticket:
        field_nrs.append( [field] )
    for ticket in tickets:
        for i,field in enumerate(ticket):
            field_nrs[i].append(field)

    # Find matching fields
    matching_fields = [ [] for _ in field_nrs]
    for i,numbers in enumerate(field_nrs):
        for name,ranges in fields.items():
            if all_in_range(ranges,numbers):
                matching_fields[i].append(name)

    # Reduce fields
    matches = {}
    done = False
    while not done:
        done = True
        # find one with only one match
        match = ""
        for i,m_field in enumerate(matching_fields):
            if len(m_field) == 1:
                match = m_field[0]
                matches[match] = i
                done = False
        # remove
        for m_field in matching_fields:
            if match in m_field:
                m_field.remove(match)

    # Calculate answer
    all_dep = my_ticket[matches["departure location"]] * \
              my_ticket[matches["departure station"]] * \
              my_ticket[matches["departure platform"]] * \
              my_ticket[matches["departure track"]] * \
              my_ticket[matches["departure date"]] * \
              my_ticket[matches["departure time"]]

    print(all_dep)
if __name__ == "__main__":
    main()
