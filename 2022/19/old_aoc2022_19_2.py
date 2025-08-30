"""Advent of Code: 2022.19.2"""
import sys
from enum import Enum

class Choice(Enum):
    """The choices"""
    Build_Ore_Robot = 1
    Build_Clay_Robot = 2
    Build_Obsidian_Robot = 3
    Build_Geode_Robot = 4
    Wait = 100

def list_choices(blueprint, path):
    """ Give the choices that robots and resources gives. """
    r_ore,r_clay,r_obsidian,_,ore,clay,obsidian,_ = path
    choices = set()

    # Can we build ore robot? Can we wait for ore robots?
    if ore >= blueprint['ore-ore'] and r_ore < max(blueprint['clay-ore'],blueprint['obsidian-ore'],blueprint['geode-ore']):
        choices.add(Choice.Build_Ore_Robot)
    else:
        choices.add(Choice.Wait)

    # Can we build clay robot? Can we wait for clay robots?
    if ore >= blueprint['clay-ore'] and r_clay < blueprint['obsidian-clay']:
        choices.add(Choice.Build_Clay_Robot)
    else:
        choices.add(Choice.Wait)

    # Can we build obsidian robot? Can we wait for obsidian robots?
    if ore >= blueprint['obsidian-ore'] and clay >= blueprint['obsidian-clay'] and r_obsidian < blueprint['geode-obsidian']:
        choices.add(Choice.Build_Obsidian_Robot)
    elif r_clay > 0:
        choices.add(Choice.Wait)

    # Can we build geode robot? Can we wait for geode robots?
    if ore >= blueprint['geode-ore'] and obsidian >= blueprint['geode-obsidian']:
        choices.add(Choice.Build_Geode_Robot)
    elif r_obsidian > 0:
        choices.add(Choice.Wait)

    return choices

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

def collect_geodes(blueprint,minutes):
    """ Blueprint """

    # Setup and collect initial resources.
    minutes_run = 0

    paths = set()
    paths.add((1,0,0,0,0,0,0,0))

    while minutes_run < minutes:
        minutes_run += 1
        
        new_paths = set()

        while paths:
            path = paths.pop()
            
            choices = list_choices(blueprint,path)

            # Make choice
            while choices:
                choice = choices.pop()
                r_ore,r_clay,r_obsidian,r_geodes,ore,clay,obsidian,geodes = path

                # Collect resources and then build robots                
                ore += r_ore
                clay += r_clay
                obsidian += r_obsidian
                geodes += r_geodes

                if choice == Choice.Build_Ore_Robot:
                    r_ore += 1
                    ore -= blueprint['ore-ore']
                elif choice == Choice.Build_Clay_Robot:
                    r_clay += 1
                    ore -= blueprint['clay-ore']
                elif choice == Choice.Build_Obsidian_Robot:
                    r_obsidian += 1
                    ore -= blueprint['obsidian-ore']
                    clay -= blueprint['obsidian-clay']
                elif choice == Choice.Build_Geode_Robot:
                    r_geodes += 1
                    ore -= blueprint['geode-ore']
                    obsidian -= blueprint['geode-obsidian']

                #ore,clay,obsidian,geodes = collect_resources(path)
                #r_ore,r_clay,r_obsidian,r_geodes = build_robots(blueprint,path,choice)

                new_paths.add((r_ore,r_clay,r_obsidian,r_geodes,ore,clay,obsidian,geodes))

        paths = new_paths
    #print(len(paths))
    print(paths)

    max_path = (0,0,0,0,0,0,0,0)
    for path in paths:
        if max_path[7] < path[7]:
            max_path = path
    return max_path[7]

    # for path in paths:
    #     if path[7] == max_path[7]:
    #         print(path)
        


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
        # blueprints[ int(line_parts[1][0:-1]) ] = [int(line_parts[6]),
        #                                           int(line_parts[12]),
        #                                           int(line_parts[18]),
        #                                           int(line_parts[21]),
        #                                           int(line_parts[27]),
        #                                           int(line_parts[30])]
        blueprints[ int(line_parts[1][0:-1]) ] = {'ore-ore': int(line_parts[6]),
                                                  'clay-ore':int(line_parts[12]),
                                                  'obsidian-ore':int(line_parts[18]),
                                                  'obsidian-clay':int(line_parts[21]),
                                                  'geode-ore':int(line_parts[27]),
                                                  'geode-obsidian':int(line_parts[30]) }
    #print(blueprints)

    print("First started")
    first = collect_geodes(blueprints[1],4)
    print("First: ", first)
    # print("Second started")
    # second = collect_geodes(blueprints[2],32)
    # print("Second:", second)
    # print("Results:", first*second)
    # print("Third started")
    # third = collect_geodes(blueprints[3],32)
    # print("Third: ",third)
    # print("Results:", first*second*third)




if __name__ == "__main__":
    main()

# at minute 4 a bad desision is made (1, 0, 0, 0, 3, 0, 0, 0) ->  (1, 1, 0, 0, 2, 0, 0, 0)
# It waited one minute to create a clay robot.