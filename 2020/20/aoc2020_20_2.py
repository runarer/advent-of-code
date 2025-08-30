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
        unplaced_neighbours[prev].remove(cur)
        unplaced_neighbours[cur ].remove(prev)

        prev = cur

    # Lines
    for i in range(1,image_dim):
        # First, no prev
        above = image[i-1][0]
        cur = unplaced_neighbours[above].pop(0)
        image.append([cur])
        unplaced_neighbours[cur].remove(above)
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
        unplaced_neighbours[cur].remove(prev)
        unplaced_neighbours[prev].remove(cur)
        prev = cur # needed?

    return image

def align_image_parts(image):
    """Somee"""
    def find_matching_border(image_part1,image_part2):
        borders_1 = get_border(image_part1)
        borders_2 = get_border(image_part2)

        for i,border_1 in enumerate(borders_1):
            for border_2 in borders_2:
                if border_1 == border_2:
                    return i
                if border_1 == border_2[::-1]:
                    return i
        return 0

    # Align corner
    # Find n and m
    n = find_matching_border(image[0][0],image[0][1])
    m = find_matching_border(image[0][0],image[1][0])

    new_image = image[0][0]
    # Do we need to flip
    if (n,m) in [(1,0),(2,1),(3,2),(0,3)]:
        new_image = flip_image_horz(new_image)
        if (n,m) == (1,0):
            m = 2
        elif (n,m) == (2,1):
            n = 0
        elif (n,m) == (3,2):
            m = 0
        else:
            n = 2
    # Rotate
    while n != 1 and m != 2:
        n = (n+1) % 4
        m = (m+1) % 4
        new_image = rotate_image(new_image)
    image[0][0] = new_image

    # Align top row
    for j in range(1,len(image[0])):
        border = "".join( [line[-1] for line in image[0][j-1]] )
        image[0][j] = line_up_image(image[0][j],border,3)

    # Align each line.
    for i in range(1,len(image)):
        for j,img in enumerate(image[i]):
            border = image[i-1][j][-1]
            image[i][j] = line_up_image(img,border,0)

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

def cleanup_image(image):
    """ Removes borders and assemble image"""
    new_image = []

    for n,_ in enumerate(image):
        for m in range(1,9):
            line = ""
            for j in range(len(image[0])):
                line += image[n][j][m][1:9]
            new_image.append(line)

    return new_image

def mark_seamonster(image):
    """ Mark seamonsters """
    seamonsters = 0

    for i in range(len(image)-2):
        for j in range(len(image[0])-20):
            if image[i][j+18] != '#':
                continue
            if image[i+1][j] != '#':
                continue
            if image[i+1][j+5] != '#':
                continue
            if image[i+1][j+6] != '#':
                continue
            if image[i+1][j+11] != '#':
                continue
            if image[i+1][j+12] != '#':
                continue
            if image[i+1][j+17] != '#':
                continue
            if image[i+1][j+18] != '#':
                continue
            if image[i+1][j+19] != '#':
                continue
            if image[i+2][j+1] != '#':
                continue
            if image[i+2][j+4] != '#':
                continue
            if image[i+2][j+7] != '#':
                continue
            if image[i+2][j+10] != '#':
                continue
            if image[i+2][j+13] != '#':
                continue
            if image[i+2][j+16] != '#':
                continue

            # Found one
            seamonsters += 1

            # Mark it
            image[i  ][j+18] = 'O'

            image[i+1][j   ] = 'O'
            image[i+1][j+5 ] = 'O'
            image[i+1][j+6 ] = 'O'
            image[i+1][j+11] = 'O'
            image[i+1][j+12] = 'O'
            image[i+1][j+17] = 'O'
            image[i+1][j+18] = 'O'
            image[i+1][j+19] = 'O'

            image[i+2][j+1 ] = 'O'
            image[i+2][j+4 ] = 'O'
            image[i+2][j+7 ] = 'O'
            image[i+2][j+10] = 'O'
            image[i+2][j+13] = 'O'
            image[i+2][j+16] = 'O'

    return seamonsters

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
    image_grid = create_image_grid(image_parts)
    image = [ [ image_parts[img] for img in row] for row in image_grid ]
    image = align_image_parts(image)
    image = cleanup_image(image)

    # Find seamonster, flip and rotate until some found
    found = 0
    i = 0
    while found < 1:
        i += 1
        if i == 5:
            image = flip_image_horz(image)
        image = [ list(line) for line in image]
        found = mark_seamonster(image)
        if found > 1:
            break
        image = rotate_image(image)

    # Calculate high-sea
    high_sea = 0
    for line in image:
        high_sea += line.count('#')
    print(high_sea)


if __name__ == "__main__":
    main()
