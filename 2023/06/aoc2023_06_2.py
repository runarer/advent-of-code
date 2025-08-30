"""
    Advent of Code: 2019.1.1
    if i hold the whole time it wont travel. if i hold the whole time minus
    one second it will travel time-1, if i hold the whole time minus 2 seconds ¨
    it will travel (time-2)*2 and so on. (time-3)*3... 
    
    distance_traveled = (time-hold_time)*(time-(time-hold_time))

    distance_traveled = hold_time*(time-hold_time)

    kan løse 0 = (-1*hold_time)**2 + hold_time*time - distance
"""

import sys

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
    time = int("".join(lines[0].split(':')[1].split()))
    record = int("".join(lines[1].split(':')[1].split()))

    min_hold_time = time
    for hold_time in range(int(record/time),time):
        if record - (time - hold_time)*hold_time < 0:
            min_hold_time = hold_time
            break
    max_hold_time = time - min_hold_time
    
    print(f'wins: {max_hold_time-min_hold_time+1}')

if __name__ == "__main__":
    main()
