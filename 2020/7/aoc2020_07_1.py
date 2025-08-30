"""Advent of Code: 2020.7.1"""
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
                self.contains[color] = number

    def can_contain(self, bag_color):
        """ Check if this bag can contain a bag of a color"""
        if bag_color in self.contains:
            return self.contains[bag_color]
        return 0

    def __str__(self):
        if self.contains:
            return f"{self.color} Contains {self.contains}"
        return f"{self.color} Contains nothing."

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

    # Search for possible outer layers
    # Queue, pop, count it, search for containers.
    queue = ["shiny gold"]
    number_of_containers = set()
    while queue:
        place_bag = queue.pop()
        number_of_containers.add(place_bag)
        for bag in bags:
            if bag.can_contain(place_bag):
                queue.append(bag.color)
    print(len(number_of_containers)-1)


if __name__ == "__main__":
    main()
