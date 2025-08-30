"""Advent of Code: 2022.11.2"""
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
    lines = [line.strip() for line in lines]
    monkey_input = [ lines[x:x+6] for x in range(0,len(lines),7)]

    items = []
    inspected = []
    operation = []
    divide = []
    true = []
    false = []
    monkeys = 0

    # Klokk som alle gir riktig svar etter 0 -> 9 699 690

    for monkey in monkey_input:
        monkeys = int(monkey[0].split()[1][:-1]) + 1 # 'Monkey 0:' get number, remove last ':'

        inspected.append(0)
        items.append( list(map(int,monkey[1].split(':')[1].split(','))) ) # 'Starting items: 86, 70, 71, 56'
        m_op = monkey[2].split('=')[1].split() # 'Operation: new = old + 1'
        operation.append(eval(f"lambda old: {m_op[0]} {m_op[1]} {m_op[2]}"))
        divide.append(int(monkey[3].split()[-1])) # 'Test: divisible by 11'
        true.append(int(monkey[4].split("monkey")[-1])) # 'If true: throw to monkey 7'
        false.append(int(monkey[5].split("monkey")[-1])) # 'If false: throw to monkey 6'

    max_integer = 1
    for number in divide:
        max_integer *= number

    for _ in range(10000):
        for monkey in range(monkeys):
            # Inspect
            inspected[monkey] += len(items[monkey])
            items[monkey] = [ operation[monkey](item) % max_integer for item in items[monkey] ]

            # Send around items
            items[true[monkey]] += [ item for item in items[monkey] if not item % divide[monkey] ]
            items[false[monkey]] += [ item for item in items[monkey] if item % divide[monkey] ]

            items[monkey] = []

    for n in range(monkeys):        
        print(f"Monkey {n} inspected items {inspected[n]} times.")

    inspected.sort()
    print(inspected[-1]*inspected[-2])

if __name__ == "__main__":
    main()


# 20733696060


# Divisible by 19

# Divisible by 17

# Divisible by 13

# Divisible by 11

# Divisible by 7
# Three digit or larger,
# 1. double last digit
# 2. subtract the doubled last digit from second and third digit
# 3. Is what remain dividable by 7?
# 161 -> 16 - 2 = 14 -> 14 / 2 = 1

# Divisible by 5
# Last digit 0 or 5

# Divisible by 3


# Divisible by 2
# Last digit even
# Monkey 0 inspected items 33 times.
# Monkey 1 inspected items 31 times.
# Monkey 2 inspected items 34 times.
# Monkey 3 inspected items 34 times.
# Monkey 4 inspected items 3 times.
# Monkey 5 inspected items 34 times.
# Monkey 6 inspected items 34 times.
# Monkey 7 inspected items 16 times.
# 1156
# [0, 3, 3, 4, 6, 2, 2, 3, 5, 4, 4, 6, 7, 2, 0, 0, 5, 5, 4, 4, 6, 2, 2, 0, 0, 3, 3, 5, 1, 6, 6, 2, 2, 3, 5, 1, 6, 6, 2, 2, 0, 0, 3, 3, 5, 1, 6, 6, 7, 2, 0, 0, 3, 3, 5, 1, 6, 6, 2, 2, 0, 0, 3, 3, 5, 1, 6, 6, 7, 2, 0, 0, 3, 3, 5, 
# 1, 6, 6, 2, 2, 0, 0, 3, 3, 5, 1, 6, 6, 7, 2, 0, 0, 3, 3, 5, 1, 6, 6, 2, 2, 0, 0, 3, 3, 5, 1, 6, 6, 7, 2, 0, 0, 3, 3, 5, 1, 6, 6, 2, 2, 0, 0, 3, 3, 5, 1, 6, 6, 7, 2, 0, 0, 3, 3, 5, 1, 6, 6, 2, 2, 0, 0, 3, 3, 5, 1, 6, 6, 7, 2, 0, 0, 3, 3, 5, 1, 6, 6, 2, 2, 0, 0, 3, 3, 5, 1, 6, 6, 7, 2, 0, 0, 3, 3, 5, 1, 6, 6, 2, 2, 0, 0, 3, 3, 5, 1, 6, 6, 7, 2, 0, 0, 3, 3, 5, 1, 6, 6, 2, 2, 0, 0, 3, 3, 5, 1, 6, 6, 7, 2, 0, 0, 3, 3, 5, 1, 6, 6, 2, 2, 0, 0, 3, 3, 5, 1, 6, 6, 7, 2, 0, 0, 3, 3, 5, 1, 6, 6, 2, 2, 0, 0, 3, 3, 5, 1, 6, 6, 7, 2, 0, 0, 3, 3, 5, 1, 6, 6, 2, 2, 0, 0, 3, 3, 5, 1, 6, 6, 7, 2, 0, 0, 3, 3, 5, 1, 6, 6, 2, 2, 0, 0, 3, 3, 5, 1, 6, 6, 7, 2, 0, 0, 3, 3, 5, 1, 6, 6, 2, 2, 0, 
# 0, 3, 3, 5, 1, 6, 6, 7, 2, 0, 0, 3, 3, 5, 1, 6, 6, 2, 2, 0, 0, 3, 3, 5, 1, 6, 6, 7, 2, 0, 0, 3, 3, 5, 1]