"""
    Som forventet må man jobbe med blokker og ikke dict/list.

    Jeg lagrer kun blokker som er "på" i en liste. Denne oppdateres underveis.
    Side gange side gange side vil gi antall på i denne blokken og summering av dette vil gi svaret.

    Nye blokker kan ovelappe delvis, helt eller ikke i det hele tatt. Når det er fullstendig
    overlapp så slettes blokkene som overlappes. og ved ingen overlapp så går man vidre til neste.

    Når det er delvis overlapp så skal det lages nye blokker og de ulike situasjonene er:
    1. Fullstendig overlapp på en side. -> Gjør den gamle blokken mindre.
    2. Delvis overlapp på en side. -> Gjør den gamle blokken mindre og lag en ny.
    3. Delvis overlapp på et hjørne. -> Gjør den gamle blokken mindre og lag to nye.
    4. Splitting av en side. -> Gjør den gamle blokken mindre og lag to nye.
    5. Delvis splitting av en side. -> Gjør den gamle blokken mindre og lag tre nye.
    6. Deling i to. -> 2 nye blokker.
    7. Hull i midten. -> 6 nye blokker.
    8. Uthulling. -> 4 nye blokker.
    9. Delvis uthulling. -> 5 nye blokker
    10. Total overlapp. -> slett gammel

    Hvordan finner jeg ut hvilken gruppe en overlapp er i?
    6. (ox1 < nx1 < ox2) and (ox1 < nx2 < ox2) and (ny1 < oy1 and ny2 > oy2) and (nz1 < oz1 and nz2 > oz2) # for splitt langs x-akse
       (oy1 < ny1 < oy2) and (oy1 < ny2 < oy2) and (nx1 < ox1 and nx2 > ox2) and (nz1 < oz1 and nz2 > oz2) # for splitt langs y-akse
       (oz1 < nz1 < oz2) and (oz1 < nz2 < oz2) and (nx1 < ox1 and nx2 > ox2) and (ny1 < oy1 and ny2 > oy2) # for splitt langs z-akse
    Hvordan teste dette. Må lage test filer.

    Hvordan regne ut nye blokker?
"""
import sys, re

def run_instuctions(instructions):
    reactor = [instructions[0][1]]

    for inst,(new_block) in instructions[1:]:
        new_blocks = []
        remove_blocks = []
        do_not_add = False
        
        for old_block in reactor:
            nx1,nx2,ny1,ny2,nz1,nz2 = new_block
            ox1,ox2,oy1,oy2,oz1,oz2 = old_block

            # Check for no overlap, Tested.
            if nx1 > ox2 or nx2 < ox1 or ny1 > oy2 or ny2 < oy1 or nz1 > oz2 or nz2 < oz1:
                continue

            # 10. Total overlap, tested and ok
            if nx1 <= ox1 and ny1 <= oy1 and nz1 <= oz1 and \
               nx2 >= ox2 and ny2 >= oy2 and nz2 >= oz2:
                #print("Total overlap")
                remove_blocks.append(old_block)
                continue

            # 7. Hole in the middle
            if ox1 <= nx1 <= ox2 and oy1 <= ny1 <= oy2 and oz1 <= nz1 <= oz2 \
               and ox1 <= nx2 <= ox2 and oy1 <= ny2 <= oy2 and oz1 <= nz2 <= oz2:
                if inst == "on":
                    # Pointless hole
                    do_not_add = True
                    break

            # Remove stuff outside of overlap, Makes new blocks right side.
            if nx1 < ox1: nx1 = ox1
            if nx2 > ox2: nx2 = ox2
            if ny1 < oy1: ny1 = oy1
            if ny2 > oy2: ny2 = oy2
            if nz1 < oz1: nz1 = oz1
            if nz2 > oz2: nz2 = oz2

            # Create 6 new blocks
            if ox1 < nx1:
                left_block = (ox1,nx1-1,oy1,oy2,oz1,oz2)
                new_blocks.append(left_block)

            if ox2 > nx2:
                right_block = (nx2+1,ox2,oy1,oy2,oz1,oz2)
                new_blocks.append(right_block)

            if oz1 < nz1:
                bottom_block = (nx1,nx2,oy1,oy2,oz1,nz1-1)
                new_blocks.append(bottom_block)

            if oz2 > nz2:
                top_block = (nx1,nx2,oy1,oy2,nz2+1,oz2)
                new_blocks.append(top_block)

            if oy1 < ny1:
                side_down_block = (nx1,nx2,oy1,ny1-1,nz1,nz2)
                new_blocks.append(side_down_block)

            if oy2 > ny2:
                side_top_block = (nx1,nx2,ny2+1,oy2,nz1,nz2)
                new_blocks.append(side_top_block)

            # Remove old block
            remove_blocks.append(old_block)

        # remove blocks in remove_blocks from reactor
        for block in remove_blocks:
            reactor.remove(block)

        # add new_blocks to reactor
        reactor += new_blocks

        if do_not_add or inst == "off":
            continue
        reactor.append(new_block)

    return reactor

def create_instructions(lines):
    instructions = []

    for line in lines:
        matches = re.match(r"(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)",line)
        instruction = (matches[1], \
                        (int(matches[2]),int(matches[3]), \
                        int(matches[4]),int(matches[5]), \
                        int(matches[6]),int(matches[7]))  \
                      )
        instructions.append(instruction)

    return instructions

def find_total_on(blocks):
    total_on = 0
    for x1,x2,y1,y2,z1,z2 in blocks:
        total_on += ((x2-x1)+1)*((y2-y1)+1)*((z2-z1)+1)
    return total_on

def main():
    """Start"""
    #get argument
    if len(sys.argv) < 1:
        sys.exit("Usage: python " + sys.argv[0] + " filename")
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except IOError as err:
        print("{}\nError opening {}. Terminating program.".format(err, filename), file=sys.stderr)
        sys.exit(1)

    instructions = create_instructions(lines)
    reactor = run_instuctions(instructions)
    total_on = find_total_on(reactor)
    print(total_on)

if __name__ == "__main__":
    main()
