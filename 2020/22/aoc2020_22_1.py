"""Advent of Code: 2020.22.1"""
import sys

def create_decks(lines,player_1,player_2):
    """ Fills out the decks """
    next_player = 0
    for nr,line in enumerate(lines[1:]):
        if line.strip():
            player_1.append(int(line))
        else:
            next_player = 3 + nr
            break

    for line in lines[next_player:]:
        if line.strip():
            player_2.append(int(line))




def play_the_game(player_1,player_2):
    """ Playes the game to completion"""
    rounds = 0
    while player_1 and player_2:
        rounds += 1

        card_1 = player_1.pop(0)
        card_2 = player_2.pop(0)

        if card_1 > card_2:
            player_1.append(card_1)
            player_1.append(card_2)
        else:
            player_2.append(card_2)
            player_2.append(card_1)

    return rounds




def main():
    """Start"""
    #get argument
    if len(sys.argv) < 1:
        sys.exit("Usage: python " + sys.argv[0] + " filename")
    filename = sys.argv[1]
    try:
        with open(filename, 'rt', encoding="utf-8") as file:
            lines = file.readlines()
    except IOError as err:
        print(f"{err}\nError opening {filename}. Terminating program.", file=sys.stderr)
        sys.exit(1)

    player_1 = []
    player_2 = []

    create_decks(lines,player_1,player_2)
    _ = play_the_game(player_1,player_2)

    winner = player_1
    if player_2:
        winner = player_2

    score = sum([ x*y for x,y in zip(winner,range(len(winner),0,-1))])
    print(score)

if __name__ == "__main__":
    main()
