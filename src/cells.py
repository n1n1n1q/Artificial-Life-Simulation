"""
Map's cells
"""

import random


class Cell:
    """
    Cell template class
    """

    def __init__(
        self,
        coordinates: tuple[int, int],
        age: int = 0,
        threshold_age: int = 0,
        status: int = -1,
        color: str | None = None,
    ) -> None:
        self.age = age
        self.threshold_age = threshold_age
        self.priority = status
        self.x, self.y = coordinates
        self.color = color
        self.height = 0

    def _change_state(self, other: "Cell"):
        other.__class__ = self.__class__
        other.color = self.color
        other.threshold_age = self.threshold_age

    def infect(self, other: "Cell") -> None:
        """
        Abstract method for other
        """
        raise NotImplementedError


class Void(Cell):
    """
    Void cell class
    An empty cell that is going to be consumed by water
    """

    def __init__(self, coordinates, age=0) -> None:
        super().__init__(coordinates, age, 0, [])

    def infect(self, other: Cell) -> None:
        """
        Infect method for void cells
        Returns nothing because Void can't infect any cell
        """
        return None


class Water(Cell):
    """
    Water cell class
    A cell class that represents a certain terrain filled with water
    """

    def __init__(self, coordinates: tuple[int, int], age: int = 0) -> None:
        super().__init__(coordinates, age, 30, 1, "#1A4480")

    def infect(self, other: Cell) -> None:
        """
        Water cell's infect method
        Infects only the Void ones with 100% chance
        """
        if self.priority - other.priority == 1 and self.age <= self.threshold_age:
            self._change_state(other)


class Dirt(Cell):
    """
    Dirt cell
    """

    def __init__(self, coordinates: tuple[int, int], age: int = 0) -> None:
        super().__init__(coordinates, age, 40, 2)

    def infect(self, other: Cell, coeff: int = 0) -> None:
        """
        Dirt cell's infect method
        Infects only water cells, with a certain chance
        """
        if (
            self.priority - other.priority == 1
            and random.random() + coeff**2 / 100 > 0.6
            and self.age <= self.threshold_age
        ):
            self._change_state(other)


class Grass(Cell):
    """
    Grass cell
    """

    def __init__(self, coordinates: tuple[int, int], age: int = 0) -> None:
        super().__init__(coordinates, age, 100, 3)

    def infect(self, other: Cell) -> None:
        """
        TODO
        """
        return super().infect(other)


class Stone(Cell):
    """
    Stone cell
    """

    def __init__(self, coordinates: tuple[int, int], age: int = 0) -> None:
        super().__init__(coordinates, age, 70, 3)

    def infect(self, other: Cell) -> None:
        """
        TODO
        """
        return super().infect(other)


class Sand(Cell):
    """
    Sand cell
    """

    def __init__(self, coordinates: tuple[int, int], age: int = 0) -> None:
        super().__init__(coordinates, age, 90, 3)

    def infect(self, other: Cell) -> None:
        """
        TODO
        """
        return super().infect(other)
