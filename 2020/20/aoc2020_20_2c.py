"""Advent of Code: 2020.1.1"""
from math import sqrt
import sys

class ImagePart:
    """ Class for an image part"""

    def __init__(self,image,image_id):
        """ image is the partial image"""
        self.image_id = image_id
        self.image = image
        self.top : ImagePart = None
        self.right : ImagePart = None
        self.bottom : ImagePart = None
        self.left : ImagePart = None

    def rotate(self):
        """ Rotates an image 90 degree clockwise. """
        temp_part = self.top
        self.top = self.left
        self.left = self.bottom
        self.bottom = self.right
        self.right = temp_part

        new_image = list(self.image[0])

        for line in self.image[1:]:
            for j,point in enumerate(line):
                new_image[j] = point + new_image[j]

        self.image = new_image

    def flip_horz(self):
        """Flips the image horizontally"""
        temp_part = self.top
        self.top = self.bottom
        self.bottom = temp_part
        
        self.image = self.image[::-1]

    def flip_vert(self):
        """Flipes the image vertically"""
        temp_part = self.left
        self.left = self.right
        self.right = temp_part

        self.image = [line[::-1] for line in self.image]

    def remove_border(self):
        """ Removes the border from an image. """
        self.image = [ img[1:-1] for img in self.image[1:-1] ]

    def set_border(self,borders):
        """Sets the border based on a list"""
        self.top = borders[0]
        self.right = borders[1]
        self.bottom = borders[2]
        self.left = borders[3]

    def __str__(self):
        return f"Top:{self.top}  Right:{self.right}  Bottom:{self.bottom}  Left:{self.left}"


def matching_borders(borders_1,borders_2):
    """ Try to line up borders. """
    # For each border in borders_1
    # compare it to each border and its reversed in borders_2
    for i,border_1 in enumerate(borders_1):
        for j,border_2 in enumerate(borders_2):
            if border_1 == border_2:
                return True,(i,j)
            if border_1 == border_2[::-1]:
                return True,(i,-1*j)

    return False,(0,0)

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

def recreate_image(image_parts):
    """ Create an image based on parts. """
    image_prts = { k:ImagePart(v,k) for k,v in image_parts.items() }
    image_dim     = int( sqrt( len(image_parts) ) )
    image         = [ [] for _ in range(image_dim) ]
    image_borders = { k: get_border(v) for k,v in image_parts.items() }
    image_overlap = {k: { k2:matching_borders(v,v2) for k2,v2 in image_borders.items() if k != k2} \
                                                    for k, v  in image_borders.items()           }
    shared_borders= {k: {k2:v2[1] for k2,v2 in v.items() if v2[0]} for k,v in image_overlap.items()}
    for image_id, borders in shared_borders.items():
        for image_nbr_id, border in borders.items():
            if border[0] == 0:
                image_prts[image_id].top = image_nbr_id
                continue
            if border[0] == 1:
                image_prts[image_id].right = image_nbr_id
                continue
            if border[0] == 2:
                image_prts[image_id].bottom = image_nbr_id
                continue
            if border[0] == 3:
                image_prts[image_id].left = image_nbr_id
                continue

    for k,v in image_prts.items():
        print(k,v)

    corner_ids    = [k for k,v in shared_borders.items() if len(v) == 2 ]
    side_ids    = [k for k,v in shared_borders.items() if len(v) == 3 ]
    center_ids    = [k for k,v in shared_borders.items() if len(v) == 4 ]

    # Build Image
    # 1. Place parts in 2d list in its right position.
    image[0].append(corner_ids[0])
    last_part = corner_ids[0]
    last_part_pos = [v[0] for k,v in shared_borders[last_part].items() ]
    last_part_nbr = list(shared_borders[last_part].keys())

    next_part = last_part_nbr[0]
    image[0].append(last_part_nbr[0])
    side_ids.remove(next_part)

    last_part = next_part
    for _ in range(2,image_dim-1):
        for part in shared_borders[last_part].keys():
            if part in side_ids:
                next_part = part
                side_ids.remove(part)
                image[0].append(part)
                break
        last_part = next_part
       

    # get position from shared_borders

    # Build side


    #Rotate to right position [1,2]

    # for i in range(1,image_dim-1):
    #     next_part = 
    #     image[0].append(next_part)

    # 2. Rotate and/or flip the image - TEST rotate.
    # 3. Purge borders.
    # 4. Merge images.
    #   Start with a corner
    #   Move down and append strings.
    #   Move right and add to the strings    

    return shared_borders

def rotate_image(image):
    """ Rotates an image 90 degree clockwise. """
    new_image = [ point for point in image[0] ]

    for line in image[1:]:
        for j,point in enumerate(line):
            new_image[j] = point + new_image[j]

    return new_image

def flip_image_horz(image):
    """ Flips an image. """
    return image[::-1]

def flip_image_vert(image):
    """ Flips an image. """
    return [line[::-1] for line in image]

def strip_border(image):
    """ Removes the border from an image. """
    return [ img[1:-1] for img in image[1:-1] ]

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

    # Create image
    image = recreate_image(image_parts)
    for k,v in image.items():
        print(k,v)
    # print(image)


    # Find seamonster


if __name__ == "__main__":
    main()
