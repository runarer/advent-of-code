"""Advent of Code: 2024.21.1

    The keypad and the arrowpad are both bidirectional graphs.
    However they are so small that using pathfinding for the movements
    is unnessesary. A lookup table with 'from', 'to' and all the needed moves
    will be way faster.  

"""
import sys

# Make some graphs, manual input
key_graph = {
    '0': [('2','^'),('A','>')], 
    '1': [('2','<'),('4','^'),('A','v')],
    '2': [('0','v'),('3','<'),('5','^'),('1','>')],
    '3': [('2','>'),('6','^')],
    '4': [('1','v'),('5','<'),('7','^')],
    '5': [('2','v'),('4','>'),('6','<'),('8','^')],
    '6': [('9','^'),('5','>'),('3','v')],
    '7': [('4','v'),('8','<')],
    '8': [('9','<'),('5','v'),('7','>')],
    '9': [('6','v'),('8','>')],
    'A': [('0','<'),('1','^')]
}

arrow_graph = {
    '^': [('v','v'),('A','>')],
    'v': [('^','^'),('>','>'),('<','<')],
    '<': [('v','>')],
    '>': [('v','<'),('A','^')],
    'A': [('^','<'),('>','v')]
}


def find_shortest_path(graph : dict[str,list[tuple[str,str]]], start : str, target: str):
    pass

def build_lookup_table(graph : dict[str,list[tuple[str,str]]]):
    keys = graph.keys()

    lookup_table ={}
    
    for from_key in keys:
        lookup_table[from_key] = {}
        for to_key in keys:
            lookup_table[from_key][to_key] = find_shortest_path(graph,from_key,to_key)

    return lookup_table

keypad = build_lookup_table(key_graph)
arrowpad = build_lookup_table(arrow_graph)

def calculate_moves(graph,seqence):
    pass

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
    input_lines = []

    for line in lines:
        keypad_input = calculate_moves(keypad,line)
        first_arrowpad_input = calculate_moves(arrowpad,keypad_input)
        second_arrowpad_input = calculate_moves(arrowpad,first_arrowpad_input)
        final_arrowpad_input = calculate_moves(arrowpad,second_arrowpad_input)

        input_lines.append((line,final_arrowpad_input))


    part1 = sum(len(input)*int(line[:-1]) for line,input in input_lines)


    print(f"Part 1: {None}")

if __name__ == "__main__":
    main()
