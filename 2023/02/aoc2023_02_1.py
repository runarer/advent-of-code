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
    red = 12
    green = 13
    blue = 14

    sum_of_game_ids = 0

    for line in lines:
        line = line.strip()
        game_id_and_games = line.split(':')
        rounds = game_id_and_games[1].split(';')

        game_is_possible = True

        for r in rounds:
            draws = r.split()
            while draws:
                colour_of_cubes = draws.pop().strip(',')
                number_of_cubes = draws.pop()
                if colour_of_cubes == 'red' and int(number_of_cubes) > red:
                    game_is_possible = False
                elif colour_of_cubes == 'green' and int(number_of_cubes) > green:
                    game_is_possible = False
                elif colour_of_cubes == 'blue' and int(number_of_cubes) > blue:
                    game_is_possible = False

            if not game_is_possible:
                break

        if game_is_possible:
            sum_of_game_ids += int(game_id_and_games[0][5:])
            print(game_id_and_games[0][5:])

    print(sum_of_game_ids)


if __name__ == "__main__":
    main()
