"""
    Etter at player 1 har kastet terningen 3 gangner så finnes det 27 universer hvor de har fått
    poeng. Flere av disse universerne har samme poengsum og kan behandles likt i fortsettelsen.
    Trenger kun vite antallet av hver per sum.

        Bruk en dict for poeng:univers oversikt. En per player. {(poeng,universes)}

    Player 2 har nå 0 poeng i 27 ulike univers. Etter et kast er det 27*3=81 univers hvor
    player 2 har poeng. Så 243 og til slutt 729.

        Totalt antall univers etter n kanst er 3^n [3,9,27,81,243,729,...]

    Player 2 har 27 universer med laveste kast (1,1,1) og 27 univers med høyeste kast (3,3,3)
    og 27 med midterste kast (2,2,2).
    Player 1 har også 27 universer med laveste kast, høyeste kast og midterste kast.
    Så vi må gange hvert univers i player 1 poengoversikt med 27.


    DEBUG:
    Har ikke tatt hensyn til at begge spillere må kjenne til hverandres spill. Må fjerne spillene
    der en vinner fra den andres runder.

    games = {(player1_score,player1_pos,player2_score,player2_pos):universes}
"""

class Game():
    def __init__(self,player_1_start,player_2_start) -> None:
        self.board = [x+1 for x in range(10)]
        self.player_1_wins = 0
        self.player_2_wins = 0
        self.universes = {((0,player_1_start-1),(0,player_2_start-1)):1}

    def player_1_rounds(self):
        def add_universes(score,pos,player_2,uni,steps):
            new_score = score + self.board[ (pos+steps) % 10]
            new_pos = (pos+steps) % 10

            if ((new_score,new_pos),player_2) in new_universes:
                new_universes[((new_score,new_pos),player_2)] += uni
            else:
                new_universes[((new_score,new_pos),player_2)] = uni

        new_universes = {}
        
        # Calculate new universes
        for ((score,pos),player_2), uni in self.universes.items():
            add_universes(score,pos,player_2,uni,3)
            add_universes(score,pos,player_2,uni*3,4)
            add_universes(score,pos,player_2,uni*6,5)
            add_universes(score,pos,player_2,uni*7,6)
            add_universes(score,pos,player_2,uni*6,7)
            add_universes(score,pos,player_2,uni*3,8)
            add_universes(score,pos,player_2,uni,9)

        # Look for victories
        final_universes = {}
        for ((score,pos),player_2), uni in new_universes.items():
            if score >= 21:
                self.player_1_wins += uni
            else:
                final_universes[((score,pos),player_2)] = uni
        
        self.universes = final_universes

    def player_2_rounds(self):
        def add_universes(score,pos,player_1,uni,steps):
            new_score = score + self.board[ (pos+steps) % 10]
            new_pos = (pos+steps) % 10

            if (player_1,(new_score,new_pos)) in new_universes:
                new_universes[(player_1,(new_score,new_pos))] += uni
            else:
                new_universes[(player_1,(new_score,new_pos))] = uni

        new_universes = {}
        
        # Calculate new universes
        for (player_1,(score,pos)), uni in self.universes.items():
            add_universes(score,pos,player_1,uni,3)
            add_universes(score,pos,player_1,uni*3,4)
            add_universes(score,pos,player_1,uni*6,5)
            add_universes(score,pos,player_1,uni*7,6)
            add_universes(score,pos,player_1,uni*6,7)
            add_universes(score,pos,player_1,uni*3,8)
            add_universes(score,pos,player_1,uni,9)

        # Look for victories
        final_universes = {}
        for (player_1,(score,pos)), uni in new_universes.items():
            if score >= 21:
                self.player_2_wins += uni
            else:
                final_universes[(player_1,(score,pos))] = uni
        
        self.universes = final_universes

def main():
    games = Game(8,6)

    while True:
        # Player 1 plays a round with 3 throws
        games.player_1_rounds()
        if not games.universes:
            break
        games.player_2_rounds()
        if not games.universes:
            break

    max_wins = max(games.player_1_wins,games.player_2_wins)
    print(max_wins)

if __name__ == "__main__":
    main()
