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
    new_marks = np.zeros(all_boards.shape, dtype=bool)

    new_marks[indices] = all_boards[indices] == draw
    all_marks = np.logical_or(new_marks, prev_marks)

    return all_marks


def check_bingo(all_marks, indices):
    bingo = False
    index = []

    for axis in [1, 0]:
        for i in indices:
            board = all_marks[i]
            full_row_or_column = np.sum(board, axis=axis)
            bingo = 5 in full_row_or_column
            if bingo:
                index.append(i)

    return index


# Since this solves both part one and part two it shall be the only bit executed (the version which only solvers part
# one is appended as a comment string
remaining_indices = np.arange(0, boards.shape[0])
bingo_results = {"numbers_drawn": [], "bingo_indices": []}
board_marks = np.zeros(boards.shape, dtype=bool)

for number in draws:
    board_marks = mark_number(number, board_marks, boards, remaining_indices)
    index = check_bingo(board_marks, remaining_indices)
    if len(index) > 0:
        bingo_results["numbers_drawn"].append(number)
        bingo_results["bingo_indices"].append(index)

        for i in index:
            remaining_indices = np.delete(remaining_indices, np.where(remaining_indices == i))
        continue
    if len(remaining_indices) == 0:
        break

for j, part in zip([0, -1], ["one", "two"]):
    bingo_index = bingo_results["bingo_indices"][j]
    bingo_board = boards[bingo_index]
    bingo_marks = board_marks[bingo_index]
    sum_not_marked = np.sum(bingo_board[np.invert(bingo_marks)])
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