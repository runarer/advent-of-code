import sys

def insert_elements(template, rules):
    new_template = ""
    for i in range(len(template)-1):
        new_template += rules[template[i:i+2]]
    return new_template + template[-1]

def calc_final_number(template):
    largest  = 0
    smallest = len(template)
    for cha in set(template):
        count = template.count(cha)
        if count > largest:
            largest = count
        if count < smallest:
            smallest = count
    return largest - smallest

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
    template = lines[0].strip()
    rules = {}
    for line in lines[2:]:
        old,insert = line.strip().split(" -> ")
        rules[old] = old[0] + insert
    for _ in range(10):
        template = insert_elements(template,rules)
    value = calc_final_number(template)
    print(value)

if __name__ == "__main__":
    main()
