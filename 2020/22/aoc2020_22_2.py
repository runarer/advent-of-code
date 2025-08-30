"""Advent of Code: 2020.22.2"""
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




def play(player1,player2):
    """ Plays the game with the players decks and return the winner. """
    round_winner = 1
    prev_rounds1 = set()
    prev_rounds2 = set()

    while player1 and player2:
        # Check previous rounds
        deck1 = tuple(player1)
        deck2 = tuple(player2)

        if deck1 in prev_rounds1 or deck2 in prev_rounds2:
            return 1

        prev_rounds1.add(deck1)
        prev_rounds2.add(deck2)

        # Play this round
        card1 = player1.pop(0)
        card2 = player2.pop(0)

        if len(player1) >= card1 and len(player2) >= card2:
            round_winner = play(player1[:card1],player2[:card2])
        else:
            if card1 > card2:
                round_winner = 1
            else:
                round_winner = 2

        if round_winner == 1:
            player1.append(card1)
            player1.append(card2)
        else:
            player2.append(card2)
            player2.append(card1)

    return round_winner # however won the last round.




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
    winner = play(player_1,player_2)

    if winner == 1:
        winner = player_1
    else:
        winner = player_2

    score = sum([ x*y for x,y in zip(winner,range(len(winner),0,-1))])
    print(score)

if __name__ == "__main__":
    main()
