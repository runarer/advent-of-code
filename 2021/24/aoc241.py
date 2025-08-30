import sys, math

def create_instructions(lines):
    instructions = []

    for line in lines:
        inst = None
        var1 = None
        var2 = None

        if "inp" in line:
            inst, var1 = line.strip().split()
        else:
            inst, var1, var2 = line.strip().split()
            if var2 not in "wxyz":
                var2 = int(var2)
        instructions.append((inst,var1,var2))

    return instructions

def run_instuctions(instructions,data):
    state = {'w':0,'x':0,'y':0,'z':0}
    data_pointer = 0

    #print(state)
    for inst, var1, var2 in instructions:
        #print(inst,var1,var2)
        if inst == "inp":
            state[var1] = int(data[data_pointer])
            data_pointer += 1

        elif inst == "add":
            if isinstance(var2,int):
                state[var1] += var2
            else:
                state[var1] += state[var2]

        elif inst == "mul":
            if isinstance(var2,int):
                state[var1] = state[var1] * var2
            else:
                state[var1] = state[var1] * state[var2]

        elif inst == "div":
            if isinstance(var2,int):
                if var2 != 0:
                    #state[var1] = int( (state[var1]/var2)+0.5 )
                    state[var1] = int(state[var1]/var2)
            else:
                if state[var2] != 0:
                    #state[var1] = int( (state[var1]/state[var2])+0.5 )
                    state[var1] = int(state[var1]/state[var2])

        elif inst == "mod":
            if isinstance(var2,int):
                if state[var1] < 0 or var2 <= 0:
                    continue
                #state[var1] = state[var1] % var2
                state[var1] = int(math.fmod(state[var1],var2))
            else:
                if state[var1] < 0 or state[var2] <= 0:
                    continue
                #state[var1] = state[var1] % state[var2]
                state[var1] = int(math.fmod(state[var1],state[var2]))

        elif inst == "eql":
            if isinstance(var2,int):
                state[var1] = int( state[var1] == var2 )
            else:
                state[var1] = int(state[var1] == state[var2])

        else:
            print("Instruction Not Found")
        
        #print(inst,var1,var2,state)

    return state

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
    #state = run_instuctions(instructions,"13579246899999")

    # __99__________ er antatt
    # __9979________ er antatt
    # _399799_______ er antatt
    # _399799__96___ er antatt
    # _399799_2969__ er antatt
    # _399799929691_ er antatt
    # 93997999296912 er antatt
    state = run_instuctions(instructions,"93997999296912")
    print(state)

    # Second task
    state = run_instuctions(instructions,"81111379141811")
    print(state)

    

    


if __name__ == "__main__":
    main()
