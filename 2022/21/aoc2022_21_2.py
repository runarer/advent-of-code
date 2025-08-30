"""Advent of Code: 2022.21.2"""
import sys

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
    lines = [line.strip().split() for line in lines]
    numbers = { line[0].split(':')[0] : int(line[1]) for line in lines if len(line) == 2}
    del numbers['humn']
    calculations = { line[0].split(':')[0] : line[1:] for line in lines if len(line) == 4}
    calculations['root'][1] = '='

    changes = True
    while changes:
        to_remove = []
        changes = False
        for monkey, calc in calculations.items():
            if calc[0] in numbers:
                changes = True
                calc[0] = numbers[calc[0]]
            if calc[2] in numbers:
                changes = True
                calc[2] = numbers[calc[2]]
            if isinstance(calc[0],int) and isinstance(calc[2],int):
                if calc[1] == '+':
                    numbers[monkey] = calc[0] + calc[2]
                elif calc[1] == '-':
                    numbers[monkey] = calc[0] - calc[2]
                elif calc[1] == '*':
                    numbers[monkey] = calc[0] * calc[2]
                elif calc[1] == '/':
                    changes = True
                    numbers[monkey] = int(calc[0] / calc[2])
                to_remove.append(monkey)
        for monkey in to_remove:
            del calculations[monkey]

    humn = 0
    monkey = 'root'
    if isinstance(calculations['root'][0],int):
        humn = calculations['root'][0]
        monkey = calculations['root'][2]
    else:
        humn = calculations['root'][2]
        monkey = calculations['root'][0]
    del calculations['root']

    while calculations:
        next_monkey = 0
        number = 0
        number_first = False
        if isinstance(calculations[monkey][0],int):
            number = calculations[monkey][0]
            next_monkey = calculations[monkey][2]
            number_first = True
        else:
            number = calculations[monkey][2]
            next_monkey = calculations[monkey][0]

        if calculations[monkey][1] == '+':
            humn -= number
        elif calculations[monkey][1] == '-':
            if number_first:
                humn = number - humn
            else:
                humn = humn + number
        elif calculations[monkey][1] == '*':
            humn = int(humn / number)
        elif calculations[monkey][1] == '/':
            humn *= number

        del calculations[monkey]
        monkey = next_monkey

    print(humn)
    


if __name__ == "__main__":
    main()
