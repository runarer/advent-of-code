import sys
import copy
""" Find a path, that is the lowest risk path.
    Find this by a naive algoritm, just choose the lowest risk to the
    left or down. If both equal, look ahead (How?).

    minimum_moves = x*y - 1 # -1 for the start.

    Do a recursive search from the start. Kill a path if it risk gets higher
    than lowest_risk - (minimum_moves - moves_made).

    Alternativ:
    Cave map er som to pyramider mot hverandre. Fra bunnen av legg sammen risk slik at
    midten har risk derfra og til bunnen, så benytt samme teknikk som pyramiden i eulor prodj.
    Har løst den før.

"""
def create_risk_map(cave_map):
    def find_risk(max_allowed_risk,row,col,path):
        #print("E",row,col," -> ",max_allowed_risk)
        if row < 0 or col < 0 or row >= cave_width or col >= cave_width:
            #print("E",row,col," -> ",max_allowed_risk)
            return max_risk #Outside of map
        if risk_map[row][col] > 0:
            #print("E",row,col," -> ",max_allowed_risk)
            return risk_map[row][col]
        if (row,col) in path:
            return max_risk
        max_allowed_risk -= cave_map[row][col]
        if max_allowed_risk <= 0:
            #print("E",row,col," -> ",max_allowed_risk)
            return max_risk #Dead end
        if max_allowed_risk < (cave_width-1)*2 - row - col:
            return max_risk
        #Can look around
        path.append((row,col))
        right = find_risk(max_allowed_risk,row,col+1,copy.copy(path))
        max_allowed_risk = min(max_allowed_risk,right)
        down  = find_risk(max_allowed_risk,row+1,col,copy.copy(path))
        max_allowed_risk = min(max_allowed_risk,down)
        up    = find_risk(max_allowed_risk-1,row-1,col,copy.copy(path))
        max_allowed_risk = min(max_allowed_risk,up)
        left  = find_risk(max_allowed_risk-1,row,col-1,copy.copy(path))

        return cave_map[row][col] + min(up,left,down,right)

        #risk_map[row][col] = cave_map[row][col] + min(up,left,down,right)
        #return risk_map[row][col]

    cave_width = len(cave_map)
    max_risk = cave_width*20
    risk_map = [[0 for _ in range(cave_width)] for _ in range(cave_width)]
    risk_map[-1][-1] = cave_map[-1][-1]
    risk_map[-1][-2] = cave_map[-1][-2] + cave_map[-1][-1]
    risk_map[-2][-1] = cave_map[-2][-1] + cave_map[-1][-1]
    risk_map[-2][-2] = cave_map[-2][-2] + min(risk_map[-1][-2],risk_map[-2][-1])

    for i in range(-3,(cave_width+1)*-1,-1):
        #Colum
        #print("-----")
        for j in range(-1,i,-1):
            #print('C',j,i)
            risk_map[j][i] = find_risk(risk_map[j][i+1]+cave_map[j][i],cave_width+j,cave_width+i,[])
        #Row
        for j in range(i,0,1): #FEIL HER (-1,i-1,-1) <- for fra høyre mot venstre
            #print('R',i,j)
            risk_map[i][j] = find_risk(risk_map[i+1][j]+cave_map[i][j],cave_width+i,cave_width+j,[])
    
    # risk_map[-1][-3] = find_risk(risk_map[-1][-2]+cave_map[-1][-3],cave_width-1,cave_width-1-1)
    # risk_map[-2][-3] = find_risk(risk_map[-1][-2]+cave_map[-2][-3],cave_width-2,cave_width-1-2)
    # risk_map[-3][-3] = find_risk(risk_map[-2][-3]+cave_map[-3][-3],cave_width-3,cave_width-1-2)
    # risk_map[-3][-2] = find_risk(risk_map[-2][-2]+cave_map[-3][-2],cave_width-3,cave_width-1-1)
    # risk_map[-3][-1] = find_risk(risk_map[-2][-1]+cave_map[-3][-1],cave_width-3,cave_width-1)

    #Find risk for
    # for col in range():
    #     for row in range():
    #         if risk_map[col][row] > 0:
    #             continue
    #         max_allowed_risk = 0
    #         if col+1 < cave_width:
    #             max_allowed_risk = risk_map[col+1][row]
    #         else:
    #             max_allowed_risk = risk_map[col][row+1]
    #         find_risk(max_allowed_risk,cave_width-1,cave_width-1)

    return risk_map

def find_lowest_risk(cave_map):
    def travel(risk,row,col,path):
        if row == col == cave_width-1:
            return cave_map[row][col]        
        risk += cave_map[row][col]        
        if risk_shortest_path[0][0] - risk <= 0: #allowed_risk = risk_shortest_path[0][0] - risk
            return max_risk
        if risk > max_risk - row - col:
            return max_risk #Dead end
        if (row,col) in path:
            return max_risk #Looping
        #Are we done?
        path.append((row,col))
        risks = []
        if row-1 >= 0:
            risks.append(travel(risk,row-1,col,copy.copy(path))) #is path a copy or refrence
        if col-1 >= 0:
            risks.append(travel(risk,row,col-1,copy.copy(path)))
        if row+1 < cave_width :
            risks.append(travel(risk,row+1,col,copy.copy(path)))
        if col+1 < cave_width:
            risks.append(travel(risk,row,col+1,copy.copy(path)))
        return cave_map[row][col] + min(risks)

    cave_width = len(cave_map)
    max_risk = cave_width*20
    risk_map = create_risk_map(cave_map)
    for row in risk_map:
        print(row)
    risk_shortest_path = find_minimum_moves_path(copy.deepcopy(cave_map))

    return travel(0,0,0,[])-cave_map[0][0]


# def find_lowest_risk(cave_map):
#     def travel(allowed_risk,row,col,path):
#         if row < 0 or col < 0 or row >= cave_width or col >= cave_width:
#             return max_risk #Outside of map
#         allowed_risk -= cave_map[row][col]
#         if allowed_risk < 0:
#             return max_risk #Dead end
#         if (row,col) in path:
#             return max_risk #Looping
#         #Are we done?
#         if row == col == cave_width-1:
#             return cave_map[row][col]
#         path.append((row,col))
#         up    = travel(allowed_risk,row-1,col,copy.copy(path)) #is path a copy or refrence
#         left  = travel(allowed_risk,row,col-1,copy.copy(path))
#         down  = travel(allowed_risk,row+1,col,copy.copy(path))
#         right = travel(allowed_risk,row,col+1,copy.copy(path))
#         return cave_map[row][col] + min(up,left,down,right)

#     cave_width = len(cave_map)
#     max_risk = cave_width*20
#     create_risk_map(cave_map)
#     risk_shortest_path = find_minimum_moves_path(copy.deepcopy(cave_map))

#     return travel(risk_shortest_path[0][0],0,0,[])-cave_map[0][0]

def find_minimum_moves_path(cave_map):

    #Lower pyramide
    for y in range(2,len(cave_map)+1):
        # First
        cave_map[-1][y*-1] += cave_map[-1][(y*-1)+1]
        # Middle
        for i in range(2,y):
            cave_map[-1*i][(y-i+1)*-1] += min(cave_map[-1*i][((y-i)*-1)], cave_map[-1*i+1][(y-i+1)*-1])
        #Last
        cave_map[y*-1][-1] += cave_map[(y*-1)+1][-1]
    # for row in cave_map:
    #     print(row)
    #Upper pyramide.
    #cave_map[0][0] = 0
    for n in range(0,len(cave_map)):
        for i in range(len(cave_map)-n-1):
            #print((2+i+n)*-1,i," - ",(1+i+n)*-1,i," - ",(2+i+n)*-1,(1+i))
            cave_map[(2+i+n)*-1][i] += min(cave_map[(1+i+n)*-1][i],cave_map[(2+i+n)*-1][i+1])
        #print("----------")

    return cave_map

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
    cave_map = [[int(cha) for cha in line.strip()] for line in lines]
    minimum_moves = len(cave_map)+len(cave_map[0])-1
    lowest_risk = find_lowest_risk(cave_map)
    # for row in cave_map:
    #     print(row)

    print(lowest_risk)

if __name__ == "__main__":
    main()
