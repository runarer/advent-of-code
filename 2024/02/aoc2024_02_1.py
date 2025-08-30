"""Advent of Code: 2024.2.1"""
import sys

def safe(numbers):
    if not all( abs(numbers[i] - numbers[i+1]) <= 3 and numbers[i] != numbers[i+1] for i in range(len(numbers) - 1) ):
        return False
    if all( numbers[i] < numbers[i+1] for i in range(len(numbers) - 1)):
        return True
    if all( numbers[i] > numbers[i+1] for i in range(len(numbers) - 1)):
        return True
    return False

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
    number_list = [[ int(number) for number in numbers.split()] for numbers in lines]
    print(sum( safe(numbers) for numbers in number_list ))


if __name__ == "__main__":
    main()
