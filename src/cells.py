"""
Map's cells
"""

import random
from abc import ABC, abstractmethod


class Cell(ABC):
    """
    Cell template class
    """
    SUBTYPES: dict
    def __init__(
        self,
        coordinates: tuple[int, int],
        age: int = 0,
        threshold_age: int = 0,
        type_: str | None = None,
        color: str | None = None,
        submissive: list[str] | None = None,
    ) -> None:
        self.x, self.y = coordinates
        self.age = age
        self.threshold_age = threshold_age
        self.type = type_
        self.color = color
        self.submissive = submissive
        self.height = 0

    def _change_state(self, other: "Cell"):
        other.__class__ = self.__class__
        other.color = self.color
        other.threshold_age = self.threshold_age
        other.type = self.type
        other.submissive = self.submissive

    @abstractmethod
    def infect(self, other: "Cell") -> None:
        """
        Abstract method for other
        """

    def get_subtype(self):
        """
        Get random subtype
        """
        options = list(self.SUBTYPES.keys())
        probabilities = list(self.SUBTYPES.values())
        return random.choices(options, probabilities)[0]

class Void(Cell):
    """
    Void cell class
    An empty cell that is going to be consumed by water
    """

    def __init__(self, coordinates, age=0) -> None:
        super().__init__(coordinates, age, "void", [], "#FFFFFF")

    def infect(self, other: Cell) -> None:
        """
        Infect method for void cells
        Returns nothing because Void can't infect any cell
        """
        return None

    

class Water(Cell):
    """
    Water cell class
    A cell class that represents a certain area filled with water
    """

    def __init__(self, coordinates: tuple[int, int], age: int = 0) -> None:
        super().__init__(coordinates, age, 30, "water", "#1A4480", ["void"])

    def infect(self, other: Cell) -> None:
        """
        Water cell's infect method
        Infects only the Void ones with 100% chance
        """
        if other.type in self.submissive and self.age <= self.threshold_age:
            self._change_state(other)


class Plains(Cell):
    """
    Plains cell class
    A cell class that represents an area of plains type
    """

    def __init__(self, coordinates: tuple[int, int], age: int = 0) -> None:
        super().__init__(coordinates, age, 50, "plains", "#66C61C", ["water"])

    def infect(self, other: Cell, coeff: int = 0) -> None:
        """
        Plain cell's infect method
        Infects only water cells, with a 60% + {k} chance, where k = coeff / 200
        """
        if (
            other.type in self.submissive
            and random.random() + coeff**2 / 200 > 0.6
            and self.age <= self.threshold_age
        ):
            self._change_state(other)


class Desert(Cell):
    """
    Desert cell class
    A cell class that represents an area of desert type
    """

    def __init__(self, coordinates: tuple[int, int], age: int = 0) -> None:
        super().__init__(coordinates, age, 50, "desert", "#f6d7b0", ["water"])

    def infect(self, other: Cell, coeff: int = 0) -> None:
        """
        Desert cell's infect method
        Infects only water cells, either with a 75% + {k} chance, where k = coeff / 120
        """
        if (
            other.type in self.submissive
            and random.random() + coeff**2 / 120 > 0.75
            and self.age <= self.threshold_age
        ):
            self._change_state(other)


class Forest(Cell):
    """
    Forest cell class
    A cell class that represents an area of forest type
    """

    def __init__(self, coordinates: tuple[int, int], age: int = 0) -> None:
        super().__init__(coordinates, age, 60, "forest", "#44801a", ["plains"])

    def infect(self, other: Cell, coeff: int = 0) -> None:
        """
        Forest cell's infect method
        """
        if other.type in self.submissive and (
            random.random() > 0.6 or coeff in range(3, 6)
        ):
            self._change_state(other)


class Swamp(Cell):
    """
    Swamp cell class
    A cell class that represents an area of swamp type
    """

    def __init__(self, coordinates, age) -> None:
        super().__init__(
            coordinates, age, 15, "swamp", "", ["forest", "plains", "water"]
        )

    def infect(self, other: Cell) -> None:
        """
        Swamp's cell infect method
        """
        if other.type in self.submissive and self.age <= self.threshold_age:
            self._change_state(other)


class Snowy(Cell):
    """
    Snowy cell class
    A cell that represents a snowy area
    """

    def __init__(self, coordinates: tuple[int, int], age: int = 0) -> None:
        super().__init__(
            coordinates, age, 20, "snow", "#FFFAFA", ["forest", "plains", "water"]
        )
        self.prev_type = None

    def infect(self, other: Cell, coeff: int = 0) -> None:
        """
        Snowy cell's infect method
        """
        if (
            other.type in self.submissive
            and self.age <= self.threshold_age
            and (random.random() > 0.5 or coeff > 3)
        ):
            tmp = other.type
            self._change_state(other)
            other.prev_type = tmp


class Mountain(Cell):
    """
    Mountain cell class
    A cell class that represents an area of mountain type
    """

    def __init__(self, coordinates: tuple[int, int], age: int = 0) -> None:
        super().__init__(
            coordinates,
            age,
            40,
            "mountain",
            "#808080",
            ["water", "desert", "plains", "forest"],
        )

    def infect(self, other: Cell, coeff: int = 0) -> None:
        """
        Mountain cell's infect method
        """
        if other.type in self.submissive and (
            coeff in range(3, 9) or random.random() > 0.8
        ):
            self._change_state(other)
