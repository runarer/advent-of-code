"""Naive approac"""
import sys

def expand_picture(old_picure,char):
    new_picture = ["".join([char for _ in range(len(old_picure)+2)])]
    for line in old_picure:
        new_picture.append(char + line + char)
    new_picture.append("".join([char for _ in range(len(old_picure)+2)]))
    
    return new_picture


def enhance_picture(old_picture,code):
    new_picture = []
    
    end = len(old_picture)-1
    for line in range(1,end):
        new_line = ""
        for row in range(1,end):
            #turn 3x3 to value
            value = int(old_picture[line-1][row-1:row+2] + old_picture[line][row-1:row+2] + old_picture[line+1][row-1:row+2],2)
            new_line += code[value]
        new_picture.append(new_line)

    return new_picture

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

    #line 0: code
    code = ['0' if char == '.' else '1' for char in lines[0].strip()]
    #line 1 skip

    #line 2 to next to last
    picture = []
    for line in lines[2:]:
        new_line = "".join(['0' if char == '.' else '1' for char in line.strip()])
        picture.append(new_line)

    for i in range(50):
        if i % 2:
            picture = expand_picture(picture,code[0])
            picture = expand_picture(picture,code[0])
        else:
            picture = expand_picture(picture,code[511])
            picture = expand_picture(picture,code[511])
        picture = enhance_picture(picture,code)

    value = sum([x.count('1') for x in picture])
    print(value)


if __name__ == "__main__":
    main()
