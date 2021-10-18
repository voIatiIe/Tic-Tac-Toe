import unittest
import numpy as np

from main import TicTacGame


class ValidationTest(unittest.TestCase):
    def setUp(self):
        self.inputs = ["0 0", "3 1", "3", "1 ", "a a", "b", "1 1"]
        self.labels = [(0, 0),
                       "Cell index should be 0, 1 or 2",
                       "There should be two indicies",
                       "Cell index should be int",
                       "Cell index should be int",
                       "There should be two indicies",
                       "Cell is busy",]
        self.game = TicTacGame()
        self.game.values = np.full((3, 3), " ")
        self.game.values[1, 1] = "X"

    def test_result(self):
        for inp, lab in zip(self.inputs, self.labels):
            try:
                res = self.game.validate_input(inp, 0)
            except (ValueError, IndexError) as error:
                assert lab == str(error)
            else:
                assert lab == res

    def tearDown(self):
        pass


class CheckEndgameTest(unittest.TestCase):
    def setUp(self):
        self.inputs = [np.array([["X", " ", " "],
                                 [" ", "X", " "],
                                 [" ", " ", "X"]]),
                       np.array([[" ", "O", " "],
                                 [" ", "O", " "],
                                 [" ", "O", " "]]),
                       np.array([[" ", " ", " "],
                                 ["X", "X", "X"],
                                 [" ", " ", " "]]),
                       np.array([[" ", " ", "O"],
                                 [" ", "O", " "],
                                 ["O", " ", " "]]),
                       np.array([["O", "X", "X"],
                                 ["X", "O", "O"],
                                 ["O", "X", "X"]]),
                       np.array([["O", "X", " "],
                                 ["X", "O", "O"],
                                 ["O", "X", "X"]]),
                       np.array([["O", "X", "X"],
                                 ["X", "X", "O"],
                                 ["O", "X", "X"]]),]
        self.game = TicTacGame()
        self.labels = [1, 1, 1, 1, 1, 0, 1]
        self.players = [0, 1, 0, 1, 1, 1, 0]
        self.msgs   = [f"Player {self.game.players[0]['name']} wins!",
                       f"Player {self.game.players[1]['name']} wins!",
                       f"Player {self.game.players[0]['name']} wins!",
                       f"Player {self.game.players[1]['name']} wins!",
                       "Draw!",
                       "",
                       f"Player {self.game.players[0]['name']} wins!",]

    def test_result(self):
        for inp, lab, msg, plr in zip(self.inputs, self.labels, self.msgs, self.players):
            self.game.cur_plr = plr
            self.game.values = inp
            res = self.game.check_endgame()

            assert res == lab
            assert msg == self.game.endgame_msg


    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
