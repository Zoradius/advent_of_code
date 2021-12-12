import numpy as np

# This is my second draft of day 5. It sacrifices some generality for understandability although I am sure the main
# method can be made more efficient than this. But hey it works.

with open("data/day5.txt", "r") as file:
    # file.read reads the text file as a string
    # split separates the string into a list of strings
    # since there is an empty entry at the end we drop it
    data = file.read().split("\n")[:-1]
    # Split the strings into the "from" and "to" parts
    data = [line.split(" -> ") for line in data]
    # Split the x and y coordinates
    data = [[point.split(",") for point in line] for line in data]
    # Convert to array of shape (# Points, 2, 2) since we have two coordinates for two points
    data = np.array(data, dtype=int)


# This part sacrifices generality. I would normally recommend treating the coordinates as spatial coordinates (instead
# of indices) and then mapping to a uniformly indexed (square or rectengular) mesh, then one needs to map the
# coordinates to their respective index, but since the data here clearly ranges from 0 to 1000 with borders of unit 10
# we just initialize a 1 to 1 representation meaning the coordinates equal their index.
data_range = np.max(data) - np.min(data)  # Read the range of the coordinate values

grid_part_one = np.zeros((data_range+20, data_range+20))  # Initialize a mesh to write lines into
grid_part_two = np.zeros((data_range+20, data_range+20))  # also for part two


def draw_line(line, mesh, part_two):
    # This function takes a line of shape (2, 2) containing two coordinates of two points and adds a one to each space
    # in a mesh array covered by the line as it is described in the problem description. (part_two is a boolean value
    # that activates the sub-routines for part two of the problem.)
    # Read coordinate values
    x1, x2 = line[0][0], line[1][0]
    y1, y2 = line[0][1], line[1][1]

    # If the line is vertical
    if x1 == x2 and not(y1 == y2):
        # Since numpy's range function only works for increasing ranges, we need to know which value constitutes our
        # lower and upper bound of the value range.
        low = min(y1, y2)
        up = max(y1, y2)
        # add ones to all y values in the vertical direction, here we add one to the upper bound since the problem
        # includes the final space to be covered but numpy's range function excludes the final value. This follows for
        # all other index ranges we define from here on out.
        mesh[x1, np.arange(low, up+1)] += 1
        return mesh
    # if the line is horizontal
    elif y1 == y2 and not(x1 == x2):
        low = min(x1, x2)
        up = max(x1, x2)
        # add ones to all x values in the horizontal direction
        mesh[np.arange(low, up+1), y1] += 1
        return mesh
    # if line isn't a line but actually a point
    elif x1 == x2 == y1 == y2:
        # add a one to that point (this case does not occur for my piece of data)
        mesh[x1, y2] += 1
    # if the line is a 45 degrees diagonal line (this part could probably be made more efficient)
    elif (np.abs(x2 - x1) == np.abs(y2 - y1)) and part_two:
        # Again we define our possible value ranges via numpy and the respective extremum
        x_low, x_max = min(x1, x2), max(x1, x2)
        y_low, y_max = min(y1, y2), max(y1, y2)
        x_range = np.arange(x_low, x_max+1)
        y_range = np.arange(y_low, y_max+1)

        # If the initial point lies to the left of the end point
        if x1 < x2:
            # and the end point lies above our initial point
            if y2 > y1:
                # use the ranges as is
                x = x_range
                y = y_range
            # and the end point lies below our initial point
            elif y2 < y1:
                x = x_range  # keep the x values
                y = np.flip(y_range)  # reverse the y values
        # if the initial point lies to the right of the final point
        elif x1 > x2:
            # and the final point lies above out initial point
            if y1 < y2:
                # reverse only the x range
                x = np.flip(x_range)
                y = y_range
                # and the final point lies below out initial point
            elif y1 > y2:
                # reverse both value ranges
                x = np.flip(x_range)
                y = np.flip(y_range)

        # add ones at each space according to the value ranges
        mesh[x, y] += 1
        return mesh
    else:
        return mesh


# draw lines for each line in the data set
for line in data:
    draw_line(line, grid_part_one, False)  # for part one without diagonals
    draw_line(line, grid_part_two, True)  # for part two with diagonals

# The solutions are then given by the number of points covered by two or more lines
print(f"The solution for part one is: {np.sum(grid_part_one >= 2)}")
print(f"The solution for part two is: {np.sum(grid_part_two >= 2)}")
