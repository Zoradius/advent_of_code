with open("data/day2.txt", "r") as file:
    # file.read reads the text file as a string
    # split separates the string into a list of strings
    # since there is an empty entry at the end we drop it
    data = [item.split(" ") for item in file.read().split("\n")][:-1]
    data = [(item[0], float(item[1])) for item in data]


# Part 1
# This is admittedly convoluted, but copying and pasting the method with only slight variations also seemed 'meh'
# Since Dictionaries in Python, just as lists, are mutable we can store relevant data in a dictionary and manipulate
# them. (Over all converting the string data into indices would have probably been better).
def parse_command(direction, amount, position={"horizontal": None, "depth": None}):
    try:
        # Check to see if we do part 2 i. e. have an 'aim' property
        position["aim"]
    except KeyError:
        # if not do the 'simpler' case
        with_aim = False
        variable = "depth"
    else:
        # if yes do the 'extended' case
        with_aim = True
        variable = "aim"

    if direction == "forward":
        # increase our horizontal position if command is forward
        position["horizontal"] += amount
        if with_aim:
            # update depth according to aim if aim has been given
            position["depth"] += position["aim"] * amount

    elif direction == "down":
        # increase either depth or aim property if command is 'down'
        position[variable] += amount
    elif direction == "up":
        # decrease either depth or aim property if command is 'up'
        position[variable] -= amount
    else:
        # just to be safe
        raise ValueError("Direction variable not understood")


pos_1 = {"horizontal": 0, "depth": 0}
for point in data:
    parse_command(*point, position=pos_1)

result_part_1 = pos_1["horizontal"] * pos_1["depth"]
print(f"The solution to part one is: {result_part_1}")

# Part 2

pos_2 = {"horizontal": 0, "depth": 0, "aim": 0}
for point in data:
    parse_command(*point, position=pos_2)

result_part_2 = pos_2["horizontal"] * pos_2["depth"]
print(f"The solution to part two is: {result_part_2}")
