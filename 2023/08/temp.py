
    #['AAA', 'PRA', 'PVA', 'XLA', 'PTA', 'FBA']
    
    # "AAA" = 13206+1
    # "PRA" = 19950+1
    # "PVA" = 14892+1
    # "XLA" = 12082+1
    # "PTA" = 20512+1
    # "FBA" = 22198+1

    pp = "PVA"
    for s in range(100000):
        #print(pp)
        next_instruction = instructions[steps % nr_inst]
        pp = desert_map[pp][next_instruction]
        if pp[2] == 'Z':
            print(f'{s} {pp}')
        steps += 1

    #while any(pos[2] != 'Z' for pos in positions):
    #    next_instruction = instructions[steps % len(instructions)]
    #    positions = [ desert_map[pos][next_instruction] for pos in positions]
    #    steps += 1

    #print(steps)