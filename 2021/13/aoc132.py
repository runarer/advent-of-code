import sys
from operator import add

def fill_out_paper(dot_list):
    size_x = 0
    size_y = 0
    for x,y in dot_list:
        if x > size_x:
            size_x = x
        if y > size_y:
            size_y = y
    paper = [[0 for _ in range(size_x+1)] for _ in range(size_y+1)]
    for x,y in dot_list:
        paper[y][x] = 1
    return paper

def fold_paper(paper, folds):
    folded_paper = paper
    for fold in folds:
        if fold[0] == 'y':
            first_half  = folded_paper[0:fold[1]]
            second_half = folded_paper[fold[1]+1:]
            second_half.reverse()
            folded_paper = [list(map(add, first_half[i], second_half[i])) for i in range(len(first_half))]
        else:
            first_half  = [folded_paper[i][0:fold[1] ] for i in range(len(folded_paper))]
            second_half = [folded_paper[i][fold[1]+1:] for i in range(len(folded_paper))]
            for line in second_half:
                line.reverse()
            folded_paper = [list(map(add, first_half[i], second_half[i])) for i in range(len(first_half))]

    return folded_paper



def main():
    """Start"""
    #get argument
    if len(sys.argv) < 1:
        sys.exit("Usage: python " + sys.argv[0] + " filename")
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except IOError as err:
        print("{}\nError opening {}. Terminating program.".format(err, filename), file=sys.stderr)
        sys.exit(1)

    dots = []
    folds = []

    for line in lines:
        if line == '\n': continue
        if "fold" in line:
            folds.append([line[11],int(line[13:].strip())])
            continue
        x, y = line.strip().split(',')
        dots.append([int(x),int(y)])
    paper = fill_out_paper(dots)
    # for p in paper:
    #     print(p)
    folded_paper = fold_paper(paper, folds)
    print("fold:")
    for p in folded_paper:
        line = ""
        for i in p:
            if i > 0: line += '#'
            else: line += '.'
        print(line)


if __name__ == "__main__":
    main()
