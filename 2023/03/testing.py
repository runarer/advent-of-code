dict1 = {'a': 1 ,'b': 2 ,'c': 3 ,'d': 4}
dict2 = {'d','c','e','f'}

for o in dict1.keys() & dict2:
    print(o)