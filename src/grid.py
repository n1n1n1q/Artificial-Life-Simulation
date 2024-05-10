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
        self.seed = seed if seed else self.generate_seed()
        self.destinations = [0, 0]
        self.scaling_coeff = (n * m) / (60 * 60)
        if self.scaling_coeff < 0.8:
            self.scaling_coeff += (1 - self.scaling_coeff) / ((self._n + self._m) / 10)
        self.set_up()

    def __getitem__(self, i):
        return self._map[i]

    def generate_seed(self):
        """
        Generate a random seed string for the grid
        """
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
        self.n_rows, self.n_cols = self._n, self._m
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
            self._map[new[0]][new[1]].threshold_age *= self.scaling_coeff

    def biome_distribution(self):
        """
        Secondary biomes distribution
        """
        self.destinations[0] = 2
        stack = [Forest, Mountain, Swamp, Snowy]
        used = set()
        while stack:
            curr = stack.pop()((-1, -1))
            print(curr)
            while 1:
                new = (
                    random.randint(0, self.n_rows - 1),
                    random.randint(0, self.n_cols - 1),
                )
                if new in used or self._map[new[0]][new[1]].type not in curr.submissive:
                    continue
                if (
                    curr.type == "swamp"
                    and self._map[new[0]][new[1]].type == "water"
                    and not [
                        i
                        for i in self.get_neighbours(self._map[new[0]][new[1]])
                        if i.type != "water"
                    ]
                ):
                    continue
                curr.x, curr.y = new
                used.add(new)
                self._map[new[0]][new[1]] = curr
                self._map[new[0]][new[1]].threshold_age *= self.scaling_coeff
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

    def get_adjacent(self, cell: "Cell"):
        """
        Get adjecent cells of a given cell (neighbours and corners)
        """
        corners = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        res = [
            self._map[cell.x + i][cell.y + j]
            for i, j in corners
            if cell.x + i not in [-1, self.n_rows]
            and cell.y + j not in [-1, self.n_cols]
        ] + self.get_neighbours(cell)
        return res

    def large_texture(self, cell: "Cell"):
        """
        Determine is a large texture can be applied to a cell
        """
        adj = [(0, 1), (1, 0), (1, 1)]
        res = [
            self._map[cell.x + i][cell.y + j]
            for i, j in adj
            if cell.x + i != self.n_rows
            and cell.y + j != self.n_cols
            and self._map[cell.x + i][cell.y + j].type == cell.type

        ]
        return len(res) == 3

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
                if cell.type != "water" and cell.age <= cell.threshold_age:
                    flag = True
        if not flag:
            self.destinations[ind] = ind + 1

    def update_grid(self):
        """
        Walks through the grid and updates its' cells according to its rules
        """
        if self.destinations[1]:
            self._change_water()
            return True
        if self.destinations[0] == 1:
            self.biome_distribution()
        if not self.destinations[0]:
            self._update(0)
        else:
            self._update(1)
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

    def _change_water(self):
        """
        Calculate the height of water cells based on their distance to the nearest non-water cell
        """
        set_water = set()
        set_not_water = set()
        for row in self._map:
            for cell in row:
                if cell.type != 'water':
                    set_not_water.add((cell.x, cell.y))
        for row in self._map:
            for cell in row:
                if cell.type == 'water':
                    dis_set = set()
                    for el in set_not_water:
                        dis_set.add((abs(el[0] - cell.x)**2 + abs(el[1] - cell.y)**2)**(1/2))
                    set_water.add((cell, min(dis_set)))
                    cell.height = 5 - min(dis_set)
