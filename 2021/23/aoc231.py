"""
Ta utgangspunkt i tilstanden. finn alle lovlige trekk. Dette gir en liste over alle
mulige veier videre samt dens energibruk. Sorter basert på energibruk og gå videre med den første.
Dette vil gi en max energi som kan sendes med videre til kall nedover listen. Så fort noen får lik
eller høyere energi så kuttes søket.

Rekkefølge for trekk.
    1.  Fra rom til destinasjon. Dette oppdaterer rooms slik at alle eterfølgende søk bruker dette
        utgangspunktet.
    2.  Fra hallway to destinasjon. Dette oppdaterer også rooms slik at alle eterfølgende søk
        bruker dette utgangspunktet.
    3.  Flytt fra room og ut til hallway. Her blir det en liste med flere muligheter. Kanskje vi
        skal rydde dem (1 og 2) før vi sorterer og går videre med flere flyninger ut til hallway?

    Så det er kun 3. som skaper nye "univers". 1 og 2 er opprydding som alltid vil gi det samme.
    1 og 2 kan testes seperat.
    1 og 2 må loopes til det ikke er mer igjen fordi en flytting kan gi mulighet for å flytte flere.

Funskjoner:
def energy_usage(type:chr,steps:int) -> int
def move_to_destination(hallway,room) -> int, returnere energien for å rydde opp.
def move(hallway,room,max_energy) -> int, returnere energien for å flytte alt til riktig plass.

Finnes det noe mulighet for å finne og kutte blokkeringer?

Skal jeg ta med antall igjen å plassere i sorteringen? Først antall, så energi.

Etter at to amphipod har beveget seg ut i hallway så vil det være dublikater i "listen" over
"univers". Disse vil utvikle seg likt og bør reduseres til kun et "univers". Kan gjøres med et set,
men da må jeg bytte fra lister til tupler.

From room to room implemented and tested.
From hallway to room next.
"""

def energy_usage(type:chr,steps:int) -> int:
    if type == 'A':
        return steps
    if type == 'B':
        return 10*steps
    if type == 'C':
        return 100*steps
    if type == 'D':
        return 1000*steps

def move_to_destination(hallway,rooms) -> int:
    # If nothing in the hallway, no way to change anything.
    if hallway.count('.') == 11:
        return 0

    destination_hallway = {'A':2,'B':4,'C':6,'D':8,}
    energy_used = 0
    done = False

    while not done:
        done = True
        # Check if i can move something from room to rooms        
        for i,amphipod in enumerate(rooms):
            if amphipod == '.':
                continue

            destination = destination_hallway[amphipod]

            # Is the amphipod allready home?
            if i in (destination-1,destination-2):
                continue

            # Is the destination free? If only the first space, is the second space occupied by
            # the right amphipod.
            if rooms[destination-2] != '.':
                continue
            if rooms[destination-1] != '.':
                if rooms[destination-1] != amphipod:
                    continue

            ## Is amphipod in last part of room, if so the space infront must be free.
            if i % 2 == 1:
                if rooms[i-1] != '.':
                    continue

            # Is the path blocked?
            ## Enter hallway, need to go to hallway destination, nothing but '.' between them.
            ## destination er hallway destination
            hallway_entry = 0
            if i < 2:
                hallway_entry = 2
            elif i < 4:
                hallway_entry = 4
            elif i < 6:
                hallway_entry = 6
            else:
                hallway_entry = 8

            ## Steps to move into the hallway
            steps = 1
            if i in (1,3,5,7):
                steps = 2

            blocked = False
            if hallway_entry < destination:
                #move right
                for space in range(hallway_entry+1,destination+1):
                    if hallway[space] != '.':
                        blocked = True
                        break
                steps += destination - hallway_entry
            else:
                # move left
                for space in range(destination,hallway_entry):
                    if hallway[space] != '.':
                        blocked = True
                        break
                steps += hallway_entry - destination

            if blocked:
                continue

            # move
            rooms[i] = '.'
            if rooms[destination-1] == '.':
                rooms[destination-1] = amphipod
                steps += 2
            else:
                rooms[destination-2] = amphipod
                steps += 1
            energy_used += energy_usage(amphipod,steps)

            # Moved something? done = False else: done = True
            done = False

        # Check if i can move something from hallway to rooms
        for i,amphipod in enumerate(hallway):
            if amphipod == '.':
                continue

            destination = destination_hallway[amphipod]

            # Is destination not free or occupied by an amphipod that is not in it final destination
            if rooms[destination-2] != '.':
                continue
            if rooms[destination-1] != '.':
                if rooms[destination-1] != amphipod:
                    continue

            # Is the path blocked? Also calculate steps.
            blocked = False
            steps = 0
            if i < destination:
                #move right
                for space in range(i+1,destination):
                    if hallway[space] != '.':
                        blocked = True
                        break
                steps += destination - i
            else:
                # move left
                for space in range(destination+1,i):
                    if hallway[space] != '.':
                        blocked = True
                        break
                steps += i - destination
            if blocked:
                continue

            # Move the amphipod
            hallway[i] = '.'
            if rooms[destination-1] == '.':
                rooms[destination-1] = amphipod
                steps += 2
            else:
                rooms[destination-2] = amphipod
                steps += 1
            energy_used += energy_usage(amphipod,steps)

            # Moved something? done = False else: done = True
            done = False

        
    return energy_used

def moves_to_the_hallway(hallway,rooms,energy):
    """ Returns a list of all the possible moves into the hallway from a given situasjon. """
    universes = []
    destination_hallway = {'A':2,'B':4,'C':6,'D':8,}

    for i, amphipod in enumerate(rooms):
        if amphipod == '.':
            continue
        
        # Is the amphipod blocked from entering the hallway?
        if i % 2 == 1:
            if rooms[i-1] != '.':
                continue

        # Is the amphipod already in place
        if i == destination_hallway[amphipod]-1:
            continue
        if i == destination_hallway[amphipod]-2 and rooms[i+1] == amphipod: #Out of bound? make two if's
            continue

        # Create all possible moves for this amphipod
        for destination,hallway_space in enumerate(hallway):
            if destination in (2,4,6,8): # cant stop outside a room
                continue
            if hallway_space != '.': # Occupied
                continue

            # Where do the amphipod enter the hallway
            hallway_entry = 0
            if i < 2:
                hallway_entry = 2
            elif i < 4:
                hallway_entry = 4
            elif i < 6:
                hallway_entry = 6
            else:
                hallway_entry = 8

            # Is the path blocked?
                        
            blocked = False
            # Steps to move into the hallway
            steps = 1
            if i in (1,3,5,7):
                steps = 2

            if hallway_entry < destination:
                #move right
                for space in range(hallway_entry+1,destination+1):
                    if hallway[space] != '.':
                        blocked = True
                        break
                steps += destination - hallway_entry
            else:
                # move left
                for space in range(destination,hallway_entry):
                    if hallway[space] != '.':
                        blocked = True
                        break
                steps += hallway_entry - destination
            
            if blocked:
                continue

            # New univers discovered
            new_hallway = list(hallway)
            new_hallway[destination] = amphipod
            new_rooms = list(rooms)
            new_rooms[i] = '.'
            energy_used = energy_usage(amphipod,steps)
            universes.append([new_hallway,new_rooms,energy_used+energy])

    return universes

def make_moves(hallway,rooms):
    def same_list(list1, list2) -> bool:
        for i,item in enumerate(list1):
            if list2[i] != item:
                return False
        return True
    min_energy = 1000000
    universes = moves_to_the_hallway(hallway,rooms,0)

    while True:
        print("Working...")
        next_universes = []
        for universe in universes:
            # Is it a solved universe
            if same_list(universe[1],['A','A','B','B','C','C','D','D']):
                min_energy = min(universe[2],min_energy)
                continue

            # Is this universe already using more energy than the best solution so far
            if universe[2] >= min_energy:
                continue

            new_universes = moves_to_the_hallway(universe[0],universe[1],universe[2])

            for i,_ in enumerate(new_universes):
                new_universes[i][2] += move_to_destination(new_universes[i][0],new_universes[i][1])

            next_universes += new_universes

        if not next_universes:
            break

        next_universes.sort(key=lambda x:x[2])
        universes = [next_universes[i] for i in range(len(next_universes)) if i == 0 or next_universes[i] != next_universes[i-1]]

    return min_energy

def test_move_to_destination():
    #Testcases for def move_to_destination
    # Skal flytte 'B' fra testroom[0] til testroom[3]
    # og 'D' fra
    # Så: ['A','B','.','B','C','C','D','A']
    test_hallway_1 = ['.','.','.','.','.','C','.','.','.','D','.']
    test_rooms_1 = ['B','A','.','B','D','C','.','A']
    print(test_hallway_1,test_rooms_1)
    energy_used = move_to_destination(test_hallway_1,test_rooms_1)
    print(test_hallway_1,test_rooms_1,"Used", energy_used)

    # Skal flytte 'B' fra hallway til testroom[3]
    # Så: ['A','B','.','B','C','C','D','A']
    test_hallway_1 = ['.','.','.','B','.','D','.','.','.','.','.']
    test_rooms_1 = ['A','B','.','.','C','C','D','A']
    print(test_hallway_1,test_rooms_1)
    energy_used = move_to_destination(test_hallway_1,test_rooms_1)
    print(test_hallway_1,test_rooms_1,"Used", energy_used)

    # Skal flytte begge 'D' fra hallway til testroom[3]
    # Så: ['.','A','B','B','C','C','D','D']
    test_hallway_2 = ['.','.','.','.','.','D','.','D','.','A','.']
    test_rooms_2 = ['.','A','B','B','C','C','.','.']
    print(test_hallway_2,test_rooms_2)
    energy_used = move_to_destination(test_hallway_2,test_rooms_2)
    print(test_hallway_2,test_rooms_2,"Used", energy_used)

def main():
    hallway = ['.' for _ in range(11)]
    # Test
    # rooms = ['B','A','C','D','B','C','D','A']
    
    # Input
    rooms = ['C','B','B','C','D','A','D','A']

    min_energy = make_moves(hallway,rooms)
    print(min_energy)

if __name__ == "__main__":
    main()
