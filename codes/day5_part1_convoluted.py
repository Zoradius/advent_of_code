import numpy as np

# This is my first attempt at solving part one of day 5, which does work but felt too convoluted to name my final draft.
# Feel free to ignore this or take a look at it if you're inclined I'm not your boss or the police. But be aware that
# it's not commented.

with open("data/day5.txt", "r") as file:
    # file.read reads the text file as a string
    # split separates the string into a list of strings
    # since there is an empty entry at the end we drop it
    data = file.read().split("\n")[:-1]
    data = [line.split(" -> ") for line in data]
    data = [[point.split(",") for point in line] for line in data]
    data = np.array(data, dtype=int)

x_min, x_max = np.min(data[:, :, 0]), np.max(data[:, :, 0])
x_range = (x_max - x_min) + 1

y_min, y_max = np.min(data[:, :, 1]), np.max(data[:, :, 1])
y_range = (y_max - y_min) + 1

xy_range = max(x_range, y_range)
xy_min = min(x_min, y_min)

grid = np.zeros((xy_range, xy_range))


def get_index(x_y):
    return x_y - xy_min


def draw_line(line, mesh):
    # check if line is horizontal or vertical
    is_vertical = line[0][0] == line[1][0]
    is_horizontal = line[0][1] == line[1][1]

    if is_horizontal is is_vertical:
        return mesh

    if is_vertical:
        mesh_copy = mesh
    elif is_horizontal:
        mesh_copy = mesh.T

    stat = line[0][int(is_horizontal)]
    vars = [line[i][int(is_vertical)] for i in range(line.shape[0])]
    stat_index = get_index(stat)
    var_indices = [get_index(var) for var in vars]

    mesh_copy[stat_index, np.arange(np.min(var_indices), np.max(var_indices)+1)] += 1

    if is_horizontal:
        print("hor", line)
        return mesh_copy.T
    elif is_vertical:
        print("ver", line)
        return mesh_copy


for line in data:
    grid = draw_line(line, grid)


n_larger_two = np.sum(grid >= 2)

print(f"Solution for part 1 is: {n_larger_two}")

"""
plt.imshow(grid.T, origin="lower")
intersec = np.argwhere(grid>=2)
plt.scatter(intersec[:,0], intersec[:,1])
"""

