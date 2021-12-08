import numpy as np

with open("data/day1.txt", "r") as file:
    # file.read reads the text file as a string
    # split separates the string into a list of strings
    # since there is an empty entry at the end we drop it
    data = file.read().split("\n")[:-1]
    # we map all the strings to integer values
    data = list(map(int, data))
    # and convert it to a numpy array
    data = np.array(data)
    # Could all be crammed into one line:
    # data = np.array(list(map(int, file.read().split("\n")[:-1])))


# Part 1
# since we are going to need it again later, define a method to compare consecutive numbers
def compare_consecutive_entries(array):
    shifted_data = np.roll(array, 1)  # Shift array values over by one place
    data_difference = array - shifted_data  # Get the difference between consecutive values
    increased_data = data_difference > 0  # check if difference is positive
    increased_count = np.sum(increased_data[1:])  # sum over the truth values (numpy treads true as 1 and false as 0)
    # Note that since numpy.roll is cyclical we drop the first entry before we sum since that compares the first to
    # the last entry. Here it does not make a difference since the last value is larger than the first and therefore
    # isn't counted anyways

    # Again this could be crammed into one line:
    # increased_coun = np.sum(((data - np.roll(data, 1)) > 0)[1:])

    return increased_count


solution_part_1 = compare_consecutive_entries(data)

# Part 2
# Funnily enough, I did use this sliding window stuff a few weeks ago. Turns out the newest numpy version has a build-in
# method for that, but at the time that version wasn't on pip yet. It is now however, so this requires numpy >= 1.20.0
windows = np.lib.stride_tricks.sliding_window_view(data, 3)
summed_windows = np.array(list(map(np.sum, windows)))
solution_part_2 = compare_consecutive_entries(summed_windows)

# Again this can be crammed into one line but alas.
