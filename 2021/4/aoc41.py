"""AoC day 4, part 1, play bingo"""

import sys

def check_boards(boards):
    """Check the board for winning stuff."""
    for board in range(int(len(boards)/25)):
        #Check colums
        for row in range(board*25,5+board*25):
            if boards[row] != 'M':
                continue
            #check colum
            for i in range(row+5,row+25,5):
                if boards[i] != 'M':
                    break
            else:
                return board
        #Check rows
        for colum in range(board*25,25+board*25,5):
            if boards[colum] != 'M':
                continue
            #check row
            for i in range(colum+1,colum+5):
                if boards[i] != 'M':
                    break
            else:
                return board
    return -1

def find_first_winner(boards, numbers):
    """Playes the game"""
    #play first four, no victory
    boards = ['M' if x in numbers[:4] else x for x in boards]
    for draw in numbers[4:]:
        boards = ['M' if x == draw else x for x in boards]
        winning_board = check_boards(boards)
        if winning_board != -1:
            return (boards[winning_board*25:winning_board*25+25],draw)
    return -1

def caluculate_score(board, draw):
    """Calculate final score."""
    score = 0
    for num in board:
        if num != 'M':
            score += int(num)
    return int(draw)*score

def main():
    """Start"""
    #get argument
    if len(sys.argv) < 1:
        sys.exit("Usage: python " + sys.argv[0] + " filename")
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as file:
            numbers = file.readline().strip().split(',')
            boards = file.read().split()
    except IOError as err:
        print("{}\nError opening {}. Terminating program.".format(err, filename), file=sys.stderr)
        sys.exit(1)
    board, draw = find_first_winner(boards, numbers)    
    print("Final score is: ",caluculate_score(board, draw))

if __name__ == "__main__":
    main()
