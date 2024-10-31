from field import Field

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
