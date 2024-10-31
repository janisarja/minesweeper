from tkinter import *

VERY_EASY = 1
EASY = 10
NORMAL = 15
HARD = 22

DEFAULT_SIZE = "15x15"
DEFAULT_DIFFICULTY = "Normal"

DEFAULT_COLOR = "#F0F0F0"

WIN_MESSAGE = "You won!"
WIN_COLOR = "green"
LOSE_MESSAGE = "Game over"
LOSE_COLOR = "red"

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
                                     self.check_if_win(grid_object))
        self.__restart_button = Button(self.__mainwindow, text="Restart",
                                       command=lambda:
                                       self.new_game(grid_object))
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

    def game_over(self, win, grid_object):
        """
        Opens all fields and displays the result of the game. Called when mine is
        opened or Check-button is pressed.

        :param win: bool, True if won, False if lost
        :param ui: UI, the user interface of the game
        :param grid_object: GameGrid, the grid that the fields are stored in
        """
        grid_object.open_all_fields()
        if win:
            self.display_result(True)
        else:
            self.display_result(False)


    def check_if_win(self, grid_object):
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
                    self.game_over(False, grid_object)
                    return
            except IndexError:
                self.game_over(False, grid_object)
                return

        self.game_over(True, grid_object)


    def new_game(self, grid_object):
        """
        Resets the game grid and starts a new game with the chosen size and
        difficulty.

        :param ui: UI, the user interface of the game
        :param grid_object: GameGrid, the grid that the fields are stored in
        """
        #  Reset the game and the result.
        grid_object.reset()
        self.reset_result()

        #  Create new game.
        grid_height, grid_width = self.get_size()
        grid_object.generate_fields(grid_height, grid_width, self.get_difficulty(),
                                    self)
        self.display_grid(grid_object)
        self.display_widgets()
        self.get_mainwindow().geometry(f"{grid_width*21}x{grid_height*21+118}")
        self.get_mainwindow().mainloop()

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
