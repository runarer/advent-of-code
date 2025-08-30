"""Dette skulle vært løst med binærtre isteden for dette tullet."""
import sys, math, re

def explode(snailfish_number: str) -> str:
    """
    Explode return a new snailfish number with the left most 5-level pair number
    exploded. If no number explode, the input number returns unchanged
    """
    def insert_left(number: str, left_string: str) -> str:
        #regex (whatever)(number)(whaterver, no numbers) search from right
        #(.+)(\d+)(\D+)
        #results = re.split(r"(.+)(\d+)(\D+)",left_string,maxsplit=1)
        rev_string = left_string[::-1]
        results = re.split(r"(\d+)",rev_string,maxsplit=1)
        if results[0] != rev_string:
            new_number = str(int(number) + int(results[1][::-1]))
            return results[2][::-1] + new_number + results[0][::-1]
        return left_string

    def insert_right(number: int, right_string: str) -> str:
        #regex (whatever, no numbers)(number)(whatever) search from left
        #(\D+)(\d+)(.+)    
        results = re.split(r"(\d+)",right_string,maxsplit=1)
        if results[0] != right_string:
            new_number = str(int(results[1])+int(number))
            return results[0] + new_number + results[2]
        return right_string

    bracket_level = 0
    index = 0
    for char in snailfish_number:
        if bracket_level == 5:
            #We have an explosion
            l_bracket = index
            r_bracket = snailfish_number.index(']',index)
            #print(snailfish_number[l_bracket:r_bracket])
            l_number, r_number = snailfish_number[l_bracket:r_bracket].split(',')
            #print("FISH L:",snailfish_number[:l_bracket-1])
            #print("FISH R:",snailfish_number[r_bracket+1:])
            return insert_left(l_number,snailfish_number[:l_bracket-1]) + '0' + \
                   insert_right(r_number,snailfish_number[r_bracket+1:])
        if char == '[':
            bracket_level += 1
        elif char == ']':
            bracket_level -= 1
        index += 1

    #Find left most 5-level pair
    return snailfish_number

def split(snailfish_number: str) -> str:
    """Split the left most number higher than 9."""
    def split_number(to_split) -> str:
        number = int(to_split)/2
        l_number = str(math.floor(number))
        r_number = str(math.ceil(number))
        return "[" + l_number + "," + r_number +"]"

    #regex: (whatever)(more than one digit)(whatever) not global or multiline
    #split with \d\d+ ? hva gir det i retur
    results = re.split(r"(\d\d+)",snailfish_number,maxsplit=1)
    if results[0] != snailfish_number:
        return results[0] + split_number(results[1]) + results[2]
    return snailfish_number

def reduce(snailfish_number: str) -> str:
    has_exploded = True
    has_split    = True

    while has_exploded or has_split:
        #print(snailfish_number)
        new_number = explode(snailfish_number)
        if new_number != snailfish_number:
            has_exploded = True
            snailfish_number = new_number
            continue
        has_exploded = False

        new_number = split(snailfish_number)
        if new_number != snailfish_number:
            has_split = True
            snailfish_number = new_number
            continue
        has_split = False

    return snailfish_number

def add_snailnumbers(first_snailnumber: str, second_snailnumber: str) -> str:
    new_number = "[" + first_snailnumber + "," + second_snailnumber + "]"
    #print("A: ", new_number)
    return reduce(new_number)

def magnitude(snailfish_number: str) -> int:
    while True:
        results = re.split(r"(\[(\d+),(\d+)\])",snailfish_number,maxsplit=1)
        if results[0] == snailfish_number:
            break
        magn = str((int(results[2])*3) + (int(results[3])*2))
        snailfish_number = results[0] + magn + results[4]
    return snailfish_number

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

    numbers = [ line.strip() for line in lines]

    snailfish_sum = numbers[0]
    for number in numbers[1:]:
        print(" ",snailfish_sum)
        print("+",number)
        snailfish_sum = add_snailnumbers(snailfish_sum,number)
        print("=",snailfish_sum)
        print("----------------------------------------------------------")

    print("\nSum", snailfish_sum)
    magnit = magnitude(snailfish_sum)
    print("Magnitude: ",magnit)

if __name__ == "__main__":
    main()
