"""Advent of Code: 2024.21.1

    Solved with recursion and memoization.

    The keypad and the arrowpad are both bidirectional graphs.
    However they are so small that using pathfinding for the movements
    is unnessesary. A lookup table with 'from', 'to' and all the needed moves
    will be way faster.  

"""
import sys

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

nr_robots = 25
moves_memoizations: list[dict[str,int]] = [{} for _ in range(nr_robots)] 

def moves(token:str,robots:int) -> int:
    current_robot = nr_robots - robots
    
    # end condition and shortcut
    if robots == 0:
        return len(token)
    
    if token in moves_memoizations[current_robot]:
        return moves_memoizations[current_robot][token]

    # Find tokens needed for this robot to do its job
    total_moves:int = 0

    position = 'A'
    for chr in token:
        first = moves(arrow_lookup[position][chr][0],robots-1)
        second = first + 1
        
        if len(arrow_lookup[position][chr]) > 1:
            second = moves(arrow_lookup[position][chr][1],robots-1)
        
        total_moves += min(first,second)

        position = chr

    moves_memoizations[current_robot][token] = total_moves

    return total_moves


def calculate_moves(lookup,seqence,position='A'):

    new_sequence = []

    for token in seqence:
        new_sequence += lookup[position][token]
        position = token

    return new_sequence



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
    part2 = 0

    for line in lines:
        line = line.strip()

        start = 'A'
        line_parts = list(line)
        line_size = 0
        for line_part in line_parts:
            next_sequence = calculate_moves(key_lookup,line_part,start)
         
            print(next_sequence)

            first = moves(next_sequence[0],nr_robots)
            second = first + 1
            
            if len(next_sequence) > 1:
                second = moves(next_sequence[1],nr_robots)
            line_size += min(first,second)
            start = line_part

        part2 += line_size*int(line[:-1])

    print(f"Part 2: {part2}")

if __name__ == "__main__":
    main()
