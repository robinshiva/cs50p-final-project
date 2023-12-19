import sys
import math

# Test puzzle with a solution
puzzle1 = [
            [1, 9, 0, 0, 0, 0, 0, 0, 0],
            [5, 0, 0, 0, 0, 0, 0, 0, 0],
            [7, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 5, 0, 0, 6, 0, 7, 2],
            [0, 6, 1, 8, 7, 0, 0, 4, 0],
            [0, 8, 7, 2, 0, 0, 0, 1, 5],
            [3, 0, 2, 6, 0, 0, 0, 0, 9],
            [0, 0, 4, 0, 0, 0, 3, 8, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0],
        ]

# Test puzzle without a solution
puzzle2 = [
            [1, 7, 0, 1, 0, 0, 0, 0, 0],
            [5, 0, 0, 0, 0, 0, 0, 0, 0],
            [7, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 5, 0, 0, 6, 0, 7, 2],
            [0, 6, 1, 8, 7, 0, 0, 4, 0],
            [0, 8, 7, 2, 0, 0, 0, 1, 5],
            [3, 0, 2, 6, 0, 0, 0, 0, 9],
            [0, 0, 4, 0, 0, 0, 3, 8, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0],
        ]

# Test puzzle with 3x2 boxes
puzzle3 = [
    [0, 0, 0, 0, 0, 0],
    [0, 3, 6, 4, 2, 0],
    [0, 5, 0, 0, 1, 0],
    [0, 4, 0, 0, 6, 0],
    [0, 1, 5, 2, 3, 0],
    [0, 0, 0, 0, 0, 0],        
]


def main(puzzle):
    total_numbers = len(puzzle[0]) * len(puzzle)
    solution = True

    # Check puzzle's size
    puzzle_size = len(puzzle)
    for i in range(puzzle_size):
        if puzzle_size != len(puzzle[i]):
            print("Sudoku board is not a square.")
            sys.exit(1)

    # My own backtracking algorithm
    i = 0
    while i < total_numbers:
        # Go through the squares from left to right, top to bottom
        
        row_num = i // len(puzzle)
        column_num = i % len(puzzle)

        # If the number is already set by the puzzle, skip it
        if puzzle[row_num][column_num] > 0:
            i += 1

        else:
            # Set number to whatever was in the square before minus 1,
            # using negative values to differentiate between the given numbers and the possible solutions
            number = puzzle[row_num][column_num] - 1
            puzzle[row_num][column_num] = 0

            # Check if the number could be correct, otherwise decrease by 1
            while not check_number(puzzle, number, (row_num, column_num)) and number > (puzzle_size * -1):
                number -= 1

            # If the smallest possible number (usually -9) does not work or it was already at the smallest number before, set the square to 0
            # and backtrack one or more squares until another changeable square is found
            if number == (puzzle_size * -1) and not check_number(puzzle, number, (row_num, column_num)) or number < (puzzle_size * -1):
                puzzle[row_num][column_num] = 0
                i -= 1
                while puzzle[i // len(puzzle)][i % len(puzzle[0])] > 0:
                    i -= 1
                
            # If the number works as a solution for now, write it in the square and go to the next one
            else:
                puzzle[row_num][column_num] = number
                i += 1

        # If the algorithm backtracks further than the first square, there is no possible solution
        if i < 0:
            solution = False
            print("Could not find a solution.")
            break
                
    # Print the solution with absolute values instead of negative ones
    if solution:
        puzzle_abs_values = []
        for row_num in puzzle:
            puzzle_abs_values.append([abs(num) for num in row_num])
        print(puzzle_abs_values)


def check_number(puzzle, number, position):
    """Checks if a given number at a given position is a possible solution for a given puzzle, otherwise returns 'False'"""
    return check_row(puzzle, number, position) and check_column(puzzle, number, position) and check_box(puzzle, number, position)


def check_row(puzzle, number, position):
    """Checks if a given number is already in a row and returns 'False' if so"""
    if abs(number) in [abs(num) for num in puzzle[position[0]]]:
        return False
    return True


def check_column(puzzle, number, position):
    """Checks if a given number is already in a column and returns 'False' if so"""
    column_numbers = []
    for row in puzzle:
        column_numbers.append(abs(row[position[1]]))
    if abs(number) in column_numbers:
        return False
    return True


def check_box(puzzle, number, position):
    """Checks if a given number is already in a box and returns 'False' if so"""
    box_numbers = []

    # Change the horizontal_box_size manually for non-square boxes
    horizontal_box_size = int(math.sqrt(len(puzzle)))
    # horizontal_box_size = 3
    vertical_box_size = int(len(puzzle) / horizontal_box_size)
    
    # Find the first row and column of the box in which the given number is in
    row_num_start = (position[0] // vertical_box_size) * vertical_box_size
    column_num_start = (position[1] // horizontal_box_size) * horizontal_box_size

    # Get all the numbers inside the box
    for i in range(vertical_box_size):
        row = puzzle[row_num_start + i]
        for j in range(horizontal_box_size):
            box_numbers.append(abs(row[column_num_start + j]))
    if abs(number) in box_numbers:
        return False
    return True


if __name__ == "__main__":
    main(puzzle1)
