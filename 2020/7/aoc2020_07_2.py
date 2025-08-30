"""Advent of Code: 2020.7.2"""
import sys

class Bag:
    """ Bag """
    def __init__(self, rule):
        """ Takes a rule and create a bag based on that."""
        self.color, contains = rule.strip().strip('.').split(" bags contain ")
        self.contains = {}
        if "no other bags" not in contains:
            # Get each individual rule
            contain_rules = contains.split(", ")

            # Parse each rule
            for contain_rule in contain_rules:
                number, color1, color2, _ = contain_rule.split()
                color = color1 + " " + color2
                self.contains[color] = int(number)

    def can_contain(self, bag_color):
        """ Check if this bag can contain a bag of a color"""
        if bag_color in self.contains:
            return self.contains[bag_color]
        return 0

    def __str__(self):
        if self.contains:
            return f"{self.color} Contains {self.contains}"
        return f"{self.color} Contains nothing."

def contain_bags(bags, bag):
    """ Recursive function for calculating how many bags are within a bag."""
    if not bags[bag].contains:
        return 0
    number_of_bags = 0
    for ib_color,ib_nr in bags[bag].contains.items():
        number_of_bags += ib_nr + (ib_nr * contain_bags(bags, ib_color))
    return number_of_bags


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

    # Create bags
    bags = [ Bag(line) for line in lines]
    bags = { bag.color:bag for bag in bags}
    number_of_bags = contain_bags(bags,"shiny gold")
    print(number_of_bags)

if __name__ == "__main__":
    main()
