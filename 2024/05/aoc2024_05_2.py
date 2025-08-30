"""Advent of Code: 2024.5.2"""
import sys

# I can combine the two below.

def valid(update, rules):
    valid = True
    for i, page in enumerate(update):
        if page not in rules:
            continue
        for next_page in update[i:]:
            if next_page in rules[page]:
                valid = False
                break
        if not valid:
            break
        
    return valid

def order(update, rules):
    page_i = 0
    while page_i != len(update):
        page = update[page_i]

        if page not in rules:
            page_i += 1
            continue

        for next_page_i in range(page_i+1,len(update)):
            next_page = update[next_page_i]
            if next_page in rules[page]:
                # Need to move next_page before page
                update.pop(next_page_i)
                update.insert(page_i,next_page)
                page_i -= 1 # Check at index again.
                break
        page_i += 1



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
    # For each page, there's a set of pages that needs to be before that page.
    rules = {}
    updates = []
    
    rules_done = False
    for line in lines:
        if line == '\n':
            rules_done = True
            continue

        if not rules_done:
            page_before, page_after = map(int,line.strip().split('|'))
            if page_after in rules:
                rules[page_after].append(page_before)
            else:
                rules[page_after] = [page_before]
        else:
            updates.append( list(map( int, line.strip().split(',') ) ) )

    # for each page in update, is any or the next pages in the before set?
    fixed_updates = 0
    for update in updates:
        if not valid(update,rules):            
            order(update,rules)
            fixed_updates += update[len(update)//2]
    print(fixed_updates)
        
            
    

            
    
    # print(rules)
    # print(updates)


if __name__ == "__main__":
    main()
