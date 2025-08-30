"""Advent of Code: 2019.1.1"""
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
    sum_of_powers = 0

    for line in lines:
        line = line.strip()
        game_id_and_games = line.split(':')
        rounds = game_id_and_games[1].split(';')

        cubes = {"red" : 0, "green" : 0, "blue" : 0 }

        for r in rounds:
            draws = r.split(',')
            while draws:
                number_and_colour = draws.pop().split()

                number_of_cubes = int(number_and_colour[0])
                colour_of_cubes = number_and_colour[1]

                if cubes[colour_of_cubes] < number_of_cubes:
                    cubes[colour_of_cubes] = number_of_cubes
            
        sum_of_powers += cubes["red"] * cubes["blue"] * cubes["green"]

    print(sum_of_powers)

if __name__ == "__main__":
    main()
