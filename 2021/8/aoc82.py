import sys

def desiffer_scrambled_digits(input_digits):
    output_digits = ["" for x in range(10)]

    for digit in input_digits:
        #Find 1
        if len(digit) == 2:
            output_digits[1] = ''.join(sorted(digit))
            continue
        #Find 4
        if len(digit) == 4:
            output_digits[4] = ''.join(sorted(digit))
            continue
        #Find 7
        if len(digit) == 3:
            output_digits[7] = ''.join(sorted(digit))
            continue
        #Find 8
        if len(digit) == 7:
            output_digits[8] = ''.join(sorted(digit))
            continue

    b_and_d = [c for c in output_digits[4] if c not in output_digits[1]]

    for digit in input_digits:
        #Find 0,6 or 9
        if len(digit) == 6:
            if output_digits[1][0] not in digit or output_digits[1][1] not in digit:
                output_digits[6] = ''.join(sorted(digit))
            else:
                for cha in output_digits[4]:
                    if cha not in digit:
                        break
                else:
                    output_digits[9] = ''.join(sorted(digit))
                    continue
                output_digits[0] = ''.join(sorted(digit))
                continue
        #Find 2,3 or 5
        if len(digit) == 5:
            #Find 3
            if output_digits[1][0] in digit and output_digits[1][1] in digit:
                output_digits[3] = ''.join(sorted(digit))
                continue
            #Find 2 or 5
            for cha in b_and_d:
                if cha not in digit:
                    break
            else:
                output_digits[5] = ''.join(sorted(digit))
                continue
            output_digits[2] = ''.join(sorted(digit))
    return output_digits

def desiffer_scrambled_numbers(digits, numbers):
    number = 0
    for i,n in enumerate(reversed(numbers)):
        number += digits.index(''.join(sorted(n))) * (10**i)
    return number

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

    sum_of_all_numbers = 0
    for line in lines:
        splitt_line = line.split('|')
        digits = desiffer_scrambled_digits(splitt_line[0].strip().split())
        sum_of_all_numbers += desiffer_scrambled_numbers(digits, splitt_line[1].strip().split())
    print(sum_of_all_numbers)


if __name__ == "__main__":
    main()