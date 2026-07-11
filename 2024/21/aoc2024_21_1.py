"""Advent of Code: 2024.21.1

    The keypad and the arrowpad are both bidirectional graphs.
    However they are so small that using pathfinding for the movements
    is unnessesary. A lookup table with 'from', 'to' and all the needed moves
    will be way faster.  

    
    Need to rearrange the keypresses in lookuptables
    If we are in position 0 and wants to press 9 there are several paths,
    but ^^^<A will be the fastes for next level to do.
    If 0 or A do vertical position first.
    For the others to horizontal first.
"""
import sys

# Make some graphs, manual input
# key_graph = {
#     '0': {'2':'^','A':'>'},
#     '1': {'2':'>','4':'^'},
#     '2': {'0':'v','3':'>','5':'^','1':'<'},
#     '3': {'2':'<','6':'^','A':'v'},
#     '4': {'1':'v','5':'>','7':'^'},
#     '5': {'2':'v','4':'<','6':'>','8':'^'},
#     '6': {'9':'^','5':'<','3':'v'},
#     '7': {'4':'v','8':'>'},
#     '8': {'9':'>','5':'v','7':'<'},
#     '9': {'6':'v','8':'<'},
#     'A': {'0':'<','3':'^'}}

# arrow_graph = {
#     '^': {'v':'v','A':'>'},
#     'v': {'^':'^','>':'>','<':'<'},
#     '<': {'v':'>'},
#     '>': {'v':'<','A':'^'},
#     'A': {'^':'<','>':'v'}
# }

# def build_lookup_table(graph : dict[str,dict[str,str]]):
#     keys = graph.keys()

#     lookup_table ={}
    
#     for from_key in keys:
#         from collections import deque

#         lookup_table[from_key] = {from_key:''}
#         for next_key in graph[from_key]:
#             lookup_table[from_key][next_key] = graph[from_key][next_key]

#         queue = deque([(key,graph[from_key][key]) for key in graph[from_key]])
#         while queue:
#             key,movement = queue.popleft()

#             for n_key in graph[key]:
#                 if n_key in lookup_table[from_key]:
#                     continue

#                 lookup_table[from_key][n_key] = movement+graph[key][n_key]
#                 queue.append((n_key,lookup_table[from_key][n_key]))

#     for from_key in lookup_table:
#         for to_key in lookup_table[from_key]:
#             lookup_table[from_key][to_key] += 'A'


#     return lookup_table

# key_lookup = build_lookup_table(key_graph)
# arrow_lookup = build_lookup_table(arrow_graph)

# print(key_lookup)
# print(arrow_lookup)

# printed and manually changed, I dont know if this was faster.
key_lookup: dict[str, dict[str, list[str]]] = {
    '0': {'0': ['A'], '2': ['^A'], 'A': ['>A'], '3': ['^>A','>^A'], '5': ['^^A'], '1': ['^<A'], '6': ['^^>A','>^^A'], '4': ['^^<A'], '8': ['^^^A'], '9': ['^^^>A','>^^^A'], '7': ['^^^<A']}, 
    '1': {'1': ['A'], '2': ['>A'], '4': ['^A'], '0': ['>vA'], '3': ['>>A'], '5': ['>^A','^>A'], '7': ['^^A'], 'A': ['>>vA'], '6': ['>>^A','^>>A'], '8': ['>^^A','^^>A'], '9': ['>>^^A','^^>>A']}, 
    '2': {'2': ['A'], '0': ['vA'], '3': ['>A'], '5': ['^A'], '1': ['<A'], 'A': ['v>A','>vA'], '6': ['>^A','^>A'], '4': ['^<A','<^A'], '8': ['^^A'], '9': ['>^^A','^^>A'], '7': ['^^<A','<^^A']}, 
    '3': {'3': ['A'], '2': ['<A'], '6': ['^A'], 'A': ['vA'], '0': ['<vA','v<A'], '5': ['<^A','^<A'], '1': ['<<A'], '9': ['^^A'], '4': ['<<^A','^<<A'], '8': ['<^^A','^^<A'], '7': ['^^<<A','<<^^A']},
    '4': {'4': ['A'], '1': ['vA'], '5': ['>A'], '7': ['^A'], '2': ['v>A','>vA'], '6': ['>>A'], '8': ['>^A','^>A'], '0': ['>vvA'], '3': ['v>>A','>>vA'], '9': ['>>^A','^>>A'], 'A': ['>>vvA']}, 
    '5': {'5': ['A'], '2': ['vA'], '4': ['<A'], '6': ['>A'], '8': ['^A'], '0': ['vvA'], '3': ['v>A','>vA'], '1': ['v<A','<vA'], '7': ['<^A','^<A'], '9': ['>^A','^>A'], 'A': ['vv>A','>vvA']},     
    '6': {'6': ['A'], '9': ['^A'], '5': ['<A'], '3': ['vA'], '8': ['^<A','<^A'], '2': ['<vA','v<A'], '4': ['<<A'], 'A': ['vvA'], '7': ['^<<A','<<^A'], '0': ['<vvA','vv<A'], '1': ['<<vA','v<<A']},     
    '7': {'7': ['A'], '4': ['vA'], '8': ['>A'], '1': ['vvA'], '5': ['v>A','>vA'], '9': ['>>A'], '2': ['vv>A','>vvA'], '6': ['v>>A','>>vA'], '0': ['>vvvA'], '3': ['vv>>A','>>vvA'], 'A': ['>>vvvA']},
    '8': {'8': ['A'], '9': ['>A'], '5': ['vA'], '7': ['<A'], '6': ['>vA','v>A'], '2': ['vvA'], '4': ['v<A','<vA'], '3': ['>vvA','vv>A'], '0': ['vvvA'], '1': ['vv<A','<vvA'], 'A': ['>vvvA','vvv>A']},     
    '9': {'9': ['A'], '6': ['vA'], '8': ['<A'], '5': ['v<A','<vA'], '3': ['vvA'], '7': ['<<A'], '2': ['<vvA','vv<A'], '4': ['v<<A','<<vA'], 'A': ['vvvA'], '0': ['vvv<A','<vvvA'], '1': ['<<vvA','vv<<A']}, 
    'A': {'A': ['A'], '0': ['<A'], '3': ['^A'], '2': ['<^A','^<A'], '6': ['^^A'], '5': ['<^^A','^^<A'], '1': ['^<<A'], '9': ['^^^A'], '4': ['^^<<A'], '8': ['<^^^A','^^^<A'], '7': ['^^^<<A']}}


arrow_lookup: dict[str, dict[str, list[str]]] = {
    '^': {'^': ['A'], 'v': ['vA'], 'A': ['>A'], '>': ['v>A','>vA'], '<': ['v<A']}, 
    'v': {'v': ['A'], '^': ['^A'], '>': ['>A'], '<': ['<A'], 'A': ['^>A','>^A']}, 
    '<': {'<': ['A'], 'v': ['>A'], '^': ['>^A'], '>': ['>>A'], 'A': ['>>^A']}, 
    '>': {'>': ['A'], 'v': ['<A'], 'A': ['^A'], '^': ['<^A','^<A'], '<': ['<<A']}, 
    'A': {'A': ['A'], '^': ['<A'], '>': ['vA'], 'v': ['<vA','v<A'], '<': ['v<<A']}}

# take a list of list; for each list find all possible new lists
def calculate_moves(lookup,seqences,position='A'):

    new_sequences = []

    for seqence in seqences:

        current_new_sequences = []

        for token in seqence:
            if not current_new_sequences:
                current_new_sequences += lookup[position][token]
            else:
                temp = []
                for line in current_new_sequences:
                    temp.append(line+lookup[position][token][0])
                    if len(lookup[position][token]) > 1:
                        temp.append(line+lookup[position][token][1])
                current_new_sequences = temp.copy()

            position = token

        new_sequences += current_new_sequences

    # return list of list, the shortest ones
    shortest = min(len(line) for line in new_sequences)
    return [line for line in new_sequences if len(line) == shortest]

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

    part1 = 0

    for line in lines:
        line = line.strip()
        next_sequence = calculate_moves(key_lookup,[line])
        for _ in range(2):
            next_sequence = calculate_moves(arrow_lookup,next_sequence)

        part1 += len(list(next_sequence)[0])*int(line[:-1])


    print(f"Part 1: {part1}")

if __name__ == "__main__":
    main()



# 029A: <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
# 029A: <vA<AA>>^AvAA<^A>Av<<A>>^AvA^A<vA^>Av<<A>^A>AAvA^Av<<A>A^>AAA<Av>A^A

# 980A: <v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A
# 980A: v<<A>>^AAAvA^A<vA<AA>>^AvAA<^A>Av<<A>A^>AAA<Av>A^A<vA^>A<A>A

# 179A: <v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
# 179A: v<<A>>^A<vA<A>>^AAvAA<^A>Av<<A>>^AAvA^A<vA^>AA<A>Av<<A>A^>AAA<Av>A^A

# 456A: <v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A
# 456A: v<<A>>^AA<vA<A>>^AAvAA<^A>A<vA^>A<A>A<vA^>A<A>Av<<A>A^>AA<Av>A^A

# 379A: <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
#       v<<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA^>AA<A>Av<<A>A^>AAAvA<^A>A
# 379A: v<<A>>^AvA^Av<<A>>^AA<vA<A>>^AAvAA<^A>A<vA^>AA<A>Av<<A>A^>AAA<Av>A^A
#       v<<A>>^AvA^Av<<A>>^AA<vA<A>>^AAvAA<^A>A<vA^>AA<A>Av<<A>A^>AAA<Av>A^A



# 379A: <v<A >>^A vA ^A <vA <A A >>^A A vA <^A >A A vA ^A <vA >^A A <A >A <v<A >A >^A A A vA <^A >A
# 379A: <A >A v<<A A >^A A >A vA A ^A <vA A A >^A
# 379A: ^A <<^^A >>A vvvA
# 379A: 3 7 9 A

# 254470 to high
# 246990


# <A>A<AAv<AA>>^AvAA^A<vAAA^>A
# <A>Av<<AA>^AA>AvAA^A<vAAA^>A