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
    boards = [[list(filter(lambda a: a != '', item)) for item in board] for board in boards]
    boards = np.array(boards, dtype=int)


def mark_number(draw, prev_marks, all_boards):
    new_marks = all_boards == draw
    all_marks = np.logical_or(new_marks, prev_marks)
    return all_marks


def check_bingo(all_marks):
    bingo = False
    index = None

    direction = {"rows": np.zeros(all_marks.shape, dtype=bool), "columns": np.zeros(all_marks.shape, dtype=bool)}

    for axis, across in zip([1, 0], ["rows", "columns"]):
        for i, board in enumerate(all_marks):
            full_row_or_column = np.sum(board, axis=axis)
            bingo = 5 in full_row_or_column
            if bingo:
                index = i
                break
        if bingo:
            break
    return index


board_marks = np.zeros(boards.shape, dtype=bool)  # to keep track of which fields are marked
final_number = None

for number in draws:
    board_marks = mark_number(number, board_marks, boards)
    index = check_bingo(board_marks)
    if index is not None:
        final_number = number  # in principle one could just use the number variable outside the loop
        break

print(f"Bingo is at: {index}")
sum_not_marked = np.sum(boards[index][np.invert(board_marks[index])])
result_part_one = sum_not_marked * final_number
print(f"The solution for part one is: {result_part_one}")
