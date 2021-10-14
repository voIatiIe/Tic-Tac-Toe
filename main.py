from config import TEMPLATE, GOBACK
import numpy as np


class TicTacGame:
    players = {0: {"mrk": "X", "name": "Player_1"}, 1: {"mrk": "O", "name": "Player_2"}}

    def __init__(self):
        self.field = "\n".join(TEMPLATE)
        self.values = np.full((3, 3), " ")
        self.cur_plr = 0
        self.line_ctr = 0
        self.update_board()
        self.msg = ""

    def update_board(self):
        self.clear_screen()
        print(self.field.format(*self.values.ravel()))

    def clear_screen(self):
        if self.line_ctr:
            print(GOBACK*self.line_ctr)
            for _ in range(self.line_ctr - 1):
                print(" "*70)
            print(GOBACK*self.line_ctr)

    def start_game_loop(self):
        while True:
            x, y = self.ask()

            self.values[x, y] = self.players[self.cur_plr]["mrk"]
            self.update_board()

            if self.check_win():
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
            self.line_ctr = 10
            self.update_board()
            return self.ask()
        try:
            x, y = map(int, inp)

            if not ((x in (0, 1, 2)) and (y in (0, 1, 2))):
                self.msg = "Cell index should be 0, 1 or 2"
                self.line_ctr = 10
                self.update_board()
                return self.ask()
        except ValueError:
            self.msg = "Cell index should be int"
            self.line_ctr = 10
            self.update_board()
            return self.ask()
        if self.values[x, y] != " ":
            self.msg = "Cell is busy"
            self.line_ctr = 10
            self.update_board()
            return self.ask()

        self.line_ctr = 10

        return x, y

    def check_win(self):
        for i in range(3):
            row = self.values[i, :]
            line = self.values[:, i]
            mrk = self.players[self.cur_plr]['mrk']

            if (row == mrk).all() or (line == mrk).all():
                print(f"Player {self.players[self.cur_plr]['name']} wins!")

                return 1

        rng = list(range(3))
        d1, d2 = self.values[rng, rng], self.values[rng, rng[::-1]]

        if (d1 == mrk).all() or (d2 == mrk).all():
            print(f"Player {self.players[self.cur_plr]['name']} wins!")

            return 1


t = TicTacGame()
t.start_game_loop()