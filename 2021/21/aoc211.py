#make a class for die. How do I make classes in python -> write a markup doc.

# The die class takes a optional min and max value, default 1 and 100
# die.roll(number_of_rolls=1) returns the sum of a given number of rolls.

class Die:
    def __init__(self,minimum=1,maximum=100) -> None:
        self.minimum = minimum
        self.maximum = maximum
        self.last_roll = 0
    
    def roll(self) -> int:
        if self.last_roll == self.maximum:
            self.last_roll = self.minimum
        else:
            self.last_roll += 1
        return self.last_roll


    def rolls(self,nr_of_rolls:int):
        if nr_of_rolls <= 0:
            return 0
        return sum([self.roll() for _ in range(nr_of_rolls)])

class Player():
    def __init__(self,start) -> None:
        #self.board = [x-10 if x > 10 else x for x in range(start, start+10)]
        self.board = [x+1 for x in range(10)]
        self.score = 0
        self.pawn_at = start-1

    def move(self,moves:int) -> int:
        self.pawn_at = (self.pawn_at + moves) % 10
        self.score += self.board[ self.pawn_at ]
        return self.score

def main():
    die = Die()
    player1 = Player(8)
    player2 = Player(6)

    rolls = 0
    while True:
        score = player1.move(die.rolls(3))
        rolls += 3
        if score >= 1000:
            break
        print("Player 1: ",score)
        score = player2.move(die.rolls(3)) #endre til liste med players
        rolls += 3
        if score >= 1000:
            break
        print("Player 2: ",score)

    loser_and_round = min(player1.score,player2.score)*rolls
    print(player1.board)
    print(player2.board)
    print(rolls)
    print(loser_and_round)

if __name__ == "__main__":
    main()
