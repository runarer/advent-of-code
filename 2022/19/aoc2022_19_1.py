"""Advent of Code: 2022.19.2"""
import sys
import math

def find_paths(blueprint,path):
    """Shut up for now!"""
    r_ore,r_clay,r_obsidian,r_geodes,ore,clay,obsidian,geodes,minutes = path
    
    no_robot_to_build = True

    new_paths = []

    # Make desisions
    if r_ore < max(blueprint['clay-ore'],blueprint['obsidian-ore'],blueprint['geode-ore']):
        # How much time does it take to build one
        ore_needed = blueprint['ore-ore']-ore
        time_to_produce_ore = 0
        if ore_needed > 0:
            time_to_produce_ore = int(math.ceil(ore_needed/r_ore))
        time_to_make_ore_robot = 1 + time_to_produce_ore
        if minutes > time_to_make_ore_robot:
            no_robot_to_build = False
            new_ore = ore - blueprint['ore-ore'] + r_ore * time_to_make_ore_robot
            new_clay = clay + r_clay * time_to_make_ore_robot
            new_obsidian = obsidian + r_obsidian * time_to_make_ore_robot
            new_geodes = geodes + r_geodes * time_to_make_ore_robot
            new_paths.append((r_ore+1,r_clay,r_obsidian,r_geodes,new_ore,new_clay,new_obsidian,new_geodes,minutes-time_to_make_ore_robot))

    # if ore robots are not at their max, if the ore that can be made before clay robot
    # is more than is needed by the clay by an amount that lets us make a new ore robot, then that is 
    # a better choice than making a clay robot.

    if r_clay < blueprint['obsidian-clay']:
        ore_needed = blueprint['clay-ore']-ore
        time_to_produce_ore = 0
        if ore_needed > 0:
            time_to_produce_ore = int(math.ceil(ore_needed/r_ore))
        time_to_make_clay_robot = 1 + time_to_produce_ore
        if minutes > time_to_make_clay_robot:
            no_robot_to_build = False
            new_ore = ore - blueprint['clay-ore'] + r_ore * time_to_make_clay_robot
            new_clay = clay + r_clay * time_to_make_clay_robot
            new_obsidian = obsidian + r_obsidian * time_to_make_clay_robot
            new_geodes = geodes + r_geodes * time_to_make_clay_robot
            new_paths.append((r_ore,r_clay+1,r_obsidian,r_geodes,new_ore,new_clay,new_obsidian,new_geodes,minutes-time_to_make_clay_robot))

    if r_obsidian < blueprint['geode-obsidian'] and r_clay > 0:
        ore_needed = blueprint['obsidian-ore']-ore
        clay_needed = blueprint['obsidian-clay']-clay
        time_to_produce_ore = 0
        time_to_produce_clay = 0
        if ore_needed > 0:
            time_to_produce_ore = int(math.ceil(ore_needed/r_ore))
        if clay_needed > 0:
            time_to_produce_clay = int(math.ceil(clay_needed/r_clay))
        time_to_make_obsidian_robot = 1 + max(time_to_produce_ore,time_to_produce_clay)
        if minutes > time_to_make_obsidian_robot:
            no_robot_to_build = False
            new_ore = ore - blueprint['obsidian-ore'] + r_ore * time_to_make_obsidian_robot
            new_clay = clay - blueprint['obsidian-clay'] + r_clay * time_to_make_obsidian_robot
            new_obsidian = obsidian + r_obsidian * time_to_make_obsidian_robot
            new_geodes = geodes + r_geodes * time_to_make_obsidian_robot
            new_paths.append((r_ore,r_clay,r_obsidian+1,r_geodes,new_ore,new_clay,new_obsidian,new_geodes,minutes-time_to_make_obsidian_robot))

    if r_obsidian > 0:
        ore_needed = blueprint['geode-ore']-ore
        obsidian_needed = blueprint['geode-obsidian']-obsidian
        time_to_produce_ore = 0
        time_to_produce_obsidian = 0
        if ore_needed > 0:
            time_to_produce_ore = int(math.ceil(ore_needed/r_ore))
        if obsidian_needed > 0:
            time_to_produce_obsidian = int(math.ceil(obsidian_needed/r_obsidian))
        time_to_make_geode_robot = 1 + max(time_to_produce_ore,time_to_produce_obsidian)
        if minutes > time_to_make_geode_robot:
            no_robot_to_build = False
            new_ore = ore - blueprint['geode-ore'] + r_ore * time_to_make_geode_robot
            new_clay = clay + r_clay * time_to_make_geode_robot
            new_obsidian = obsidian - blueprint['geode-obsidian'] + r_obsidian * time_to_make_geode_robot
            new_geodes = geodes + r_geodes * time_to_make_geode_robot
            new_paths.append((r_ore,r_clay,r_obsidian,r_geodes+1,new_ore,new_clay,new_obsidian,new_geodes,minutes-time_to_make_geode_robot))

    if no_robot_to_build:
        # Can't build anymore robots. So add resources
        while minutes > 0:
            minutes -= 1
            ore += r_ore
            clay += r_clay
            obsidian += r_obsidian
            geodes += r_geodes
        new_paths.append((r_ore,r_clay,r_obsidian,r_geodes,ore,clay,obsidian,geodes,minutes))
    
    return new_paths

def collect_geodes(blueprint,minutes):
    """ Blueprint """

    # Setup and collect initial resources.
    paths = set()
    completed_paths = set()
    paths.add((1,0,0,0,0,0,0,0,minutes))

    while paths:
        path = paths.pop()
        new_paths = find_paths(blueprint,path)
        for new_path in new_paths:
            if new_path[8] < 1:
                completed_paths.add(new_path)
            else:
                paths.add(new_path)

    max_path = (0,0,0,0,0,0,0,0,0)
    for path in completed_paths:
        if max_path[7] < path[7]:
            max_path = path
    return max_path[7]
        
# max time to make geode is make clay -> make obsidian -> make geode

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

    blueprints = {}
    for line in lines:
        line_parts = line.strip().split()
        blueprints[ int(line_parts[1][0:-1]) ] = {'ore-ore': int(line_parts[6]),
                                                  'clay-ore':int(line_parts[12]),
                                                  'obsidian-ore':int(line_parts[18]),
                                                  'obsidian-clay':int(line_parts[21]),
                                                  'geode-ore':int(line_parts[27]),
                                                  'geode-obsidian':int(line_parts[30]) }
    total_quality = 0
    for i,blueprint in blueprints.items():
        print("Blueprint ",i)
        total_quality += i*collect_geodes(blueprint,24)
    print("Total Quality:",total_quality)



if __name__ == "__main__":
    main()
