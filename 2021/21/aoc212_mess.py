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

class Player():
    def __init__(self,start) -> None:
        self.board = [x+1 for x in range(10)]
        self.wins = 0
        self.universes = {(0,start-1):1}

    def play_3_round(self):
        def add_universes(score,pos,uni,steps):
            new_score = score + self.board[ (pos+steps) % 10]
            new_pos = (pos+steps) % 10

            if (new_score,new_pos) in new_universes.keys():
                new_universes[(new_score,new_pos)] += uni
            else:
                new_universes[(new_score,new_pos)] = uni

        new_universes = {}
        
        # Calculate new universes

        for (score,pos), uni in self.universes.items():
            #### PROBLEM: hvis (score, pos) eksisterer så skal den oppdateres og ikke overskrives
            add_universes(score,pos,uni,3)
            add_universes(score,pos,uni*3,4)
            add_universes(score,pos,uni*6,5)
            add_universes(score,pos,uni*7,6)
            add_universes(score,pos,uni*6,7)
            add_universes(score,pos,uni*3,8)
            add_universes(score,pos,uni,9)
            
            # 3 steps
            # new_universes[(score+get_score(pos,3),get_pos(pos,3))] = uni
            # # 4 steps
            # new_universes[(score+get_score(pos,3),get_pos(pos,4))] = uni*3
            # # 5 steps
            # new_universes[(score+get_score(pos,3),get_pos(pos,5))] = uni*6
            # # 6 steps
            # new_universes[(score+get_score(pos,3),get_pos(pos,6))] = uni*7
            # # 7 steps
            # new_universes[(score+get_score(pos,7),get_pos(pos,7))] = uni*6
            # # 8 steps
            # new_universes[(score+get_score(pos,8),get_pos(pos,8))] = uni*3
            # # 9 steps
            # new_universes[(score+get_score(pos,9),get_pos(pos,9))] = uni

        # Look for victories
        final_universes = {}
        for (score,pos), uni in new_universes.items():
            if score >= 21:
                self.wins += uni
            else:
                final_universes[(score,pos)] = uni
        
        self.universes = final_universes

    def wait_for_other_player(self):
        new_universes = {}
        
        # Update universes
        for (score,pos), uni in self.universes.items():
            new_universes[(score,pos)] = uni*27
        
        self.universes = new_universes

def main():
    # # Oppgave:
    # player1 = Player(8)
    # player2 = Player(6)

    # Test case
    player1 = Player(4)
    player2 = Player(8)

    while True:
        player1.play_3_round()
        player2.wait_for_other_player()
        if not player1.universes:
            break
        print("Player 1:",player1.wins)
        #print("Player 1:",player1.universes)
        summ = sum(player1.universes.values())
        print(summ)

        player2.play_3_round()
        player1.wait_for_other_player()
        if not player2.universes:
            break
        print("Player 2:",player2.wins)
        #print("Player 2:",player2.universes)
        summ = sum(player2.universes.values())
        print(summ)


    max_victories = max(player1.wins,player2.wins)
    print("Player 1:",player1.wins)
    print("Player 2:",player2.wins)
    print(max_victories)

if __name__ == "__main__":
    main()
