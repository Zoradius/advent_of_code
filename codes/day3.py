import numpy as np

with open("data/day3.txt", "r") as file:
    # file.read reads the text file as a string
    # split separates the string into a list of strings
    # since there is an empty entry at the end we drop it
    data = file.read().split("\n")[:-1]
    # Now we create a 2D array of shape (Number of digits, number of entries). `list()` takes a string and converts it
    # into a list of characters, we save these as integer types in a numpy array and transpose for the above shape.
    data = np.array([list(item) for item in data], dtype=int).T


def get_rate(arr, which="gamma"):
    # This method gets either the gamma or epsilon via the keyword argument `which`, since the only difference between
    # the two is whether we take the most or least common numeral for the corresponding digit.
    rate = []
    if which == "gamma":
        signum = 1
    elif which == "epsilon":
        signum = -1
    else:
        raise ValueError("Raty Type not understood")

    for digits in arr:
        # For every digit we count the number of ones by summing over all entries for the current digit.
        n_ones = np.sum(digits)
        # We compare this to the overall number of entries, and change the sign depending on which rate we calculate.
        diff = signum * (n_ones - arr.shape[1] / 2)
        if diff > 0:
            # if there are more/fewer (gamma/epsilon) than half of all entries ones then append a one to the result
            rate.append("1")
        else:
            # if there are fewer/more (gamma/epsilon) than half of all entries zeros then append a zero to the result
            rate.append("0")
        # Note that there was no description on how to handle a case `diff == 0`.
    return rate


# Get both rates from the entire data set
gamma_rate = get_rate(data, which="gamma")
epsilon_rate = get_rate(data, which="epsilon")

# Convert the list of characters to a string and then from binary to decimal
gamma_rate_decimal = int("".join(gamma_rate), 2)
epsilon_rate_decimal = int("".join(epsilon_rate), 2)
# Multiply both decimal representations for result
result_part_1 = gamma_rate_decimal * epsilon_rate_decimal
print(f"The result for part one is: {result_part_1}")


def bit_criteria(arr, i, which="oxygen"):
    # This function gives the bit criteria for a given digit place `i` and an (sub-)dataset arr. Again the keyword
    # `which` handles whether most or least common digits are used. Here we we keep only entries with the most/least
    # common i-th digit.
    if which == "oxygen":
        signum = 1
    elif which == "co2_scrubber":
        signum = -1
    else:
        raise ValueError("Bit criteria type not understood")

    current_digits = arr[i]  # list of all entries for the current digit
    n_ones = np.sum(current_digits)  # number of ones for current digit
    # difference between number of ones and half of the total number of entries:
    diff = signum * (n_ones - arr.shape[1] / 2)

    if diff > 0:
        return arr[:, arr[i] == 1]  # If most/least (oxygen/co2_scrubber) common digit is one, keep all those entries
    elif diff == 0:
        # if both zeros and ones are equally common keep those entries with a one (oxygen) or a zero (co2_scrubber) at
        # i-th place
        return arr[:, arr[i] == int(signum > 0)]
    else:
        # if least/most (oxygen/co2_scubber) common digit is zero, keep all those entries
        return arr[:, arr[i] == 0]


# Dictionary to save outputs
results = {}
# Iterate in parallel over the functional arguments, in both cases we input the whole data set, but with different key-
# word arguments
for work_array, flag in zip([data, data], ["oxygen", "co2_scrubber"]):
    for digit in range(work_array.shape[0]):
        # evaluate the bit criteria for every digit and set the output to be the new input for the next iteration
        work_array = bit_criteria(work_array, digit, which=flag)
        # If only one element remains we quit and move on
        if work_array.shape[1] == 1:
            # save output to dictionary; the transposing only gets rid of a superfluous dimension, `flatten()` would
            # have worked just the same
            results[flag] = work_array.T
            break

# Again we convert the resulting binary to decimal, only that we here have to convert the list of integers first to a
# list of characters and then into a string into a decimal integer number
oxygen_rating_decimal = int("".join([str(item) for item in results["oxygen"][0]]), 2)
co2_scrubber_rating_decimal = int("".join([str(item) for item in results["co2_scrubber"][0]]), 2)
# Multiply for final result
result_part_2 = oxygen_rating_decimal * co2_scrubber_rating_decimal
print(f"The result for part two is: {result_part_2}")
