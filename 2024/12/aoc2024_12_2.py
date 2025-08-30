"""Advent of Code: 2024.12.2
    When finding fence sides, I can save all corners of each fence side. 
    Then I can start on the most top left corner and walk in one direction around while counting 
    turns and mark each plot corner as visited. If I return to a visited and there are more corners
    left, there's one or more inner fences. Repeat the process for these corners.
"""
import sys

def combine_fences(fence_parts):
    fence_sides = []
    cur_row, cur_start, cur_stop = fence_parts[0]
    
    for fence_part in fence_parts[1:]:
        next_row, next_start, next_stop = fence_part

        if cur_row == next_row and cur_stop == next_start:
            cur_stop = next_stop
        else:
            fence_sides.append((cur_row,cur_start,cur_stop))
            cur_row, cur_start, cur_stop = fence_part
    fence_sides.append((cur_row,cur_start,cur_stop))
    
    return fence_sides


def outline_plot(garden, starting_plot):    
    height = len(garden)
    width = len(garden[0])
    garden_plot = [starting_plot]
    plant = garden[starting_plot[0]][starting_plot[1]]
    visited = set()
    
    fence_sides = 0
    plots = 0

    # Dette kan reduseres

    north_fences = []
    east_fences = []
    south_fences = []
    west_fences = []
    
    while garden_plot:
        plot = garden_plot.pop(0)
        if plot in visited:
            continue
        row,col = plot
        visited.add(plot)
        plots += 1

        # North
        if row == 0:
            fence_sides += 1
            north_fences.append((row,col,col+1))
        elif row - 1 >= 0:
            if garden[row-1][col] == plant:
                garden_plot.append((row-1,col))
            else:                
                fence_sides += 1
                north_fences.append((row,col,col+1))

        # East
        if col == width-1:
            fence_sides += 1
            east_fences.append((col+1,row,row+1))
        elif col + 1 < width:
            if garden[row][col+1] == plant:
                garden_plot.append((row,col+1))
            else:
                east_fences.append((col+1,row,row+1))
                fence_sides += 1
        
        # South
        if row == height-1:
            fence_sides += 1
            south_fences.append((row+1,col,col+1))
        elif row + 1 < height:
            if garden[row+1][col] == plant:
                garden_plot.append((row+1,col))
            else:
                south_fences.append((row+1,col,col+1))
                fence_sides += 1

        # West
        if col == 0:
            fence_sides += 1
            west_fences.append((col,row,row+1))
        elif col - 1 >= 0:
            if garden[row][col-1] == plant:
                garden_plot.append((row,col-1))
            else:
                west_fences.append((col,row,row+1))
                fence_sides += 1

    north_fences.sort()
    east_fences.sort()
    south_fences.sort()
    west_fences.sort()

    north_fences = combine_fences(north_fences)
    east_fences = combine_fences(east_fences)
    south_fences = combine_fences(south_fences)
    west_fences = combine_fences(west_fences)

    return (visited,len(north_fences)+len(east_fences)+len(south_fences)+len(west_fences))

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

    # Do stuff with lines
    garden_map = [ [plot for plot in plots.strip()] for plots in lines]
    grouped_plots = [ [False for _ in row] for row in garden_map]

    total_price = 0

    for row,line in enumerate(garden_map):
        for col, plot in enumerate(line):
            if not grouped_plots[row][col]:
                plots, fence_sides = outline_plot(garden_map,(row,col))
                for i,j in plots:
                    grouped_plots[i][j] = True
                total_price += len(plots)*fence_sides
    print(total_price)


if __name__ == "__main__":
    main()