"""
COMP.CS.100 Projekti 5
Opiskelijanumero: H300064
Tekijä:           Jani Sarja
Sähköposti:       jani.sarja@tuni.fi

Projektin on tarkoitus olla kehittynyt käyttöliittymä.

---Minesweeper---

How to play:

The game is played much like any other minesweeper. You can open a field by 
left-clicking on it and flag a field by right-clicking it. You flag the fields
you believe have a mine in them and open the fields you believe to be safe.
Opened fields show the number of mines in their surrounding fields. If you open
a field with zero mines surrounding them, all other connected zeros and their
surrounding fields are automatically opened.

The goal is to flag all the mines. The game ends when you either hit a mine, or
press the Check-button. Pressing the Check-button makes the program check if
all mines are flagged. This is where the program works a little different than
some other minesweepers. It doesn't care whether all fields are opened. You
just need to flag every mine (and only the mines). Once the game is over, the
program displays either "Game over" should you lose or "You win!" if you have
won.

You can start a new game by pressing the Restart-button. If you don't wish to
play anymore, you can close the program by pressing the Exit-button.

If you want to change the size of the grid or the difficulty (i.e. how many
mines are spawned in the grid), you can adjust those from the menus above the
grid. Once you have chosen the desired grid size and difficulty, you still need
to press the Restart-button for those changes to come into effect. Note that
the "Very Easy" -difficulty is meant for testing of the game mechanics and
doesn't pose a real challenge.
"""
from tkinter import *
import random

VERY_EASY = 1
EASY = 10
NORMAL = 15
HARD = 22

DEFAULT_SIZE = "15x15"
DEFAULT_DIFFICULTY = "Normal"

FONT = "Arial"

ZERO_COLOR = "white"
MINE_COLOR = "red"
OPENED_COLOR = "light grey"
FLAGGED_COLOR = "orange"
DEFAULT_COLOR = "#F0F0F0"

WIN_MESSAGE = "You won!"
WIN_COLOR = "green"
LOSE_MESSAGE = "Game over"
LOSE_COLOR = "red"


class GameGrid:
    """
    A GameGrid object is the grid in which the fields are situated.
    """
    def __init__(self):
        self.__grid = []

    def generate_fields(self, grid_height, grid_width, difficulty, ui):
        """
        Creates the fields and stores them in a list within a list. The fields
        can then be accessed through that list, where the list indices
        correspond to the rows and columns of the grid.

        :param grid_height: int, number of rows in the grid
        :param grid_width: int, number of columns in the grid
        :param difficulty: int, the probability (%) of a mine being spawned in
        a single grid
        :param ui: UI, the user interface object that the grid is displayed on
        """
        for row in range(grid_height):
            self.__grid.append([])
            for col in range(grid_width):
                self.__grid[row].append(Field(row, col, difficulty, ui, self))

        #  Once the fields have been created, calculate_mines() is called on
        #  each field in the grid.
        for row in range(grid_height):
            for col in range(grid_width):
                self.__grid[row][col].calculate_mines()

    def open_connected_zeros(self, row, col):
        """
        This is called when a zero is opened manually by clicking it. Checks if
        there are other zeros connected and opens them all.

        :param row: int, row index of the manually opened zero
        :param col: int, column index of the manually opened zero
        """
        #  connected_zeros includes the zeros that have been found, but have
        #  not yet been handled. At first this only includes the manually
        #  opened zero.
        connected_zeros = {str(row) + ' ' + str(col): self.__grid[row][col]}
        found = []
        processed = []

        #  This loop is executed until there are no more connected zeros to
        #  handle (connected_zeros is epmty). Using a finite for-loop instead
        #  of while to prevent an infinite loop in case something goes wrong.
        for _ in range(800):
            if not connected_zeros:
                return

            for field in connected_zeros:
                row = connected_zeros[field].get_row()
                col = connected_zeros[field].get_col()

                #  Checks if the adjacent fields are zeros and adds them to
                #  found if they are.
                for i in [[row - 1, col - 1], [row, col - 1],
                          [row + 1, col - 1], [row - 1, col],
                          [row + 1, col], [row - 1, col + 1],
                          [row, col + 1], [row + 1, col + 1]]:
                    try:
                        if self.__grid[i[0]][i[1]].get_mines() == 0 \
                                and i[0] in range(len(self.__grid)) \
                                and i[1] in range(len(self.__grid[i[0]])):
                            found.append(str(i[0]) + ' ' + str(i[1]))
                    except IndexError:
                        pass

                #  Opens the field and its adjacent fields, unless they are
                #  flagged.
                for j in [[row - 1, col - 1], [row, col - 1],
                          [row + 1, col - 1], [row - 1, col],
                          [row, col],
                          [row + 1, col], [row - 1, col + 1],
                          [row, col + 1], [row + 1, col + 1]]:
                    if j[0] in range(len(self.__grid)) \
                            and j[1] in range(
                            len(self.__grid[j[0]])) and not \
                            self.__grid[j[0]][j[1]].is_flagged():
                        self.__grid[j[0]][j[1]].open_field()

                processed.append(str(row) + ' ' + str(col))

            #  Adds found fields to connected_zeros.
            for field in found:
                row, col = field.split()
                connected_zeros[field] = self.__grid[int(row)][int(col)]

            #  Once a field is handled and opened it gets removed from
            #  connected_zeros.
            for field in processed:
                del connected_zeros[field]

    def open_all_fields(self):
        """
        Opens all fields in the grid. This is called when a game is over.
        """
        for row in range(len(self.__grid)):
            for col in range(len(self.__grid[row])):
                self.__grid[row][col].open_field()

    def reset(self):
        """
        Resets the grid by destroying the tkinter objects of all fields and
        making the grid into an epmty list again.
        """
        for row in range(len(self.__grid)):
            for col in range(len(self.__grid[row])):
                self.__grid[row][col].delete_field()

        self.__grid = []

    def get_grid(self):
        """
        :return: list, the list structure in which the fields are stored
        """
        return self.__grid


class Field:
    """
    A field can either have a mine or be empty. The empty fields, once opened,
    show the number of mines in the surrounding fields. Each field appears in
    the user interface as a button that opens the field once pressed.
    """
    def __init__(self, row, col, difficulty, ui, grid_object):
        """
        :param row: int, row index of the field
        :param col: int, column index of the field
        :param difficulty: int, the probability (%) of a mine being spawned in
        a single grid
        :param ui: UI, the user interface object that the grid is displayed on
        :param grid_object: GameGrid, the grid that the field is a part of
        """
        self.__row = row
        self.__col = col

        self.__ui = ui

        self.__flagged = False

        self.__grid_object = grid_object
        self.__game_grid = grid_object.get_grid()

        #  self.__mines is the number of mines surrounding a field, with the
        #  exception of 9 being a mine and -1 being an initial value that is
        #  later changed to the correct calculated value. Whether a field has a
        #  mine or not is determined by chance.
        if random.randint(0, 100) <= difficulty:
            self.__mines = 9
        else:
            self.__mines = -1

        self.__button = Button(self.__ui.get_mainwindow(),
                               command=self.open_on_press,
                               font=(FONT, 7), height=1)

    def calculate_mines(self):
        """
        Calculates the number of mines surrounding the field and stores that
        value in self.__mines, unless the field is a mine itself.
        """
        row = self.__row
        col = self.__col
        number_of_mines = 0
        for i in [[row - 1, col - 1], [row, col - 1], [row + 1, col - 1],
                  [row - 1, col], [row + 1, col],
                  [row - 1, col + 1], [row, col + 1], [row + 1, col + 1]]:
            try:
                if self.__game_grid[i[0]][i[1]].__mines == 9 \
                        and i[0] in range(len(self.__game_grid))\
                        and i[1] in range(len(self.__game_grid[i[0]])):
                    number_of_mines += 1
            except IndexError:
                pass

        #  Check if a mine is completely surrounded by mines. If so, it is
        #  converted into a non-mine field (8). Otherwise it would be
        #  impossible to tell if the middle field is a mine or not.
        if self.__mines == 9 and number_of_mines == 8:
            self.__mines = number_of_mines
        elif self.__mines != 9:
            self.__mines = number_of_mines

    def open_on_press(self):
        """
        This is called when the button of the field is pressed. If the field
        has a mine, the game is over. If the field has zero surrounding mines,
        all the connected zeros and their surrounding fields are opened. If the
        field is neither a mine or a zero, it is simply opened.
        """
        #  Opening a field also unflags it.
        self.__flagged = False

        if self.__mines == 9:
            game_over(False, self.__ui, self.__grid_object)
        elif self.__mines == 0:
            self.__grid_object.open_connected_zeros(self.__row, self.__col)
        else:
            self.open_field()

    def open_field(self):
        """
        Opens the field and changes the color and text appropriately based on
        whether it's a mine, a zero or something else. Once a field is opened,
        the button is disabled.
        """
        if self.__mines == 0:
            self.__button.configure(text=self.__mines, background=ZERO_COLOR)
        elif self.__mines == 9:
            self.__button.configure(background=MINE_COLOR)
        else:
            self.__button.configure(text=self.__mines, background=OPENED_COLOR)
        self.__button["state"] = DISABLED

    def flag(self, event):
        """
        Flags the field and changes the color, unless the field has already
        been opened.
        """
        if self.__button["state"] != DISABLED:
            event.widget.configure(background=FLAGGED_COLOR)
            self.__flagged = True

    def delete_field(self):
        """
        Destroys the field.
        """
        self.__button.destroy()

    def is_flagged(self):
        """
        :return: bool, True if field has been flagged, False if not
        """
        return self.__flagged

    def get_button(self):
        """
        :return: Button, the Button object of the field
        """
        return self.__button

    def get_mines(self):
        """
        :return: int, number of mines surrounding the field (or 9 if mine)
        """
        return self.__mines

    def get_row(self):
        """
        :return: int, the row index of the fields place on the grid
        """
        return self.__row

    def get_col(self):
        """
        :return: int, the column index of the fields place on the grid
        """
        return self.__col


class UI:
    """
    User interface on which the game is displayed.
    """
    def __init__(self, grid_object):
        """
        :param grid_object: GameGrid, the grid that the fields are stored in
        """
        self.__mainwindow = Tk()
        self.__mainwindow.title("Minesweeper")

        self.__grid_height = 15
        self.__grid_width = 15
        self.__difficulty_level = NORMAL

        #  Interface widgets
        self.__title = Label(self.__mainwindow, text="Minesweeper",
                             background="light blue", borderwidth=3,
                             relief="groove", font=("Arial", 14))
        self.__result_label = Label(self.__mainwindow, relief="raised")

        self.__size = StringVar()
        self.__size.set(DEFAULT_SIZE)
        self.__size_menu = OptionMenu(self.__mainwindow,
                                      self.__size,
                                      *["10x10", "15x15", "20x20", "20x40"],
                                      command=self.set_size)
        self.__difficulty = StringVar()
        self.__difficulty.set(DEFAULT_DIFFICULTY)
        self.__difficulty_menu = OptionMenu(self.__mainwindow,
                                            self.__difficulty,
                                            *["Very Easy", "Easy", "Normal",
                                              "Hard"],
                                            command=self.set_difficulty)

        self.__check_button = Button(self.__mainwindow, text="Check",
                                     command=lambda:
                                     check_if_win(self, grid_object))
        self.__restart_button = Button(self.__mainwindow, text="Restart",
                                       command=lambda:
                                       new_game(self, grid_object))
        self.__exit_button = Button(self.__mainwindow, text="Exit",
                                    command=self.stop)

    def display_widgets(self):
        """
        Displays the widgets on the interface.
        """
        self.__size_menu.grid(row=2, column=0, columnspan=4,
                              sticky=W)
        self.__difficulty_menu.grid(row=2, column=4, columnspan=6, sticky=W)

        self.__restart_button.grid(row=self.__grid_height+3,
                                   column=self.__grid_width*1//3,
                                   columnspan=self.__grid_width//3)
        self.__exit_button.grid(row=self.__grid_height+3,
                                column=self.__grid_width*2//3,
                                columnspan=self.__grid_width//3)
        self.__title.grid(row=0, column=0, columnspan=self.__grid_width,
                          sticky=NE+SW)
        self.__check_button.grid(row=self.__grid_height+3, column=0,
                                 columnspan=self.__grid_width//3)
        self.__result_label.grid(row=1, column=0,
                                 columnspan=self.__grid_width,
                                 sticky=NE+SW)

    def display_grid(self, grid_object):
        """
        Displays the fields in a grid.

        :param grid_object: GameGrid, the grid that the fields are stored in
        """
        #  Set the minimum size of the fields.
        self.__mainwindow.rowconfigure(0, minsize=40)

        for row in range(3, self.__grid_height + 3):
            self.__mainwindow.rowconfigure(row, minsize=21)
        for col in range(self.__grid_width):
            self.__mainwindow.columnconfigure(col, minsize=21)

        game_grid = grid_object.get_grid()

        for row in range(self.__grid_height):
            for col in range(self.__grid_width):
                field = game_grid[row][col]
                field.get_button().grid(row=row + 3, column=col,
                                        sticky=NE + SW)
                field.get_button().bind("<Button-2>",
                                        game_grid[row][col].flag)
                field.get_button().bind("<Button-3>",
                                        game_grid[row][col].flag)

    def set_size(self, size):
        """
        Sets the height and width of the game grid based on the selection in
        the menu.

        :param size:
        """
        size = self.__size.get()
        height, width = size.split("x")
        self.__grid_height = int(height)
        self.__grid_width = int(width)

    def set_difficulty(self, difficulty):
        """
        Sets the difficulty of the game based on the selection in
        the menu.

        :param difficulty:
        """
        difficulty = self.__difficulty.get()
        if difficulty == "Very Easy":
            self.__difficulty_level = VERY_EASY
        if difficulty == "Easy":
            self.__difficulty_level = EASY
        if difficulty == "Normal":
            self.__difficulty_level = NORMAL
        if difficulty == "Hard":
            self.__difficulty_level = HARD

    def display_result(self, win):
        """
        Displays the result of the game once the game has ended.

        :param win: bool, True if won, False if lost
        """
        if win:
            self.__result_label.configure(text=WIN_MESSAGE,
                                          background=WIN_COLOR)
        else:
            self.__result_label.configure(text=LOSE_MESSAGE,
                                          background=LOSE_COLOR)
        self.__mainwindow.mainloop()

    def reset_result(self):
        """
        Resets the result when a new game starts.
        """
        self.__result_label.configure(text="", background=DEFAULT_COLOR)

    def stop(self):
        """
        Ends the execution of the program.
        """
        self.__mainwindow.destroy()

    def get_mainwindow(self):
        """
        :return: Tk, the mainwindow object
        """
        return self.__mainwindow

    def get_difficulty(self):
        """
        :return: int, the difficulty
        """
        return self.__difficulty_level

    def get_size(self):
        """
        :return: int, the size
        """
        return self.__grid_height, self.__grid_width


def game_over(win, ui, grid_object):
    """
    Opens all fields and displays the result of the game. Called when mine is
    opened or Check-button is pressed.

    :param win: bool, True if won, False if lost
    :param ui: UI, the user interface of the game
    :param grid_object: GameGrid, the grid that the fields are stored in
    """
    grid_object.open_all_fields()
    if win:
        ui.display_result(True)
    else:
        ui.display_result(False)


def check_if_win(ui, grid_object):
    """
    Checks if every mine is flagged and every flagged field has a mine.

    :param ui: UI, the user interface of the game
    :param grid_object: GameGrid, the grid that the fields are stored in
    :return:
    """
    game_grid = grid_object.get_grid()

    flagged = []
    has_mine = []

    #  Find all flagged fields.
    for row in range(len(game_grid)):
        for col in range(len(game_grid[row])):
            if game_grid[row][col].is_flagged():
                flagged.append(str(row) + ' ' + str(col))

    #  Find all mines.
    for row in range(len(game_grid)):
        for col in range(len(game_grid[row])):
            if game_grid[row][col].get_mines() == 9:
                has_mine.append(str(row) + ' ' + str(col))

    #  Check if all flagged fields and fields with mines are the same fields.
    for i in range(len(has_mine)):
        try:
            if flagged[i] == has_mine[i]:
                pass
            else:
                game_over(False, ui, grid_object)
                return
        except IndexError:
            game_over(False, ui, grid_object)
            return

    game_over(True, ui, grid_object)


def new_game(ui, grid_object):
    """
    Resets the game grid and starts a new game with the chosen size and
    difficulty.

    :param ui: UI, the user interface of the game
    :param grid_object: GameGrid, the grid that the fields are stored in
    """
    #  Reset the game and the result.
    grid_object.reset()
    ui.reset_result()

    #  Create new game.
    grid_height, grid_width = ui.get_size()
    grid_object.generate_fields(grid_height, grid_width, ui.get_difficulty(),
                                ui)
    ui.display_grid(grid_object)
    ui.display_widgets()
    ui.get_mainwindow().geometry(f"{grid_width*21}x{grid_height*21+118}")
    ui.get_mainwindow().mainloop()


def main():
    grid_object = GameGrid()
    ui = UI(grid_object)
    new_game(ui, grid_object)


if __name__ == "__main__":
    main()
