from project import check_row, check_column, check_box

puzzle = [
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

def test_check_row():
    assert check_row(puzzle, 1, (0, 3)) == False
    assert check_row(puzzle, 1, (1, 3)) == True
    assert check_row(puzzle, 9, (1, 1)) == True
    assert check_row(puzzle, 8, (0, 5)) == True


def test_check_column():
    assert check_column(puzzle, 9, (1, 1)) == False
    assert check_column(puzzle, 5, (1,1)) == True
    assert check_column(puzzle, 7, (2, 1)) == True
    assert check_column(puzzle, 8, (0, 5)) == True


def test_check_box():
    assert check_box(puzzle, 1, (1, 1)) == False
    assert check_box(puzzle, 4, (2, 2)) == True
    assert check_box(puzzle, 9, (8, 8)) == False
    assert check_box(puzzle, 3, (8, 0)) == False
    assert check_box(puzzle, 3, (1, 6)) == True
    assert check_box(puzzle, 7, (8, 8)) == True
    assert check_box(puzzle, 7, (3, 3)) == False
    assert check_box(puzzle, 3, (3, 3)) == True