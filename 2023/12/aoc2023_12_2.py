"""
    Advent of Code: 2019.1.1

    First number in dmg becomes, if 3, 1110 and 0 for each min length of the rest.
    So for 3,2,1 we have; 11100000, 1100 and 1. If we add these togeter we get first permutation.
    We can then apply 'row' as a mask to check if it is legal.
    
"""
import sys, itertools as it

def remove_unchangable(row):
    while row["row"].startswith('#'):
        #print(f"Start with #: {row["row"]}")
        remove = row["dmg"].pop(0)
        if row["dmg"]:
            remove += 1
        row["row"] = row["row"][remove:].strip('.')
        #print(f"Start with # (new): {row["row"]} removed {remove}")
    while row["row"].endswith('#'):
        #print(f"Ends with #: {row["row"]}")
        remove = row["dmg"].pop()
        if row["dmg"]:
            remove += 1
        row["row"] = row["row"][:len(row["row"])-remove].strip('.')
        #print(f"Ends with # (new): {row["row"]} removed {remove}")

    # Did we exhast all possibilities
    if row["dmg"]:
        smallest_length = sum( i+1 for i in row["dmg"])-1
        max_length = len(row["row"])
        if smallest_length == max_length:
            row["dmg"].clear()
            row["row"] = ""
    else:
        row["row"] = ""
    return row

def perm(nr, numbers):
    if len(numbers) == 1:
        return [numbers[0]*(2**nr)]

    new_lists = []
    for i in range(nr+1):
        ret = perm(i,numbers[1:])
        for r in ret:
            new_lists.append(numbers[0]*(2**nr)+r)
    return new_lists

def count_variants(number_str,groups):
    #print(number_str,groups)
    must_be_zero = sum(2**i for i,c in enumerate(reversed(number_str)) if c == '.')
    #print(bin(must_be_zero))
    must_be_one =  sum(2**i for i,c in enumerate(reversed(number_str)) if c == '#')
    #print(bin(must_be_one))
    min_length = sum(groups) + len(groups) - 1
    max_length = len(number_str)

    if min_length == max_length:
        return 1

    numbers = []
    for i,t in enumerate(groups):
        min_l = sum(groups[i:]) + len(groups[i:]) - 1
        nr = sum( 2**j for j in range(min_l-t,min_l) )
        numbers.append(nr)
    #print(numbers)

    first_var = sum(numbers)
    vars = 0
    if (first_var & must_be_zero) == 0 and (first_var & must_be_one) == must_be_one:
        vars += 1

    for i in range(1,max_length-min_length+1):
        gg = perm(i,numbers)
        for g in gg:
            if (g & must_be_zero) == 0 and (g & must_be_one) == must_be_one:
                vars += 1
                #print("Zero",bin(g))

    return vars

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
    springs = [ {"row" : c[0].strip('.'), "dmg": list(map(int,c[1].split(','))) } for line in lines if (c := line.split()) ]
    #sss = 0
    #for s in springs:
    #    nn =count_variants(s["row"],s["dmg"])
    #    if nn == 0:
    #        print(s)
    #    sss += nn
    #print(sss)
    for s in springs:
        print(s["row"]+"?"+s["row"]+"?"+s["row"]+"?"+s["row"]+"?"+s["row"])
        print(s["dmg"]*5)
        print(count_variants(s["row"]+"?"+s["row"]+"?"+s["row"]+"?"+s["row"]+"?"+s["row"],s["dmg"]*5))

    #print( sum(count_variants(s["row"]+"?"+s["row"]+"?"+s["row"]+"?"+s["row"]+"?"+s["row"],s["dmg"]*5) for s in springs))


    #to_bin = str.maketrans(".?#","001")
    #number_str = "??..??"    
    #adding_numbers = [ 2**i for i,c in enumerate(reversed(number_str)) if c == '?']
    #number =  sum(2**i for i,c in enumerate(reversed(number_str)) if c == '#')

    #number_to_add = sum([1,1]) - number_str.count('#')

    #n = int(number_str.translate(to_bin),2)

    #print(f"{number} to {number.translate(to_bin)} {int(number.translate(to_bin),2)} {number_to_add}")
    #for perm in it.combinations(adding_numbers,r=number_to_add):
    #    print(bin(number+sum(perm)))

    #springs = [ {"row" : c[0].strip('.'), "dmg": list(map(int,c[1].split(','))) } for line in lines if (c := line.split()) ]
    #springs = map(remove_unchangable,springs)
    #for s in springs:
    #    print(s)

if __name__ == "__main__":
    main()


