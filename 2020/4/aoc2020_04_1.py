"""Advent of Code: 2020.4.1

Lag en liste av dictonary:
    Hvert pass er representert med en dict. 
    Bruk split() og så split(':') for key value.
    En blank linje er nytt pass.

"""
import sys

def build_passport_list(lines):
    """ Lager en liste med passord """
    passports = []

    current_passport = {}
    for line in lines:
        if line.strip():
            for field in line.split():
                key, val = field.split(':')
                current_passport[key] = val
        else:
            passports.append(current_passport)
            current_passport = {}
    passports.append(current_passport)
    return passports

def is_valid(passport):
    """Check if a password got all requiered fields."""
    required = ["byr","iyr","eyr","hgt","hcl","ecl","pid"]

    for field in required:
        if field not in passport:
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

    passports = build_passport_list(lines)
    valid_passports = 0
    for passport in passports:
        if is_valid(passport):
            valid_passports += 1

    print(valid_passports)

if __name__ == "__main__":
    main()
