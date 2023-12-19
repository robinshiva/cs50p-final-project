import requests
import sys
import json
import tkinter as tk


SUDOKU_ENDPOINT = "https://sudoku-api.vercel.app/api/dosuku?query={newboard(limit:1){grids{value, solution, difficulty}}}"
DIFFICULTIES = ["Easy", "Medium", "Hard"]
USER_NUMBER_COLOR = "darkgrey"
WRONG_NUMBER_COLOR = "lightcoral"
WINNING_NUMBER_COLOR = "forestgreen"


class Game(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        # Debug puzzle
        self.puzzle = [
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

        # Create main window with new puzzle
        self.new_puzzle(None)
        self.config(padx=5, pady=5)

        # Set keyboard shortcuts for saving, loading and getting a new puzzle
        self.bind_all("1", self.save)
        self.bind_all("2", self.load)
        self.bind_all("3", self.new_puzzle)

    def new_puzzle(self, event):
        """Gets a new puzzle from the Sudoku api"""
        try:
            puzzle = requests.get(SUDOKU_ENDPOINT).json()
        except requests.exceptions.JSONDecodeError:
            print("Could not get a new board")
            sys.exit(1)
        self.puzzle_all = puzzle["newboard"]["grids"][0]
        self.puzzle = self.puzzle_all["value"]
        print("Difficulty:", self.puzzle_all["difficulty"])
        # print(self.puzzle_complete["solution"])

        self.title("Robindoku - Difficulty: " + self.puzzle_all["difficulty"])
        try:
            del self.board
        except AttributeError:
            pass
        finally:
            self.board = Board(self, self.puzzle)

    def save(self, event):
        numbers = []
        config = []
        for box in self.board.boxes:
            for square in box.squares:
                numbers.append(square.numbers)
                config.append(
                    {
                        "text": square.label.cget("text"),
                        "fg": square.label.cget("fg"),
                        "font": square.label.cget("font"),
                        "anchor": square.label.cget("anchor"),
                    }
                )
        data = {"puzzle": self.puzzle_all, "numbers": numbers, "config": config}
        with open("sudoku_save.json", "w") as file:
            json.dump(data, file)
        print("saved")

    def load(self, event):
        try:
            with open("sudoku_save.json") as file:
                data = json.load(file)
        except FileNotFoundError:
            print("Could not load from file")
        else:
            del self.board
            self.puzzle_all = data["puzzle"]
            self.puzzle = self.puzzle_all["value"]
            self.board = Board(self, self.puzzle)
            i = 0
            for box in self.board.boxes:
                for square in box.squares:
                    square.numbers = data["numbers"][i]
                    square.label.config(
                        text=data["config"][i]["text"],
                        fg=data["config"][i]["fg"],
                        font=data["config"][i]["font"],
                        anchor=data["config"][i]["anchor"],
                    )
                    i += 1
            print("loaded")

    # def get_new_puzzle(self, difficulty=""):
    #     """Requests a new board from sudoku api"""
    #     for _ in range(5):
    #         try:
    #             boards = requests.get(SUDOKU_ENDPOINT).json()
    #         except requests.exceptions.JSONDecodeError:
    #             break

    #         # Check if one of the returned boards is in the requested difficulty or if no difficulty is specified, return the first one immediately
    #         for board in boards["newboard"]["grids"]:
    #             if not difficulty:
    #                 return board
    #             elif board["difficulty"] == difficulty:
    #                 return board

    #     # If no correct board was returned after the specified number of attempts, exit
    #     print("Error getting a new board in requested difficulty at this time")
    #     sys.exit(1)


class Board:
    def __init__(self, parent, puzzle) -> None:
        nums = []
        self.parent = parent

        # Reorder the numbers, so that they can fill the squares one after the other
        for i in [0, 3, 6]:
            for j in [0, 3, 6]:
                for _ in range(3):
                    nums.append(puzzle[i][j : j + 3])
                    i += 1
                i -= 3

        # Put all numbers in one list and get rid of nested lists
        self.numbers = []
        for row in nums:
            for n in row:
                self.numbers.append(n)

        # Generate 9 boxes (each is a tk.Frame) and give them each a block of 9 numbers
        self.boxes = []
        for i in range(9):
            self.boxes.append(Box(self, self.numbers[9 * i : 9 + 9 * i]))
            self.boxes[-1].grid(row=int(i / 3), column=i % 3)


class Box(tk.Frame):
    def __init__(self, parent, numbers) -> None:
        super().__init__()
        self.parent = parent
        self.config(relief="sunken", borderwidth=1, pady=5, padx=5)

        # Generate 9 squares for each box
        self.squares = []
        for i in range(9):
            self.squares.append(Square(self, numbers[i]))
            self.squares[-1].grid(row=int(i / 3), column=i % 3)


class Square(tk.Frame):
    def __init__(self, parent, number) -> None:
        super().__init__(parent)
        # Each Square is a frame with a label to display the numbers
        self.config(width=50, height=50, relief="groove", borderwidth=1)
        self.pack_propagate(0)
        self.parent = parent

        # Create label inside the frame
        self.label = tk.Label(self)
        self.label.pack()
        self.numbers = []

        # Write hardcoded numbers
        if number != 0:
            self.label.config(
                font=("Menlo", 36),
                text=number,
            )
        # Put an empty, changeable label where the puzzle gives a 0
        else:
            self.label.config(
                font=("Menlo", 36),
                text="",
                fg=USER_NUMBER_COLOR,
                padx=4,
            )

            # Create a list to store the users numbers for the square

            # Bind left and right mouseclick to both the frame and the label to change or delete the number
            self.bind("<Button-1>", self.number_popup)
            self.label.bind("<Button-1>", self.number_popup)
            self.bind("<Button-2>", self.clear_square)
            self.label.bind("<Button-2>", self.clear_square)

    def number_popup(self, event):
        """Shows a popup to add a number to the square"""
        self.popup = tk.Menu()
        for i in range(1, 10):
            self.popup.add_command(
                label=i, command=lambda num=i: self.change_number(num)
            )
        try:
            self.popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup.grab_release()

    def change_number(self, number):
        """Writes a number to the square"""
        # If there is only one number in the square and it is selected again, make it a small number
        if len(self.numbers) == 1 and self.numbers[0] == number:
            string = ""
            for i in range(1, 10):
                if i in self.numbers:
                    string += str(i) + " "
                else:
                    string += "  "
                if i % 3 == 0:
                    string += "\n"
            self.label.config(
                text=string,
                fg=USER_NUMBER_COLOR,
                font=("Menlo", 12),
                anchor="nw",
            )

        # Otherwise continue with changing the number
        else:
            # Track all numbers of a square
            if number not in self.numbers:
                self.numbers.append(number)
            # Remove the number if it is selected again
            else:
                self.numbers.remove(number)

            # If there is only one number saved to the square (and it was selected for the first time), display it in normal size
            if len(self.numbers) == 1:
                self.label.config(
                    text=self.numbers[0],
                    fg=USER_NUMBER_COLOR,
                    font=("Menlo", 36),
                    anchor="c",
                )
                self.check_number()

            # If there is more than one number saved to the square, display all of them in small letters
            elif len(self.numbers) > 1:
                string = ""
                for i in range(1, 10):
                    if i in self.numbers:
                        string += str(i) + " "
                    else:
                        string += "  "
                    if i % 3 == 0:
                        string += "\n"
                self.label.config(
                    text=string,
                    fg=USER_NUMBER_COLOR,
                    font=("Menlo", 12),
                    anchor="nw",
                )

            # If the list of numbers is empty, clear the square
            else:
                self.clear_square(None)


    def clear_square(self, event):
        """Clears the square and deletes all numbers"""
        self.label.config(text="", fg=USER_NUMBER_COLOR)
        self.numbers = []

    def check_number(self):
        """Checks if the number is allowed according to Sudoku rules"""

        # Check if the number is already inside the squares parent box
        number = self.label.cget("text")
        square_numbers = []

        # Get all numbers of the square's parent box
        for child in self.parent.winfo_children():
            square_numbers.append(child.label.cget("text"))

        # Generate a list of all numbers
        all_numbers = []
        for box in self.parent.parent.boxes:
            for square in box.winfo_children():
                if len(str(square.label.cget("text"))) == 1:
                    all_numbers.append(square.label.cget("text"))
                else:
                    all_numbers.append("0")
        # Order the numbers row by row
        puzzle_now = []
        for j in [0, 27, 54]:
            for i in [0, 3, 6]:
                puzzle_now.append(
                    all_numbers[j : j + 27][i : i + 3]
                    + all_numbers[j : j + 27][i + 9 : i + 12]
                    + all_numbers[j : j + 27][i + 18 : i + 21]
                )
        # Get the index number of the box and square the input number is in
        box_number = str(self).split(".")[1].replace("!box", "")
        square_number = str(self).split(".")[2].replace("!square", "")
        if box_number == "":
            box_number = 1
        if square_number == "":
            square_number = 1
        square_number = int(square_number)
        box_number = int(box_number)

        # Get the number's row and column
        column, row = 0, 0
        if square_number > 6:
            row += 2
        elif square_number > 3:
            row += 1
        if box_number > 6:
            row += 6
        elif box_number > 3:
            row += 3
        if square_number in [2, 5, 8]:
            column += 1
        elif square_number in [3, 6, 9]:
            column += 2
        if box_number in [2, 5, 8]:
            column += 3
        elif box_number in [3, 6, 9]:
            column += 6

        # Get all other numbers of the number's row and column
        row_numbers = puzzle_now[row]
        column_numbers = []
        for row in puzzle_now:
            column_numbers.append(row[column])

        # If the number is in a box, row or column more than once (itself), color it differently
        if (
            square_numbers.count(number) > 1
            or column_numbers.count(number) > 1
            or row_numbers.count(number) > 1
        ):
            self.label.config(fg=WRONG_NUMBER_COLOR)

        # Check if the user has finished the puzzle
        # First check if the game has no empty squares left
        elif all_numbers.count("0") == 0:
            puzzle_finished = True
            # Check if no wrong numbers are present
            for box in self.parent.parent.boxes:
                for square in box.winfo_children():
                    if square.label.cget("fg") == WRONG_NUMBER_COLOR:
                        puzzle_finished = False
            # Turn all user numbers green to show that the puzzle is finished
            if puzzle_finished:
                for box in self.parent.parent.boxes:
                    for square in box.winfo_children():
                        if square.label.cget("fg") == USER_NUMBER_COLOR:
                            square.label.config(fg=WINNING_NUMBER_COLOR)


# Start an instance of the game
if __name__ == "__main__":
    game = Game()
    game.mainloop()
