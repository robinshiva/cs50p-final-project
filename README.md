# Sudoku Solver
#### Video Demo:  <https://youtu.be/l7j1JWYv4RQ>
#### Description:
I first wrote a Sudoku-app with tkinter as my final project but noticed afterwards that the project structure does not fit the requirements anymore because everything was object-based. So I decided to code an accompanying Sudoku solver that would be simpler in its structure and just use a few functions that can be tested with pytest.
## How to use
Simply change on of the demo puzzles or enter a new one in the format [[number, number, number, ...], [number, number, number, ...], [number, number, number, ...], ...] at the beginning of the file to provide the program with a puzzle to solve. The size of the puzzle is variable but if the side length is not a square number, the box sizes have to be specified manually. An empty square is described with 0. Choose the puzzle you want to solve at the bottom of the file when calling main and run the programm. It will then print out a possible solution for the board, if it was able to find one.
## How it works
The main function is called at the bottom of the file with a puzzle board as an input.
### main function
After calling main with a puzzle in the above described format the program first calculates the total number of squares and checks if the whole puzzle forms a square.

It then starts a while loop which steps through the puzzle square by square (left to right, top to bottom) until it has reached the end with a possible solution. The algorithm uses positive and negative numbers to differentiate between numbers that are part of the provided puzzle and others that are a possible solution.

It first looks if the value of the square is bigger than 0. If so, it is part of the puzzle and the loop will continue with the next square. Otherwise, if the square is 0 or smaller it is first decreased by 1. Then a while loop starts which can decrease the square's number further until the check_number function determines that the square fits into the grid according to Sudoku rules or until the last allowed number is reached (in a standard Sudoku game that would be a 9, so here respectively -9).

Then an if function checks if the square's number is a possible solution. If not, it is a dead end and the algorithm has to backtrack. It then sets the square to 0 and decreases 'i' until it reaches a square with a changeable number (a number smaller or equal to 0). Otherwise, if the number fits into the grid, it is written to the puzzle and 'i' increased by one, to continue the loop with the next square.

At the end of the loop there is a check if 'i' is smaller than 0. If that's the case, there is no solution for the puzzle and thus the algorithm backtracked further than 0. After finishing the loop successfully, all the numbers are converted to absolute values and the solution is printed. If the loop was terminated early this step is skipped.

### check_number function
The check_number function checks if a given number at a given position is a possible solution for a given puzzle according to Sudoku rules, otherwise returns 'False'. It does so by calling three seperate functions check_row, check_column and check_box. It takes a puzzle, a number and a tuple for the number's position as input.

### check_row function
This function checks if a given number is already present in the number's row and returns 'False' if so. Otherwise it returns 'True'. It does this by using list comprehension

### check_column function
This function checks if a given number is already present in the number's column and returns 'False' if so. Otherwise it returns 'True'. It does this by creating a list of all the numbers in one column.

### check_box function
This function checks if a given number is already present in the number's box and returns 'False' if so. It also does this by creating a list of all the numbers in one box. Because the box size can vary, the function takes the square root of the puzzle's side length as a default. If the boxes are not squares but 2x3 for example, this can be specified here.