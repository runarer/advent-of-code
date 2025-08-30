"""Advent of Code: 2022.19.2"""
import sys
import math

def make_ore_robot(blueprint,path):
    """ Makes a ore robot if it can. """
    r_ore,r_clay,r_obsidian,r_geodes,ore,clay,obsidian,geodes,minutes = path

    if r_ore < max(blueprint['clay-ore'],blueprint['obsidian-ore'],blueprint['geode-ore']):
        ore_needed = blueprint['ore-ore']-ore
        time_to_produce_ore = 0
        if ore_needed > 0:
            time_to_produce_ore = int(math.ceil(ore_needed/r_ore))

        time_to_make_ore_robot = 1 + time_to_produce_ore
        if minutes > time_to_make_ore_robot:
            new_ore = ore - blueprint['ore-ore'] + r_ore * time_to_make_ore_robot
            new_clay = clay + r_clay * time_to_make_ore_robot
            new_obsidian = obsidian + r_obsidian * time_to_make_ore_robot
            new_geodes = geodes + r_geodes * time_to_make_ore_robot
            return (r_ore+1,r_clay,r_obsidian,r_geodes,new_ore,new_clay,new_obsidian,new_geodes,minutes-time_to_make_ore_robot)
    return (r_ore,r_clay,r_obsidian,r_geodes,ore,clay,obsidian,geodes,-1)

def make_clay_robot(blueprint,path):
    """ Makes a clay robot if it can. """
    r_ore,r_clay,r_obsidian,r_geodes,ore,clay,obsidian,geodes,minutes = path

    if r_clay < blueprint['obsidian-clay']:
        ore_needed = blueprint['clay-ore']-ore
        time_to_produce_ore = 0
        if ore_needed > 0:
            time_to_produce_ore = int(math.ceil(ore_needed/r_ore))
        time_to_make_clay_robot = 1 + time_to_produce_ore
        if minutes > time_to_make_clay_robot:
            new_ore = ore - blueprint['clay-ore'] + r_ore * time_to_make_clay_robot
            new_clay = clay + r_clay * time_to_make_clay_robot
            new_obsidian = obsidian + r_obsidian * time_to_make_clay_robot
            new_geodes = geodes + r_geodes * time_to_make_clay_robot
            return (r_ore,r_clay+1,r_obsidian,r_geodes,new_ore,new_clay,new_obsidian,new_geodes,minutes-time_to_make_clay_robot)
    return (r_ore,r_clay,r_obsidian,r_geodes,ore,clay,obsidian,geodes,-1)
            
def make_obsidian_robot(blueprint,path):
    """ Makes a obsidian robot if it can. """
    r_ore,r_clay,r_obsidian,r_geodes,ore,clay,obsidian,geodes,minutes = path

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
            new_ore = ore - blueprint['obsidian-ore'] + r_ore * time_to_make_obsidian_robot
            new_clay = clay - blueprint['obsidian-clay'] + r_clay * time_to_make_obsidian_robot
            new_obsidian = obsidian + r_obsidian * time_to_make_obsidian_robot
            new_geodes = geodes + r_geodes * time_to_make_obsidian_robot
            return (r_ore,r_clay,r_obsidian+1,r_geodes,new_ore,new_clay,new_obsidian,new_geodes,minutes-time_to_make_obsidian_robot)

    return (r_ore,r_clay,r_obsidian,r_geodes,ore,clay,obsidian,geodes,-1)

def make_geode_robot(blueprint,path):
    """ Makes a geode if it can. """
    r_ore,r_clay,r_obsidian,r_geodes,ore,clay,obsidian,geodes,minutes = path
    
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
            new_ore = ore - blueprint['geode-ore'] + r_ore * time_to_make_geode_robot
            new_clay = clay + r_clay * time_to_make_geode_robot
            new_obsidian = obsidian - blueprint['geode-obsidian'] + r_obsidian * time_to_make_geode_robot
            new_geodes = geodes + r_geodes * time_to_make_geode_robot
            return (r_ore,r_clay,r_obsidian,r_geodes+1,new_ore,new_clay,new_obsidian,new_geodes,minutes-time_to_make_geode_robot)
    
    return (r_ore,r_clay,r_obsidian,r_geodes,ore,clay,obsidian,geodes,-1)

def find_paths(blueprint,path):
    """Shut up for now!"""
    r_ore,r_clay,r_obsidian,r_geodes,ore,clay,obsidian,geodes,minutes = path

    no_robot_to_build = False

    new_paths = []

    ore_robot = make_ore_robot(blueprint,path)
    clay_robot = make_clay_robot(blueprint,path)
    obsidian_robot = make_obsidian_robot(blueprint,path)
    geode_robot = make_geode_robot(blueprint,path)

    if ore_robot[8] < 1 and clay_robot[8] < 1 and obsidian_robot[8] < 1 and geode_robot[8] < 1:
        no_robot_to_build = True

    # Is it better to make ore -> clay than just clay
    if ore_robot[8] > 0:
        new_paths.append(ore_robot)

    if clay_robot[8] > 0:
        ore_clay_combo = make_clay_robot(blueprint,ore_robot)
        # Is it faster to make ore -> clay and do we have the same amount of ore left
        if ore_clay_combo[8] < clay_robot[8] or ore_clay_combo[4] < clay_robot[4]:
            new_paths.append(clay_robot)

    if obsidian_robot[8] > 0:
        clay_obsidian_combo = make_obsidian_robot(blueprint,clay_robot)

        if clay_obsidian_combo[8] < obsidian_robot[8] or clay_obsidian_combo[5] < obsidian_robot[5]:
            new_paths.append(obsidian_robot)

    if geode_robot[8] > 0:
        obsidian_geode_combo = make_geode_robot(blueprint,obsidian_robot)

        if obsidian_geode_combo[8] < geode_robot[8] or obsidian_geode_combo[6] < geode_robot[6]:
            new_paths.append(geode_robot)

    if no_robot_to_build:
        # Can't build anymore robots. So add resources, this can be calculated instead of loop
        while minutes > 0:
            minutes -= 1
            ore += r_ore
            clay += r_clay
            obsidian += r_obsidian
            geodes += r_geodes        
        return [(r_ore,r_clay,r_obsidian,r_geodes,ore,clay,obsidian,geodes,minutes)]

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
            if new_path[8] == 0:
                completed_paths.add(new_path)
            else:
                paths.add(new_path)

    max_path = (0,0,0,0,0,0,0,0,0)
    for path in completed_paths:
        if max_path[7] < path[7]:
            max_path = path
    return max_path[7]

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

    print("First started")
    first = collect_geodes(blueprints[1],32)
    print("First: ", first)
    print("Second started")
    second = collect_geodes(blueprints[2],32)
    print("Second:", second)
    print("Third started")
    third = collect_geodes(blueprints[3],32)
    print("Third: ",third)
    print("Results:", first*second*third)

if __name__ == "__main__":
    main()

#from enum import Enum
# class Choice(Enum):
#     """The choices"""
#     Build_Ore_Robot = 1
#     Build_Clay_Robot = 2
#     Build_Obsidian_Robot = 3
#     Build_Geode_Robot = 4

# def list_choices(blueprint, path):
#     """ Give the choices that robots and resources gives. """
#     r_ore,r_clay,r_obsidian,_,ore,clay,obsidian,_ = path
#     choices = set()

#     # Can we build ore robot? Can we wait for ore robots?
#     if ore >= blueprint['ore-ore'] and r_ore < max(blueprint['clay-ore'],blueprint['obsidian-ore'],blueprint['geode-ore']):
#         choices.add(Choice.Build_Ore_Robot)
#     else:
#         choices.add(Choice.Wait)

#     # Can we build clay robot? Can we wait for clay robots?
#     if ore >= blueprint['clay-ore'] and r_clay < blueprint['obsidian-clay']:
#         choices.add(Choice.Build_Clay_Robot)
#     else:
#         choices.add(Choice.Wait)

#     # Can we build obsidian robot? Can we wait for obsidian robots?
#     if ore >= blueprint['obsidian-ore'] and clay >= blueprint['obsidian-clay'] and r_obsidian < blueprint['geode-obsidian']:
#         choices.add(Choice.Build_Obsidian_Robot)
#     elif r_clay > 0:
#         choices.add(Choice.Wait)

#     # Can we build geode robot? Can we wait for geode robots?
#     if ore >= blueprint['geode-ore'] and obsidian >= blueprint['geode-obsidian']:
#         choices.add(Choice.Build_Geode_Robot)
#     elif r_obsidian > 0:
#         choices.add(Choice.Wait)

#     return choices

# def collect_resources(path):
#     """ Adds resources to the pile """
#     r_ore,r_clay,r_obsidian,r_geodes,ore,clay,obsidian,geodes = path

#     ore += r_ore
#     clay += r_clay
#     obsidian += r_obsidian
#     geodes += r_geodes

#     return (ore,clay,obsidian,geodes)

# def build_robots(blueprint, path, choice):
#     """ Build the robot. """
#     r_ore,r_clay,r_obsidian,r_geodes,ore,clay,obsidian,geodes = path

#     if choice == Choice.Build_Ore_Robot:
#         r_ore += 1
#         ore -= blueprint['ore-ore']
#     elif choice == Choice.Build_Clay_Robot:
#         r_clay += 1
#         ore -= blueprint['clay-ore']
#     elif choice == Choice.Build_Obsidian_Robot:
#         r_obsidian += 1
#         ore -= blueprint['obsidian-ore']
#         clay -= blueprint['obsidian-clay']
#     elif choice == Choice.Build_Geode_Robot:
#         r_geodes += 1
#         ore -= blueprint['geode-ore']
#         obsidian -= blueprint['geode-obsidian']

#     return (r_ore,r_clay,r_obsidian,r_geodes,ore,clay,obsidian,geodes)




    # Make desisions
    #if r_ore < max(blueprint['clay-ore'],blueprint['obsidian-ore'],blueprint['geode-ore']):
        # How much time does it take to build one
        # ore_needed = blueprint['ore-ore']-ore
        # time_to_produce_ore = 0
        # if ore_needed > 0:
        #     time_to_produce_ore = int(math.ceil(ore_needed/r_ore))
        # time_to_make_ore_robot = 1 + time_to_produce_ore
        # if minutes > time_to_make_ore_robot:
        #     no_robot_to_build = False
        #     new_ore = ore - blueprint['ore-ore'] + r_ore * time_to_make_ore_robot
        #     new_clay = clay + r_clay * time_to_make_ore_robot
        #     new_obsidian = obsidian + r_obsidian * time_to_make_ore_robot
        #     new_geodes = geodes + r_geodes * time_to_make_ore_robot
        #     new_paths.append((r_ore+1,r_clay,r_obsidian,r_geodes,new_ore,new_clay,new_obsidian,new_geodes,minutes-time_to_make_ore_robot))

    # if ore robots are not at their max, if the ore that can be made before clay robot
    # is more than is needed by the clay by an amount that lets us make a new ore robot, then that is 
    # a better choice than making a clay robot.

    #if r_clay < blueprint['obsidian-clay']:
        # ore_needed = blueprint['clay-ore']-ore
        # time_to_produce_ore = 0
        # if ore_needed > 0:
        #     time_to_produce_ore = int(math.ceil(ore_needed/r_ore))
        # time_to_make_clay_robot = 1 + time_to_produce_ore
        # if minutes > time_to_make_clay_robot:
        #     no_robot_to_build = False
        #     new_ore = ore - blueprint['clay-ore'] + r_ore * time_to_make_clay_robot
        #     new_clay = clay + r_clay * time_to_make_clay_robot
        #     new_obsidian = obsidian + r_obsidian * time_to_make_clay_robot
        #     new_geodes = geodes + r_geodes * time_to_make_clay_robot
        #     new_paths.append((r_ore,r_clay+1,r_obsidian,r_geodes,new_ore,new_clay,new_obsidian,new_geodes,minutes-time_to_make_clay_robot))

    #if r_obsidian < blueprint['geode-obsidian'] and r_clay > 0:
        # ore_needed = blueprint['obsidian-ore']-ore
        # clay_needed = blueprint['obsidian-clay']-clay
        # time_to_produce_ore = 0
        # time_to_produce_clay = 0
        # if ore_needed > 0:
        #     time_to_produce_ore = int(math.ceil(ore_needed/r_ore))
        # if clay_needed > 0:
        #     time_to_produce_clay = int(math.ceil(clay_needed/r_clay))
        # time_to_make_obsidian_robot = 1 + max(time_to_produce_ore,time_to_produce_clay)
        # if minutes > time_to_make_obsidian_robot:
        #     no_robot_to_build = False
        #     new_ore = ore - blueprint['obsidian-ore'] + r_ore * time_to_make_obsidian_robot
        #     new_clay = clay - blueprint['obsidian-clay'] + r_clay * time_to_make_obsidian_robot
        #     new_obsidian = obsidian + r_obsidian * time_to_make_obsidian_robot
        #     new_geodes = geodes + r_geodes * time_to_make_obsidian_robot
        #     new_paths.append((r_ore,r_clay,r_obsidian+1,r_geodes,new_ore,new_clay,new_obsidian,new_geodes,minutes-time_to_make_obsidian_robot))

    # if r_obsidian > 0:
    #     ore_needed = blueprint['geode-ore']-ore
    #     obsidian_needed = blueprint['geode-obsidian']-obsidian
    #     time_to_produce_ore = 0
    #     time_to_produce_obsidian = 0
    #     if ore_needed > 0:
    #         time_to_produce_ore = int(math.ceil(ore_needed/r_ore))
    #     if obsidian_needed > 0:
    #         time_to_produce_obsidian = int(math.ceil(obsidian_needed/r_obsidian))
    #     time_to_make_geode_robot = 1 + max(time_to_produce_ore,time_to_produce_obsidian)
    #     if minutes > time_to_make_geode_robot:
    #         no_robot_to_build = False
    #         new_ore = ore - blueprint['geode-ore'] + r_ore * time_to_make_geode_robot
    #         new_clay = clay + r_clay * time_to_make_geode_robot
    #         new_obsidian = obsidian - blueprint['geode-obsidian'] + r_obsidian * time_to_make_geode_robot
    #         new_geodes = geodes + r_geodes * time_to_make_geode_robot
    #         new_paths.append((r_ore,r_clay,r_obsidian,r_geodes+1,new_ore,new_clay,new_obsidian,new_geodes,minutes-time_to_make_geode_robot))
