"""Advent of Code: 2020.1.1"""
from math import sqrt
import math
import sys

def matching_borders(borders_1,borders_2):
    """ Try to line up borders. """
    match = 0

    # For each border in borders_1
    # compare it to each border and its reversed in borders_2
    for border_1 in borders_1:
        for border_2 in borders_2:
            if border_1 == border_2:
                match += 1
                continue
            if border_1 == border_2[::-1]:
                match += 1

    # There should only be one match.
    return match > 0

def get_border(image):
    """ Return four string of the border of the image. 
        Top and bottom is from left to right.
        Left and right is from top to bottom."""
    top     = image[0]
    bottom  = image[-1]

    left    = ""
    right   = ""
    for line in image:
        left += line[0]
        right += line[-1]

    return [top,right,bottom,left]

def extract_image_parts(lines):
    """ Get the image parts from file"""
    image_parts = {}

    line_nr = 0
    end_of_file = len(lines)
    while line_nr < end_of_file:
        image_id = lines[line_nr].split()[1].split(':')[0]
        line_nr += 1

        image_parts[image_id] = [line.strip() for line in lines[line_nr:line_nr+10]]
        line_nr += 11

    return image_parts

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

    image_parts = extract_image_parts(lines)
    image_dim = int( sqrt( len(image_parts) ) )
    image_borders = { k: get_border(v) for k,v in image_parts.items() }
    # for k,v in image_borders.items():
    #     print(k,v)

    image_overlap = {k: { k2:matching_borders(v,v2) for k2,v2 in image_borders.items() if k != k2} for k,v in image_borders.items()}
    # for k,v in image_overlap.items():
    #     print(k,v)

    # Find borders
    border_ids = [int(k) for k,v in image_overlap.items() if sum(v.values()) == 2 ]

    print( math.prod(border_ids) )

    if (1,2) == (1,2):
        print("Tree")
    else:
        print("obs")


if __name__ == "__main__":
    main()
