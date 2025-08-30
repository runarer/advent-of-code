"""Advent of Code: 2020.1.1"""
from math import sqrt
import sys

def create_image_grid(image_parts):
    """ Some """
    image         = [[]]
    image_dim     = int( sqrt( len(image_parts) ) )
    image_borders = { k: get_border(v) for k,v in image_parts.items() }
    image_overlap = {k: { k2:matching_borders(v,v2) for k2,v2 in image_borders.items() if k != k2} \
                                                    for k, v  in image_borders.items()           }
    shared_borders= {k: {k2:v2[1] for k2,v2 in v.items() if v2[0]} for k,v in image_overlap.items()}
    corners       = [k for k,v in shared_borders.items() if len(v) == 2 ]
    sides         = [k for k,v in shared_borders.items() if len(v) == 3 ]
    unplaced_neighbours = { k: list(v.keys()) for k,v in shared_borders.items()}

    # for k,v in unplaced_neighbours.items():
    #     print(k,v)

    cur = 0     # The current part we are working with
    prev = 0    # The previous part that was placed on line

    # Create first line of image
    # Corner
    cur = corners[0]
    image[0].append(cur)
    prev = cur # Needed?

    # First of side
    cur = unplaced_neighbours[prev].pop(0)
    image[0].append(cur)
    #sides.remove(cur)
    unplaced_neighbours[cur].remove(prev)
    prev = cur

    # Rest of side and corner
    for _ in range(2,image_dim):
        # Find cur from sides and unplaced_neighbours
        for part in unplaced_neighbours[prev]:
            if part in sides:
                cur = part
                break
            if part in corners:
                cur = part
                break

        image[0].append(cur)
        #sides.remove(cur) # unødvendig? siden man fjerner cur i
        unplaced_neighbours[prev].remove(cur)
        unplaced_neighbours[cur ].remove(prev)

        prev = cur

    # print("\t",image)
    # for i in image[0]:
    #     print(i,unplaced_neighbours[i])

    # Lines
    # Trenger kanskje ikke remove from above siden jeg er ferdig med above
    for i in range(1,image_dim):
        # First, no prev
        above = image[i-1][0]
        cur = unplaced_neighbours[above].pop(0)
        image.append([cur])
        #print("\n",cur,above,unplaced_neighbours[cur])
        unplaced_neighbours[cur].remove(above)
        #unplaced_neighbours[cur].remove(prev)
        #unplaced_neighbours[prev].remove(cur)
        prev = cur

        # Center-parts
        for j in range(1,image_dim-1):
            above = image[i-1][j]
            cur = unplaced_neighbours[above].pop(0)
            image[i].append(cur)
            unplaced_neighbours[cur].remove(above)
            unplaced_neighbours[cur].remove(prev)
            unplaced_neighbours[prev].remove(cur)
            prev = cur

        # Last
        above = image[i-1][-1]
        cur = unplaced_neighbours[above].pop(0)
        image[i].append(cur)
        unplaced_neighbours[cur].remove(above)
        #print(cur,unplaced_neighbours[cur])
        unplaced_neighbours[cur].remove(prev)
        unplaced_neighbours[prev].remove(cur)
        prev = cur # needed?

    return image

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

def line_up_image(image,target_line,target_side):
    """Lines up an image"""
    borders = get_border(image)
    pos = 0
    if target_line in borders:
        pos = borders.index(target_line)
    else:
        borders = [border[::-1] for border in borders]
        pos = borders.index(target_line)

    #Rotate into position
    while pos != target_side:
        pos = (pos+1) % 4
        image = rotate_image(image)

    borders = get_border(image)
    if borders[pos] != target_line:
        #Need to flip
        if pos == 1 or pos == 3:
            image = flip_image_horz(image)
        else:
            image = flip_image_vert(image)

    return image

def recreate_image(image_parts):
    """ Create an image based on parts. """
    image_dim     = int( sqrt( len(image_parts) ) )
    image         = [ [] for _ in range(image_dim) ]
    image_borders = { k: get_border(v) for k,v in image_parts.items() }
    image_overlap = {k: { k2:matching_borders(v,v2) for k2,v2 in image_borders.items() if k != k2} \
                                                    for k, v  in image_borders.items()           }
    shared_borders= {k: {k2:v2[1] for k2,v2 in v.items() if v2[0]} for k,v in image_overlap.items()}
    corner_ids    = [k for k,v in shared_borders.items() if len(v) == 2 ]
    side_ids    = [k for k,v in shared_borders.items() if len(v) == 3 ]
    center_ids    = [k for k,v in shared_borders.items() if len(v) == 4 ]

    # Build Image
    # 1. Place parts in 2d list in its right position.
    image[0].append(corner_ids[0])
    last_part = corner_ids[0]
    corner_ids.remove(last_part)

    last_part_pos = [v[0] for k,v in shared_borders[last_part].items() ]
    last_part_nbr = list(shared_borders[last_part].keys())

    next_part = last_part_nbr[0]
    next_line = last_part_nbr[1]
    image[0].append(last_part_nbr[0])
    side_ids.remove(next_part)

    # Top side
    last_line = [last_part,next_part]
    last_part = next_part    
    for _ in range(2,image_dim):
        for part in shared_borders[last_part].keys():
            if part in side_ids:
                next_part = part
                side_ids.remove(part)
                image[0].append(part)
                last_line.append(part)
                break
            if part in corner_ids:
                next_part = part
                corner_ids.remove(part)
                image[0].append(part)
                last_line.append(part)
                break
        last_part = next_part

    #print(last_line)
    #Corner, kan inkluderer i Top side
    # for part in shared_borders[last_part].keys():
    #     if part in corner_ids:
    #         next_part = part
    #         corner_ids.remove(part)
    #         image[0].append(part)
    #         break
    # last_part = next_part

    #


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

    return image
    

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
    image = create_image_grid(image_parts)
    # for k,v in image.items():
    #     print(k,v)
    for n in range(len(image)):
        for m in range(10):
            line = " "
            for j in range(len(image[0])):
                line += image_parts[ image[n][j] ][m]
                line += " "
            print(line)
        print(" ")



    # new_image = line_up_image(image_parts["1951"],"#...##.#..",3)
    # print("\n")
    # for line in new_image:
    #     print(line)

    # Find seamonster


if __name__ == "__main__":
    main()
