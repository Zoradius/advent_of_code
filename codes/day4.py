import numpy as np

with open("data/day4.txt", "r") as file:
    # file.read reads the text file as a string
    # split separates the string into a list of strings
    # since there is an empty entry at the end we drop it
    data = file.read().split("\n")[:-1]
    draws = np.array(data[0].split(","), dtype=int)

    # The following would have probably been easier using pandas but whatever
    boards = np.array(data[1:])
    # Count how many boards there are by counting their dividers
    counts = np.sum(boards == '')
    # Split up every board with their divider at the front
    boards = np.array(np.split(boards, counts))
    # drop all the dividers
    boards = np.delete(boards, 0, 1)
    # convert strings into lists
    boards = [[item.split(" ") for item in board] for board in boards]
    # get rid of those pesky little extra spaces
    boards = [[list(filter(lambda a: a != '', row)) for row in board] for board in boards]
    boards = np.array(boards, dtype=int)


def mark_number(draw, prev_marks, all_boards, indices):
    # This method takes a drawn number `draw`, a boolean array with marks `prev_marks`, all board states `all_boards`
    # and a list of indices of boards that haven't bingo'd yet and updates all the markings on the boards that are still
    # in the running
    # Initialize new markings with no new markings
    new_marks = np.zeros(all_boards.shape, dtype=bool)

    # everywhere where the number on the board equals the drawn number we want to place a new mark
    new_marks[indices] = all_boards[indices] == draw
    # the final markings are either previous markings or new ones
    all_marks = np.logical_or(new_marks, prev_marks)

    return all_marks


def check_bingo(all_marks, indices):
    # this method takes an array of all markings, and an array of indices of boards that still haven't bingo'd yet and
    # returns a list of the new boards that have bingo'd
    bingo = False  # Technically useless
    index = []  # Save indices as a list

    for axis in [1, 0]:  # for rows and columns on a board respectively
        for i in indices:  # for all boards that are still in the running
            board = all_marks[i]  # get current board from list of all boards
            # (^we are a bit inconsistent in not passing this as an input ^)
            full_row_or_column = np.sum(board, axis=axis)  # get the number of markings along all rows/columns
            # a bingo is achieved when the maximum number of markings are in a row/column (here we assume the board to
            # be squared, i. e. n x n, here with n = 5)
            bingo = len(full_row_or_column) in full_row_or_column
            if bingo:
                # Append the index that bingo'd (in a first iteration for part one I would have quit here)
                index.append(i)

    return index


# Since this solves both part one and part two it shall be the only bit executed (the version which only solvers part
# one is appended as a comment string
# Save an array of indices to keep track of which boards haven't bingo'd yet
remaining_indices = np.arange(0, boards.shape[0])
# Save the numbers which were drawn when one or multiple bingos occured and the corresponging indices in a dictionary
bingo_results = {"numbers_drawn": [], "bingo_indices": []}
# Initialize empty markings
board_marks = np.zeros(boards.shape, dtype=bool)

for number in draws:  # for every number that is drawn
    # update the markings on the remaining boards
    board_marks = mark_number(number, board_marks, boards, remaining_indices)
    # check if any remaining boards have bingo'd
    bingo_indices = check_bingo(board_marks, remaining_indices)
    if len(bingo_indices) > 0:  # if yes
        # save the output for later
        bingo_results["numbers_drawn"].append(number)
        bingo_results["bingo_indices"].append(bingo_indices)

        # remove the indices of the bingo'd boards from the remaining indices
        remaining_indices = np.delete(remaining_indices, np.where(np.in1d(remaining_indices, bingo_indices))[0])
        continue

    if len(remaining_indices) == 0:
        # this doesn't really happend, but in case there are no more boards left in the game we quit
        break

for j, part in zip([0, -1], ["one", "two"]):
    # This just saves me copying and pasting the same calculation of the result
    # Get the first/last index of all the boards that bingo'd
    bingo_index = bingo_results["bingo_indices"][j]
    # Get the corresponding board numbers and markings
    bingo_board = boards[bingo_index]
    bingo_marks = board_marks[bingo_index]
    # sum over all the non-marked values
    sum_not_marked = np.sum(bingo_board[np.invert(bingo_marks)])
    # multiply with the number that was drawn at the time for result
    result = bingo_results["numbers_drawn"][j] * sum_not_marked
    print("The solution for part " + part + f" is : {result}")


"""
Solution for only part one:
Note that at the time of writing this bit indices where untracked and the corresponding functions did not take a list of
indices. This code however is compatible with the new functions and use an otherwise useless complete list of indices

board_marks_a = np.zeros(boards.shape, dtype=bool)  # to keep track of which fields are marked
final_number_a = None
indices_a = np.arange(boards.shape[0])
for number in draws:
    board_marks_a = mark_number(number, board_marks_a, boards, indices_a)
    index = check_bingo(board_marks_a, indices_a)
    if index is not None:
        final_number = number  # in principle one could just use the number variable outside the loop
        break

print(f"Bingo is at: {index}")
sum_not_marked = np.sum(boards[index][np.invert(board_marks[index])])
result_part_one = sum_not_marked * final_number
print(f"The solution for part one is: {result_part_one}")
"""