"""
Map's cells
"""

from map import Grid


class Cell:
    """
    Map's cell class
    """

    def __init__(
        self,
        coordinates: tuple[int, int],
        age: int = 0,
        threshold_age: int = 0,
        status: int = -1,
        colors: list[tuple] | None = None,
    ) -> None:
        self.age = age
        self.threshold_age = threshold_age
        self.priority = status
        self.x, self.y = coordinates
        self.colors = colors

    def infect(self, other: "Cell") -> None:
        """
        ...
        """
        raise NotImplementedError

    def get_positions(self, map_: "Grid", delta: int = 1):
        """
        Get cell's neighbours that can be infected
        """
        pos = []
        for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if self.x + i in [-1, map_.n_rows] or self.y + j in [-1, map_.n_cols]:
                continue
            if self.priority - map_[self.x + i][self.y + j].priority == delta:
                pos.append((self.x + i, self.y + j))
        return pos


class Void(Cell):
    """
    Void cell
    """

    def __init__(self, coordinates, age=0) -> None:
        super().__init__(coordinates, age, 0, [])

    def infect(self, other: Cell) -> None:
        """
        ...
        """
        return None


class Water(Cell):
    """
    Water cell
    """

    def __init__(self, coordinates: tuple[int, int], age: int = 0) -> None:
        super().__init__(coordinates, age, 30, 1)

    def infect(self, other: Cell) -> None:
        """
        TODO
        """
        return super().infect(other)


class Dirt(Cell):
    """
    Dirt cell
    """

    def __init__(self, coordinates: tuple[int, int], age: int = 0) -> None:
        super().__init__(coordinates, age, 40, 2)

    def infect(self, other: Cell) -> None:
        """
        TODO
        """
        return super().infect(other)


class Grass(Cell):
    """
    Grass cell
    """

    def __init__(self, coordinates: tuple[int, int], age: int = 0) -> None:
        super().__init__(coordinates, age, 70, 3)

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
        super().__init__(coordinates, age, 100, 4)

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
        super().__init__(coordinates, age, 130, 5)

    def infect(self, other: Cell) -> None:
        """
        TODO
        """
        return super().infect(other)
