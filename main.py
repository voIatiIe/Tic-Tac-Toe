'''TicTacGame module'''

import numpy as np
from config import TEMPLATE, GOBACK


class TicTacGame:
    '''TicTacGame class'''

    players = {0: {"mrk": "X", "name": "Player_1"}, 1: {"mrk": "O", "name": "Player_2"}}

    def __init__(self):
        self.field = "\n".join(TEMPLATE)
        self.values = np.full((3, 3), " ")
        self.cur_plr = 0
        self.endgame_msg = ""

    def redraw_board(self):
        '''Redraws game board to the console'''

        print(self.field.format(*self.values.ravel()))

    @staticmethod
    def clear_screen(rows):
        '''Clears previous rows lines'''

        if rows:
            print(GOBACK*rows)
            for _ in range(rows - 1):
                print(" "*70)
            print(GOBACK*rows)

    def start_game_loop(self):
        '''Game loop'''

        self.redraw_board()
        while True:
            i, j = self.ask()

            mrk = self.players[self.cur_plr]["mrk"]
            self.values[i, j] = mrk
            self.clear_screen(10)
            self.redraw_board()

            if self.check_endgame():
                print(self.endgame_msg)
                break

            self.cur_plr = not self.cur_plr

    def ask(self):
        '''Asks players to input indicies of cells and prints validation error'''

        msg = ""
        while True:
            raw_inp = input(f"{self.players[self.cur_plr]['name']}'s turn:   {msg}\n_ _\n{GOBACK}")

            try:
                respond = self.validate_input(raw_inp)
            except (ValueError, IndexError) as error:
                msg = str(error)
            else:
                msg = ""
                break

        return respond

    def validate_input(self, inp, rows=3):
        '''Validates input'''

        inp = inp.split(" ")

        if len(inp) != 2:
            self.clear_screen(rows)
            raise IndexError("There should be two indicies")
        try:
            i, j = map(int, inp)

            if not ((i in (0, 1, 2)) and (j in (0, 1, 2))):
                self.clear_screen(rows)
                raise IndexError("Cell index should be 0, 1 or 2")
        except ValueError as error:
            self.clear_screen(rows)
            raise ValueError("Cell index should be int") from error
        if self.values[i, j] != " ":
            self.clear_screen(rows)
            raise ValueError("Cell is busy")

        return i, j

    def check_endgame(self):
        '''Checks if one of the players won or game ended with draw'''

        mrk = self.players[self.cur_plr]['mrk']
        rng = list(range(3))
        diag_1, diag_2 = self.values[rng, rng], self.values[rng, rng[::-1]]

        for i in rng:
            row = self.values[i, :]
            line = self.values[:, i]

            if (row == mrk).all() or (line == mrk).all() or \
               (diag_1 == mrk).all() or (diag_2 == mrk).all():
                self.endgame_msg = f"Player {self.players[self.cur_plr]['name']} wins!"
                return 1

        if (self.values.ravel() != " ").all():
            self.endgame_msg = "Draw!"
            return 1

        self.endgame_msg = ""
        return 0


if __name__ == "__main__":
    t = TicTacGame()
    t.start_game_loop()
