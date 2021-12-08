import numpy as np

with open("data/day4.txt", "r") as file:
    # file.read reads the text file as a string
    # split separates the string into a list of strings
    # since there is an empty entry at the end we drop it
    data = file.read().split("\n")[:-1]
    draws = np.array(data[0])

    boards = data[1:]

    # Now we create a 2D array of shape (Number of digits, number of entries). `list()` takes a string and converts it
    # into a list of characters, we save these as integer types in a numpy array and transpose for the above shape.
    data = np.array([list(item) for item in data], dtype=int).T