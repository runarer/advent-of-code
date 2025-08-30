"""Advent of Code: 2022.19.1"""
import sys
from enum import Enum

class Choice(Enum):
    """The choices"""
    Build_Ore_Robot = 1
    Build_Clay_Robot = 2
    Build_Obsidian_Robot = 3
    Build_Geode_Robot = 4
    Wait = 100
    # Wait_for_Ore_Robot = 10
    # Wait_for_Clay_Robot = 20
    # Wait_for_Obsidian_Robot = 30
    # Wait_for_Geode_Robot = 40

def list_choices(blueprint, robots, resources):
    """ Give the choices that robots and resources gives. """
    choices = set()
    # Can we build ore robot? Can we wait for ore robots?
    if resources['ore'] >= blueprint['ore-ore']:
        choices.add(Choice.Build_Ore_Robot)
    else:
        #choices.append(Choice.Wait_for_Ore_Robot)
        choices.add(Choice.Wait)

    # Can we build clay robot? Can we wait for clay robots?
    if resources['ore'] >= blueprint['clay-ore']:
        choices.add(Choice.Build_Clay_Robot)
    else:
        #choices.append(Choice.Wait_for_Clay_Robot)
        choices.add(Choice.Wait)

    # Can we build obsidian robot? Can we wait for obsidian robots?
    if resources['ore'] >= blueprint['obsidian-ore'] and resources['clay'] >= blueprint['obsidian-clay']:
        choices.add(Choice.Build_Obsidian_Robot)
    elif robots['clay'] > 0:
        #choices.append(Choice.Wait_for_Obsidian_Robot)
        choices.add(Choice.Wait)

    # Can we build geode robot? Can we wait for geode robots?
    if resources['ore'] >= blueprint['geode-ore'] and resources['obsidian'] >= blueprint['obsidian-clay']:
        choices.add(Choice.Build_Geode_Robot)
    elif robots['obsidian'] > 0:
        #choices.append(Choice.Wait_for_Geode_Robot)
        choices.add(Choice.Wait)

    return choices

def collect_resources(robots,resources):
    """ Adds resources to the pile """
    for robot_type, number in robots.items():
        resources[robot_type] += number

def build_robots(blueprint, robots, resources, choice):
    """ Build the robot. """
    if choice == Choice.Build_Ore_Robot:
        robots['ore'] += 1
        resources['ore'] -= blueprint['ore-ore']
    elif choice == Choice.Build_Clay_Robot:
        robots['clay'] += 1
        resources['ore'] -= blueprint['clay-ore']
    elif choice == Choice.Build_Obsidian_Robot:
        robots['obsidian'] += 1
        resources['ore'] -= blueprint['obsidian-ore']
        resources['clay'] -= blueprint['obsidian-clay']
    elif choice == Choice.Build_Geode_Robot:
        robots['geode'] += 1
        resources['ore'] -= blueprint['geode-ore']
        resources['obsidian'] -= blueprint['geode-obsidian']

def collect_geodes(blueprint,minutes):
    """ Blueprint """

    # Setup and collect initial resources.
    init_robots = {'ore':1,'clay':0,'obsidian':0,'geode':0}
    #resources = {'ore' : min(blueprint['ore-ore'],blueprint['clay-ore']), 'clay' : 0, 'obsidian' : 0, 'geodes' : 0}
    init_resources = {'ore' : 0, 'clay' : 0, 'obsidian' : 0, 'geode' : 0}
    minutes_run = 0
    #minutes_run = resources['ore']


    paths = [[init_resources,init_robots]]

    while minutes_run < minutes:
        minutes_run += 1

        paths_last_minute = len(paths)
        # remove_from_
        for i in range(paths_last_minute):
        #for path in paths:
            #resources, robots = path
            resources, robots = paths[i]
            choices = list_choices(blueprint,robots,resources)

            # Make choice            
            while choices:
                choice = choices.pop()

                new_resources = resources
                new_robots = robots

                # Not last choice so working with copies
                if choices:
                    new_resources = resources.copy()
                    new_robots = robots.copy()

                # Collect resources and then build robots
                collect_resources(new_robots,new_resources)
                build_robots(blueprint,new_robots,new_resources,choice)

                # Not last choice so adding copies to the end of paths
                if choices:
                    paths.append([new_resources,new_robots])
    print(len(paths))



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

    # Select blueprint
    blueprint = blueprints[1] # Just to test
    collect_geodes(blueprint,12)



if __name__ == "__main__":
    main()
