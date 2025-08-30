"""Advent of Code: 2019.1.1"""
import sys
from functools import partial

def less(key,value,part):
    return part[key] < value

def greater(key,value,part):
    return part[key] > value

def split_part(line):
    values = line.split('=')
    return { 'x' : int(values[1][:-2]), 'm' : int(values[2][:-2]), \
             'a' : int(values[3][:-2]), 's' : int(values[4][:-1]), }

def split_workflow(line):
    workflow = []

    conditions = line[line.index('{')+1:-1].split(',')
    for condition in conditions[:-1]:
        con, to = condition.split(':')

        if con[1] == '>':
            workflow.append( (partial(greater,con[0],int(con[2:])),to) )
        elif con[1] == '<':
            workflow.append( (partial(less,con[0],int(con[2:])),to) )
        else:
            print("Wrong in operant selection")
    workflow.append(conditions[-1])
    return workflow

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
    workflows = { line[0:line.index('{')] : split_workflow(line.strip()) \
                 for line in lines if line[0].isalpha() }

    parts = [ split_part(line.strip()) for line in lines if line[0] == '{' ]

    accepted_parts = []

    for part in parts:
        accepted = False

        workflow = 'in'

        while not accepted:
            for condition,to in workflows[workflow][:-1]:
                if condition(part):
                    workflow = to
                    break
            else:
                workflow = workflows[workflow][-1]

            if workflow ==  'A':
                accepted = True
                break
            if workflow == 'R':
                accepted = False
                break

        if accepted:
            accepted_parts.append(part)

    print(sum( sum( apart.values() ) for apart in accepted_parts))


if __name__ == "__main__":
    main()
