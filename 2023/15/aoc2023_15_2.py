"""Advent of Code: 2019.1.1"""
import sys
from functools import reduce

def lhash(label):
    return reduce(lambda x,y: ((x+ord(y))*17)%256,label,0)

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
    lens_boxes = [ {} for i in range(256)]

    for inst in lines[0].strip().split(','):
        if '-' in inst:
            label = inst[:-1]
            if label in lens_boxes[lhash(label)]:
                del lens_boxes[lhash(label)][label]
        elif '=' in inst:
            label, focal_length = inst.split('=')
            lens_boxes[lhash(label)][label] = int(focal_length)

    print(sum(sum((k+1)*(i+1)*n for i,n in enumerate(v.values())) for k,v in enumerate(lens_boxes)))

if __name__ == "__main__":
    main()
