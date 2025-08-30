"""Advent of Code: 2019.1.1"""
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
    calculations = { line[0].split(':')[0] : line[1:] for line in lines if len(line) == 4}

    while calculations:
        to_remove = []
        for monkey, calc in calculations.items():
            if calc[0] in numbers:
                calc[0] = numbers[calc[0]]
            if calc[2] in numbers:
                calc[2] = numbers[calc[2]]
            if isinstance(calc[0],int) and isinstance(calc[2],int):
                # print(monkey,calc)
                if calc[1] == '+':
                    numbers[monkey] = calc[0] + calc[2]
                elif calc[1] == '-':
                    numbers[monkey] = calc[0] - calc[2]
                elif calc[1] == '*':
                    numbers[monkey] = calc[0] * calc[2]
                elif calc[1] == '/':
                    numbers[monkey] = int(calc[0] / calc[2])
                to_remove.append(monkey)
        for monkey in to_remove:
            del calculations[monkey]
        # print(calculations)

    print(numbers['root'])
    # print(numbers)
    # print(calculations)


if __name__ == "__main__":
    main()
