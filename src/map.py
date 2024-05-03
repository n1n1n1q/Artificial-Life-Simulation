"""
Map/grid class
"""

from random import randint
import numpy as np
from cells import Void


class Grid:
    """
    Grid class
    """

    def __init__(self, n, m) -> None:
        self.n_rows = n
        self.n_cols = m
        self._map = np.array([
            [Void((i, j), 0) for j in range(self.n_cols)] for i in range(self.n_rows)
        ])
        self.set_up()

    def set_up(self):
        """
        Set the map up
        """
        used = set()
        arr = [Void]  # add other cell's states later
        while arr:
            new = (randint(0, self.n_rows), randint(0, self.n_cols))
            if new in used:
                continue
            used.add(new)
            self._map[new[0]][new[1]] = arr.pop()(new)

    def __getitem__(self, i):
        return self._map[i]
