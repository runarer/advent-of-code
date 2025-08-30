import sys
"""
    Denne må optimaliseres. Finn set fra input.txt
    Kan jeg endre rules?
"""

def insert_elements(template, rules,steps=1):
    # Initiate and run first step
    rules_applied = {x:0 for x in rules.keys()}
    for i in range(len(template)-1):
        for rule in rules[template[i:i+2]]:
            rules_applied[rule] += 1
    
    for _ in range(steps-1):
        this_step = {x:0 for x in rules.keys()}
        for old_rule,apply in rules_applied.items():
            if apply > 0:
                for rule in rules[old_rule]:
                    this_step[rule] += apply
        rules_applied = this_step
    return rules_applied

def calc_final_number(rules_applied,elements,template):
    characters = {x:0 for x in elements}
    characters[template[ 0]] = 1
    characters[template[-1]] = 1
    for rule,value in rules_applied.items():
        for cha in rule:
            characters[cha] += value
    values = list(characters.values())
    values.sort()
    return int((values[-1]-values[0])/2)

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
    characters = set()
    for line in lines[2:]:
        old,insert = line.strip().split(" -> ")
        rules[old] = (old[0] + insert,insert + old[-1])
        characters.add(insert)
    
    rules_applied = insert_elements(template,rules,40)
    final_number = calc_final_number(rules_applied,characters,template)
    print(final_number)
    

if __name__ == "__main__":
    main()
