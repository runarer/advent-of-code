variants = 0
    for row in springs:
        variants += 1
        #print(row)
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
        if not row["dmg"]:
            continue
        
        smallest_length = sum( i+1 for i in row["dmg"])-1
        max_length = len(row["row"])
        if smallest_length == max_length:
            #print(f"Just one: {row}")
            continue
        print(row)



# def perm(nr,depth):
#     if depth == 1:
#         return [[nr]]
#
#     new_lists = []
#     for i in range(nr+1):
#         ret = perm(i,depth-1)
#         for r in ret:
#             new_lists.append([nr]+r)
#     return new_lists