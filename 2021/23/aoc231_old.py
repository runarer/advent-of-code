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

Funskjoner:
def energy_usage(type:chr,steps:int) -> int
def move_to_destination(hallway,room) -> int, returnere energien for å rydde opp.
def move(hallway,room,max_energy) -> int, returnere energien for å flytte alt til riktig plass.

Finnes det noe mulighet for å finne og kutte blokkeringer?
"""

def energy_usage(type:chr,steps:int) -> int:
    if type == 'A': return steps
    if type == 'B': return 10*steps
    if type == 'C': return 100*steps
    if type == 'D': return 1000*steps

def move(hallway,rooms) -> int:
    #Search ended
    if rooms == ['A','A','B','B','C','C','D','D']:
        return 0
    to_destination = move_to_destination(hallway,rooms)
    to_hallway = move_to_hallway(hallway,rooms)
    return min(to_hallway,to_destination)

def move_to_hallway(hallway,rooms) -> int:
    moves = []

    # Move all if amphipods in rooms
    for i,amphipod in enumerate(rooms):
        if amphipod == '.': continue # Room is empty
        
        if amphipod == 'A':
            if i == 1: continue # No need to move
            if i == 0 and rooms[1] == 'A': continue # 'A' is done

        if amphipod == 'B':
            if i == 3: continue # No need to move
            if i == 2 and rooms[3] == 'B': continue # 'B' is done

        if amphipod == 'C':
            if i == 5: continue # No need to move
            if i == 4 and rooms[5] == 'C': continue # 'C' is done

        if amphipod == 'D':
            if i == 7: continue # No need to move
            if i == 6 and rooms[7] == 'D': continue # 'D' is done
        
        if i % 2 == 1:
            if rooms[i-1] != '.': continue # blocked

        # Can move
        for hs_i,hallway_space in enumerate(hallway):
            if hs_i in (2,4,6,8): continue # cant stop outside a room
            if hallway_space != '.': continue # Occupied
            
            #From hallway_start (given by i) to hallway_space (amphipods destination)
            hallway_start = 0
            if i < 2: hallway_start = 2
            elif i < 4: hallway_start = 4
            elif i < 6: hallway_start = 6
            else: hallway_start = 8

            # Which direction, left right, given by hs_i smaller or larger than hallway_start
            blocked = False
            # Steps to move into the hallway
            steps = 1
            if i in (1,3,5,7): steps = 2

            if hallway_start < hs_i:
                #move right
                for space in range(hallway_start+1,hs_i+1):
                    if hallway[space] != '.':
                        blocked = True
                        break
                steps += hs_i - hallway_start
            else:
                # move left
                for space in range(hs_i,hallway_start):
                    if hallway[space] != '.':
                        blocked = True
                        break
                steps += hallway_start - hs_i

            if not blocked:
                print("Move to hallway:",amphipod,"From",i,"To",hs_i)
                new_hallway = list(hallway)
                new_hallway[hs_i] = amphipod
                new_rooms = list(rooms)
                new_rooms[i] = '.'
                new_move = move(new_hallway,new_rooms)
                energy_used = energy_usage(amphipod,steps) + new_move
                moves.append(energy_used)

    if moves:
        return min(moves)
    return 1000000 # no leagal moves

def move_to_destination(hallway,rooms) -> int:
    print(hallway,rooms)
    desination_hallway = {'A':2,'B':4,'C':6,'D':8,}
    moves = []

    # Can someone move from room to room?
    # This will update rooms, so i need a way to keep track of energy usage
    energy_used = 0
    for i,amphipod in enumerate(rooms):
        if amphipod == '.': continue
        des_room = desination_hallway[amphipod]
        
        # Is it allready in the right place
        if i == des_room-1 or i == des_room-2:
            continue 
        
        # Can it move out from room
        if i % 2 == 1:
            if rooms[i-1] != '.': continue

        # Is not there free room?
        if des_room-2 != '.': continue
        if des_room-1 != '.' or des_room-1 != amphipod: continue

        # Is the path blocked
        #From hallway_start (given by i) to hallway_space (amphipods destination)
        hallway_start = 0
        if i < 2: hallway_start = 2
        elif i < 4: hallway_start = 4
        elif i < 6: hallway_start = 6
        else: hallway_start = 8

        # Which direction, left right
        blocked = False
        # Steps to move into the hallway
        steps = 1
        if i in (1,3,5,7): steps = 2

        if hallway_start < des_room:
            #move right
            for space in range(hallway_start+1,des_room+1):
                if hallway[space] != '.':
                    blocked = True
                    break
            steps += des_room - hallway_start
        else:
            # move left
            for space in range(des_room,hallway_start):
                if hallway[space] != '.':
                    blocked = True
                    break
            steps += hallway_start - des_room        
        
        if blocked: continue

        # move
        rooms[i] = '.'
        if des_room-1 == '.':
            rooms[des_room-1] = amphipod
            steps += 2
        else:
            rooms[des_room-2] = amphipod
            steps += 1

        energy_used += energy_usage(amphipod,steps)

    for i,amphipod in enumerate(hallway):
        if amphipod == '.': continue # Spot is empty

        # Blocked from i to desination_hallway[amphipod]?        
        steps = 1
        blocked = False
        
        if i < desination_hallway[amphipod]:
            #move right
            for space in range(i+1,desination_hallway[amphipod]):
                if hallway[space] != '.':
                    blocked = True
                    break
            steps += desination_hallway[amphipod] - i
        else:
            # move left
            for space in range(desination_hallway[amphipod]+1,i):
                if hallway[space] != '.':
                    blocked = True
                    break
            steps += i - desination_hallway[amphipod]

        des_room = desination_hallway[amphipod]
        room_des = -1
        if (rooms[des_room-2] == '.' and rooms[des_room-1] == '.'):
            room_des = desination_hallway[amphipod]-1
            steps += 1

        if (rooms[des_room-2] == amphipod and rooms[des_room-1] == '.'):
            room_des = desination_hallway[amphipod]-2

        if (not blocked) and room_des != -1:
            print("Move from hallway:",amphipod,"From",i,"To",room_des)
            # new_hallway = list(hallway)
            # new_hallway[i] = '.'
            # new_rooms = list(rooms)
            # new_rooms[room_des] = amphipod
            # new_move = move(new_hallway,new_rooms)
            # energy_used += energy_usage(amphipod,steps) + new_move
            # moves.append(energy_used)

            hallway[i] = '.'
            rooms[room_des] = amphipod
            new_move = move(hallway,rooms)
            energy_used += energy_usage(amphipod,steps) + new_move
            moves.append(energy_used)

    if moves:
        return min(moves)
    return 1000000 # no leagal moves

def main():
    hallway = ['.' for _ in range(11)]
    rooms = ['B','A','C','D','B','C','D','A']
    moves = move(hallway,rooms)

    print(moves)

if __name__ == "__main__":
    main()
