"""
Map/grid class
"""

import random
import numpy as np

from cells import Cell, Void, Water, Plains, Desert, Forest, Mountain, Swamp, Snowy


class Grid:
    """
    Grid class
    """

    def __init__(self, n: int, m: int, seed: str | None = None) -> None:
        self.n_rows = n
        self.n_cols = m
        self._n = n
        self._m = m
        self.seed = seed if seed else self.__generate_seed()
        self.destinations = [0, 0]
        self.set_up()

    def __getitem__(self, i):
        return self._map[i]

    def __generate_seed(self):
        seed_chars = "1234567890abcdefghABCDEFGHQWERTYqwerty"
        seed = ""
        while len(seed) != 20:
            seed += random.choice(seed_chars)
        return seed

    def change_generation_size(self, rows, cols):
        """
        Change grid's size
        """
        self._n, self._m = rows, cols

    def set_up(self):
        """
        Set the map up
        """
        random.seed(self.seed)
        self._map = np.array(
            [[Void((i, j), 0) for j in range(self._m)] for i in range(self._n)]
        )
        used = set()
        stack = [Water, Plains, Desert]
        while stack:
            new = (
                random.randint(0, self.n_rows - 1),
                random.randint(0, self.n_cols - 1),
            )
            if new in used:
                continue
            used.add(new)
            self._map[new[0]][new[1]] = stack.pop()(new)

    def biome_distribution(self):
        """
        Secondary biomes distribution
        """
        self.destinations[0] = 2
        stack = [Forest, Mountain, Swamp, Snowy]
        used = set()
        while stack:
            curr = stack.pop()((-1, -1))
            while 1:
                new = (
                    random.randint(0, self.n_rows - 1),
                    random.randint(0, self.n_cols - 1),
                )
                if new in used or self._map[new[0]][new[1]].type not in curr.submissive:
                    continue
                curr.x, curr.y = new
                used.add(new)
                self._map[new[0]][new[1]] = curr
                break
    def count_coeff(self, cell: "Cell"):
        """
        Count the number of neighboring cells of the same type in square 3x3
        """
        counter = 0
        for neighbour in np.ravel(
            self._map[
                cell.x - 1 if cell.x >= 1 else 0 : cell.x + 2,
                cell.y - 1 if cell.y >= 1 else 0 : cell.y + 2,
            ]
        ):
            if type(neighbour) is type(cell):
                counter += 1
        return counter

    def get_neighbours(self, cell: "Cell"):
        """
        Get neighboring cells of a given cell from top, left, right and below
        """
        neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        res = [
            self._map[cell.x + i][cell.y + j]
            for i, j in neighbors
            if cell.x + i not in [-1, self.n_rows]
            and cell.y + j not in [-1, self.n_cols]
        ]
        return res

    def revert_changed(self, ind):
        """
        Revert changed to false
        """
        flag = False
        for row in self._map:
            for cell in row:
                if cell.changed:
                    cell.changed = False
                    flag = True
        if not flag:
            self.destinations[ind] = 1

    def update_grid(self):
        """
        Walks through the grid and updates its' cells according to its rules
        """
        if self.destinations[1]:
            return True
        if self.destinations[1] == 1:
            self.biome_distribution()
        if not self.destinations[0]:
            self._update(0)
            print("Updating 1")
        else:
            self._update(1)
            print(self.destinations)
        return False
    def _update(self, ind):
        for row in self._map:
            for cell in row:
                if cell.changed:
                    continue
                coeff = (
                    None
                    if cell.type in ["water", "void", "swamp"]
                    else self.count_coeff(cell)
                )
                for neighbour in self.get_neighbours(cell):
                    if not neighbour.changed and coeff is not None:
                        cell.infect(neighbour, coeff)
                    elif not neighbour.changed:
                        cell.infect(neighbour)
                if cell.active:
                    cell.age += 1
        self.revert_changed(ind)
