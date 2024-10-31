"""
COMP.CS.100 Project 5

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
from gamegrid import GameGrid
from ui import UI


def main():
    grid_object = GameGrid()
    ui = UI(grid_object)
    ui.new_game(grid_object)


if __name__ == "__main__":
    main()
