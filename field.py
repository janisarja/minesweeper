import random
from tkinter import Button, DISABLED

FONT = "Arial"

ZERO_COLOR = "white"
MINE_COLOR = "red"
OPENED_COLOR = "light grey"
FLAGGED_COLOR = "orange"

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
            self.__ui.game_over(False, self.__grid_object)
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
