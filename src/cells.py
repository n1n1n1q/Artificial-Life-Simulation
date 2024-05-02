"""
Map's cells
"""


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
        self.coordinates = coordinates
        self.colors = colors

    def infect(self, other: "Cell") -> None:
        """
        Class
        """
        pass


class Void(Cell):
    """
    Void cell
    """

    def __init__(self, coordinates, age=0) -> None:
        super().__init__(coordinates, age, 0, [])


class Water(Cell):
    """
    Water cell
    """

    pass


class Dirt(Cell):
    """
    Dirt cell
    """

    pass


class Grass(Cell):
    """
    Grass cell
    """

    pass


class Stone(Cell):
    """
    Stone cell
    """

    pass


class Sand(Cell):
    """
    Sand cell
    """

    pass
