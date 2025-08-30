"""Advent of Code: 2019.1.1"""
import sys

def new_ranges(workflows,part_range,label):
    new_part_ranges = []
    cur_range = part_range.copy()

    more_ranges = True

    for condition,to in workflows[label][:-1]:
        part_rating = condition[0]
        part_value = condition[2]
        operant = condition[1]

        cur_rating = cur_range[part_rating]

        if operant == '>':
            if part_range[part_rating][1] > part_value and to != 'R':
                new_part_range = cur_range.copy()
                new_part_range[part_rating] = (max(cur_rating[0],part_value+1),cur_rating[1])
                new_part_ranges.append((new_part_range,to))
            if part_range[part_rating][0] <= part_value:
                cur_range[part_rating] = (cur_rating[0], min(part_value,cur_rating[1]) )
            else: # We are done
                more_ranges = False
                break
        else: # operant == '<'
            if part_range[part_rating][0] < part_value and to != 'R':
                new_part_range = cur_range.copy()
                new_part_range[part_rating] = ( cur_rating[0], min(cur_rating[1],part_value-1))
                new_part_ranges.append((new_part_range,to))
            if part_range[part_rating][1] >= part_value:
                cur_range[part_rating] = (max(part_value,cur_rating[0]),cur_rating[1])
            else: # We are done
                more_ranges = False
                break
    if more_ranges:
        new_part_ranges.append( (cur_range, workflows[label][-1]) )

    return new_part_ranges

def split_workflow(line):
    workflow = []

    conditions = line[line.index('{')+1:-1].split(',')
    for condition in conditions[:-1]:
        con, to = condition.split(':')
        workflow.append( ((con[0],con[1],int(con[2:])),to) )
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

    ranges = [ ({'x' :(1,4000),'m' : (1,4000),'a' : (1,4000),'s' : (1,4000)},"in") ]
    accepted = []

    while ranges:
        new_rang = new_ranges(workflows,*ranges.pop() )
        for rang in new_rang:
            if rang[1] == 'A':
                accepted.append(rang[0])
            elif rang[1] == 'R':
                continue
            else:
                ranges.append(rang)

    t = sum( ((a['x'][1]-a['x'][0])+1)*((a['m'][1]-a['m'][0])+1)*((a['a'][1]-a['a'][0])+1)*((a['s'][1]-a['s'][0])+1) for a in accepted)
    print(t)



if __name__ == "__main__":
    main()
