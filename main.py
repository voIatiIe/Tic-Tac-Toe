from config import TEMPLATE, GOBACK
import numpy as np


class TicTacGame:
    players = {0: {"mrk": "X", "name": "Player_1"}, 1: {"mrk": "O", "name": "Player_2"}}
    messages = {}

    def __init__(self):
        self.field = "\n".join(TEMPLATE)
        self.values = np.full((3, 3), " ")
        self.cur_plr = 0
        self.line_ctr = 0
        self.update_board()
        self.msg = ""

    def update_board(self):
        self.clear_screen()
        self.line_ctr = 10
        print(self.field.format(*self.values.ravel()))

    def clear_screen(self):
        if self.line_ctr:
            print(GOBACK*self.line_ctr)
            for _ in range(self.line_ctr - 1):
                print(" "*70)
            print(GOBACK*self.line_ctr)

    def start_game_loop(self):
        while True:
            i, j = self.ask()

            self.values[i, j] = self.players[self.cur_plr]["mrk"]
            self.update_board()

            if self.check_endgame():
                break

            self.cur_plr = not self.cur_plr

    def ask(self):
        raw_inp = input(f"{self.players[self.cur_plr]['name']}'s turn:   {self.msg}\n_ _\n{GOBACK}")
        self.msg = ""
        return self.validate_input(raw_inp)

    def validate_input(self, inp):
        inp = inp.split(" ")

        if len(inp) != 2:
            self.msg = "There should be two indicies"
            self.update_board()
            return self.ask()
        try:
            x, y = map(int, inp)

            if not ((x in (0, 1, 2)) and (y in (0, 1, 2))):
                self.msg = "Cell index should be 0, 1 or 2"
                self.update_board()
                return self.ask()
        except ValueError:
            self.msg = "Cell index should be int"
            self.update_board()
            return self.ask()
        if self.values[x, y] != " ":
            self.msg = "Cell is busy"
            self.update_board()
            return self.ask()

        return x, y

    def check_endgame(self):
        mrk = self.players[self.cur_plr]['mrk']
        rng = list(range(3))
        d1, d2 = self.values[rng, rng], self.values[rng, rng[::-1]]

        for i in rng:
            row = self.values[i, :]
            line = self.values[:, i]

            if (row == mrk).all() or (line == mrk).all():
                print(f"Player {self.players[self.cur_plr]['name']} wins!")

                return 1

        if (d1 == mrk).all() or (d2 == mrk).all():
            print(f"Player {self.players[self.cur_plr]['name']} wins!")

            return 1

        if (self.values.ravel() != " ").all():
            print(f"Draw!")

            return 1

        return 0


if __name__ == "__main__":
    t = TicTacGame()
    t.start_game_loop()