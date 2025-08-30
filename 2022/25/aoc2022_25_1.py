"""Advent of Code: 2022.25.1"""
import sys

def snafu_to_decimal(snafu):
    """ Translate from insane number system to a normal one. """
    translation = {'2':2,'1':1,'0':0,'-':-1,'=':-2}
    decimal = 0
    multiplier = 1

    for sign in snafu[::-1]:
        decimal += translation[sign]*multiplier
        multiplier *= 5

    return decimal

def decimal_to_snafu(decimal):
    """"  DA"""
    number = decimal
    snafu = ""
    to_snafu = {0:'0',1:'1',2:'2',3:'=',4:'-'}
    while number > 0:
        new_number = int(number/5)
        reminder = number % 5
        snafu += to_snafu[reminder]
        if reminder > 2:
            new_number += 1
        number = new_number
    return snafu[::-1]

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
    numbers = [snafu_to_decimal(line.strip())  for line in lines]

    snafu_number = decimal_to_snafu(sum(numbers))
    print(snafu_number)


if __name__ == "__main__":
    main()
