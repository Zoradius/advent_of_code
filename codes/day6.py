import numpy as np

with open("data/day6.txt", "r") as file:
    # file.read reads the text file as a string
    # split separates the string into a list of strings
    # since there is an empty entry at the end we drop it
    data = file.read().split("\n")[:-1]
    # Split the strings into the "from" and "to" parts
    data = data[0].split(",")
    data = np.array(data, dtype=int)


def update_lanternfish(state):
    new_state = state
    zeros = np.argwhere(new_state == 0)
    new_state = np.append(new_state, [8 for zero in zeros])
    new_state[:-len(zeros)+int(len(zeros) == 0)*len(new_state)] -= 1
    new_state[zeros] = 6

    return new_state


def simulate_days(n_days, initial_state):
    state = initial_state
    # tape = [state]

    for day in range(n_days):
        state = update_lanternfish(state)
        # tape.append(state)
    return state  # tape


result_part_one = simulate_days(80, data)
# result_part_two = simulate_days(256, np.array([3, 4, 3, 1, 2]))
print(f"The result of part one is: {len(result_part_one)}")
result_part_two = simulate_days(256, data)
print(f"The result of part one is: {len(result_part_two)}")