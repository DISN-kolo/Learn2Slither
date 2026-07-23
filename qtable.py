import numpy as np


class Qtable:
    def get_slice(self, state):
        if (state in self.table.keys()):
            return self.table[state]
        else:
            self.table[state] = np.array([0.0, 0.0, 0.0])
            return self.table[state]

    # state     |  left  forward  right
    # ==================================
    # (asd,qwe) |  -0.2      0.5    145
    # (qwe,qge) |   151      0.0    -12
    # (asd,a5)  |   0.0      0.9    1.7
    def __init__(self):
        self.table = {}
