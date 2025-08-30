"""Advent of Code: 2020.21.1"""
import sys

def find_name_of_allergens(products,allergens):
    """ dd """
    allergen_can_be = {k: set() for k in allergens}
    for prod in products:
        for allg in prod["allergens"]:
            if allergen_can_be[allg]:
                allergen_can_be[allg].intersection_update(prod["ingredients"])
            else:
                allergen_can_be[allg].update(prod["ingredients"])

    unknown_english = {}
    while allergen_can_be:
        # Find first with only one
        only_one = ""
        for alle, ingr in allergen_can_be.items():
            # Remove it from untranslated, place it in dictonary
            if len(ingr) == 1:
                only_one = list(ingr)[0]
                unknown_english[only_one] = alle
                del allergen_can_be[alle]
                break

        # Remove translated from untranslateds list.
        for alle, ingr in allergen_can_be.items():
            if only_one in ingr:
                ingr.remove(only_one)

    return unknown_english

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

    # Setting up basic data structures
    products = []
    ingredients = set()
    allergens = set()

    for line in lines:
        prod = line.split(" (contains ")
        ingr = prod[0].split()
        alle = prod[1].strip().strip( ')' ).split(", ")

        products.append({"ingredients":ingr,"allergens":alle})

        ingredients.update(ingr)
        allergens.update(alle)

    unknown_english = find_name_of_allergens(products,allergens)
    allergy_free_ingredients = ingredients - set(list(unknown_english.keys()))

    number_of_ingredients = 0
    for prod in products:
        for ingr in prod["ingredients"]:
            if ingr in allergy_free_ingredients:
                number_of_ingredients += 1

    print(number_of_ingredients)


if __name__ == "__main__":
    main()
