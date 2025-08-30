"""Advent of Code: 2022.11.1"""
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
    monkeys = {}

    # Kunne brukt flere liste hvor monkey nummer er 'pekeren'


    for monkey in monkey_input:
        number = int(monkey[0].split()[1][:-1]) # 'Monkey 0:' get number, remove last ':'

        new_monkey = {'inspected':0}
        new_monkey['items'] = list(map(int,monkey[1].split(':')[1].split(','))) # 'Starting items: 86, 70, 71, 56'
        m_op = monkey[2].split('=')[1].split() # 'Operation: new = old + 1'
        new_monkey['operation'] = eval(f"lambda old: int(({m_op[0]} {m_op[1]} {m_op[2]})/3)")
        new_monkey['divide'] = int(monkey[3].split()[-1]) # 'Test: divisible by 11'
        new_monkey['true']  = int(monkey[4].split("monkey")[-1]) # 'If true: throw to monkey 7'
        new_monkey['false'] = int(monkey[5].split("monkey")[-1]) # 'If false: throw to monkey 6'

        monkeys[number] = new_monkey

    for _ in range(20):
        for monkey in monkeys.values():
            # Inspect
            monkey['inspected'] += len(monkey['items'])
            monkey['items'] = list(map(monkey['operation'],monkey['items']))

            # Send around items
            monkeys[monkey['true']]['items'] += [ item for item in monkey['items'] if not item % monkey['divide']]
            monkeys[monkey['false']]['items'] += [ item for item in monkey['items'] if item % monkey['divide']]
            monkey['items'] = []

    inspections = []
    for n,monkey in monkeys.items():
        inspections.append(monkey['inspected'])
        print(f"Monkey {n} inspected items {monkey['inspected']} times.")

    inspections.sort()
    print(inspections[-1]*inspections[-2])

if __name__ == "__main__":
    main()

