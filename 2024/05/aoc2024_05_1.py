"""Advent of Code: 2024.5.1"""
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
    valid_updates = 0
    for update in updates:
        unvalid = False
        for i, page in enumerate(update):
            if page not in rules:
                continue
            for next_page in update[i:]:
                if next_page in rules[page]:
                    unvalid = True
                    break
            if unvalid:
                break
        if not unvalid:            
            valid_updates += update[len(update)//2]
            # print(update)
            
    print(valid_updates)

            
    
    # print(rules)
    # print(updates)


if __name__ == "__main__":
    main()
