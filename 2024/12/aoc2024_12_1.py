"""Advent of Code: 2024.12.1"""
import sys

def outline_plot(garden, starting_plot):    
    height = len(garden)
    width = len(garden[0])
    garden_plot = [starting_plot]
    plant = garden[starting_plot[0]][starting_plot[1]]
    visited = set()
    
    fence_sides = 0
    plots = 0

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
        elif row - 1 >= 0:
            if garden[row-1][col] == plant:
                garden_plot.append((row-1,col))
            else:
                fence_sides += 1

        # East
        if col == width-1:
            fence_sides += 1            
        elif col + 1 < width:
            if garden[row][col+1] == plant:
                garden_plot.append((row,col+1))
            else:
                fence_sides += 1
        
        # South
        if row == height-1:
            fence_sides += 1            
        elif row + 1 < height:
            if garden[row+1][col] == plant:
                garden_plot.append((row+1,col))
            else:
                fence_sides += 1

        # West
        if col == 0:
            fence_sides += 1            
        elif col - 1 >= 0:
            if garden[row][col-1] == plant:
                garden_plot.append((row,col-1))
            else:
                fence_sides += 1

    return (visited,fence_sides)

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