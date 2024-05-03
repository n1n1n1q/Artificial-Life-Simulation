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
            new = (randint(0, self.n_rows-1), randint(0, self.n_cols-1))
            if new in used:
                continue
            used.add(new)
            self._map[new[0]][new[1]] = arr.pop()(new)

    def __getitem__(self, i):
        return self._map[i]

    def count_coeff(self, cell):
        """
        Count the number of neighboring cells of the same type in square 3x3
        """
        counter = 0
        for neighbour in np.ravel(self._map[cell.x-1 if cell.x >= 1 else 0:cell.x+2, cell.y-1 if \
cell.y >= 1 else 0:cell.y+2]):
            if type(neighbour) is type(cell):
                counter += 1
        return counter

    def get_neighbours(self, cell):
        """
        Get neighboring cells of a given cell from top, left, right and below
        """
        res = []
        if cell.x != 0:
            res.append(self._map[cell.x-1][cell.y])
        if cell.x != len(self._map)-1:
            res.append(self._map[cell.x+1][cell.y])
        if cell.y != 0:
            res.append(self._map[cell.x][cell.y-1])
        if cell.y != len(self._map[0])-1:
            res.append(self._map[cell.x][cell.y+1])
        return res

    def update_grid(self):
        """
        Walks through the grid and updates its' cells according to its rules
        """
        for row in self._map:
            for cell in row:
                if type(cell) in ["water", "void"]:
                    for neighbour in self.get_neighbours(cell):
                        cell.infect(neighbour)
                else:
                    coeff = self.count_coeff(cell)
                    for neighbour in self.get_neighbours(cell):
                        cell.infect(neighbour, coeff)
                cell.age += 1
