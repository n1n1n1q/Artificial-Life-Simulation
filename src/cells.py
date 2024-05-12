"""
Map's cells
"""

import random
from abc import ABC, abstractmethod
from matplotlib import colors


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
        probability: float = 0.3,
    ) -> None:
        self.x, self.y = coordinates
        self.age = age
        self.threshold_age = threshold_age
        self.type = type_
        self._color = color
        self.submissive = submissive
        self.probability = probability
        self.height = 10
        self.changed = False
        self.active = False
        self.texture = False

    def _change_state(self, other: "Cell"):
        other.age = self.age + 1
        ran = random.random()
        if self.type != "water":
            if ran < 0.2:
                other.height -= 1
            elif ran > 0.8:
                other.height += 1
        other.probability = self.probability
        self.active = True
        other.active = True
        other.__class__ = self.__class__
        other.threshold_age = self.threshold_age
        other.type = self.type
        other.submissive = self.submissive
        other.changed = True
        other.set_color(self._color)

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
        sub = random.choices(options, probabilities)[0]
        return sub

    def set_color(self, new):
        """
        Set cell's color
        """
        self._color = new

    @property
    def color(self):
        """
        Calculates the color of the cell based on its type and height
        """
        rgb = colors.hex2color(self._color)
        rgb = (
            min(max(rgb[0] + (self.height - 10) / 100, 0), 1),
            min(max(rgb[1] + (self.height - 10) / 100, 0), 1),
            min(max(rgb[2] + (self.height - 10) / 100, 0), 1),
        )
        return colors.to_hex(rgb)

    @property
    def age_coeff(self):
        """
        Returns age coefficient
        """
        return 1 - (self.age / self.threshold_age) if self.age > 3 else 0

    def __repr__(self):
        return f"{self.type} ({self.x}, {self.y})"


class Void(Cell):
    """
    Void cell class
    An empty cell that is going to be consumed by water
    """

    SUBTYPES = {"void", 1}

    def __init__(self, coordinates, age=0) -> None:
        super().__init__(coordinates, age, 30, "void", "#181a1f")

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

    SUBTYPES = {"wavy": 0.7, "ship": 0.3}

    def __init__(self, coordinates: tuple[int, int], age: int = 0) -> None:
        super().__init__(coordinates, age, 500, "water", "#1A4480", ["void"], 0.02)

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

    SUBTYPES = {"grassy": 0.75, "house": 0.05}

    def __init__(self, coordinates: tuple[int, int], age: int = 0) -> None:
        super().__init__(coordinates, age, 39, "plains", "#62bc2f", ["water"], 0.09)

    def infect(self, other: Cell, coeff: int = 0) -> None:
        """
        Plain cell's infect method
        Infects only water cells, with a certain chance + {k} + {age_coeff}, where k = N of
        the same type cells around the initial one squared divided by 500
        """
        if (
            other.type in self.submissive
            and random.random() + self.age_coeff / 2 + coeff**2 / 500 > 0.8
            and self.age <= self.threshold_age
        ) or (
            other.type == "desert"
            and random.random() > 0.95
            and self.age <= self.threshold_age
        ):
            self._change_state(other)


class Desert(Cell):
    """
    Desert cell class
    A cell class that represents an area of desert type
    """

    SUBTYPES = {"cacti": 0.6, "wasteland": 0.3, "pyramid": 0.1}

    def __init__(self, coordinates: tuple[int, int], age: int = 0) -> None:
        super().__init__(
            coordinates, age, 27, "desert", "#f6d7b0", ["water"], probability=0.1
        )

    def infect(self, other: Cell, coeff: int = 0) -> None:
        """
        Desert cell's infect method
        Infects only water cells, either with a ceratin chance + {k}, where k = coeff**2 / 120
        """
        if (
            other.type in self.submissive
            and random.random() + coeff**2 / 120 > 0.9
            and self.age <= self.threshold_age
        ) or (
            other.type == "plains"
            and random.random() > 0.95
            and self.age <= self.threshold_age
        ):
            self._change_state(other)


class Forest(Cell):
    """
    Forest cell class
    A cell class that represents an area of forest type
    """

    SUBTYPES = {"birch": 0.34, "oak": 0.33, "mixed": 0.23, "pine": 0.1}

    def __init__(self, coordinates: tuple[int, int], age: int = 0) -> None:
        super().__init__(coordinates, age, 15, "forest", "#5D9F59", ["plains"], 0.17)

    def infect(self, other: Cell, coeff: int = 0) -> None:
        """
        Forest cell's infect method
        Infects only plains cells with either a certain chance or if there are from 0 to 2 forest
        cells around the it
        """
        if (
            other.type in self.submissive
            and (random.random() > 0.7 or coeff in range(0, 3))
            and self.age <= self.threshold_age
        ):
            self._change_state(other)


class Swamp(Cell):
    """
    Swamp cell class
    A cell class that represents an area of swamp type
    """

    SUBTYPES = {"swamp": 1}

    def __init__(self, coordinates: tuple[int, int], age: int = 0) -> None:
        super().__init__(
            coordinates, age, 10, "swamp", "#555c45", ["forest", "plains", "water"], 0.4
        )

    def infect(self, other: Cell, coeff: int = 0) -> None:
        """
        Swamp's cell infect method
        Infects forest, plains and water cells with either a certain chance or if there are from
        1 to 3 swamp cells around it
        """
        if (
            other.type in self.submissive
            and (random.random() > 0.9 or coeff in range(1, 3))
            and self.age <= self.threshold_age
        ):
            self._change_state(other)


class Snowy(Cell):
    """
    Snowy cell class
    A cell that represents a snowy area
    """

    SUBTYPES = {"snowy": 0.5, "mountain": 0.5}

    def __init__(self, coordinates: tuple[int, int], age: int = 0) -> None:
        super().__init__(
            coordinates, age, 7, "snowy", "#ecfffd", ["forest", "mountain", "plains"], 0.11
        )

    def infect(self, other: Cell, coeff: int = 0) -> None:
        """
        Snowy cell's infect method
        Infects forest, mountain and plains cells with either a certain chance or if there are from
        1 to 3 swamp cells around it
        """
        if (
            other.type in self.submissive
            and self.age <= self.threshold_age
            and (random.random() > 0.5 or coeff in range(1, 3))
        ):
            self._change_state(other)


class Mountain(Cell):
    """
    Mountain cell class
    A cell class that represents an area of mountain type
    """

    SUBTYPES = {"peaky": 0.05, "steep": 0.95}

    def __init__(self, coordinates: tuple[int, int], age: int = 0) -> None:
        super().__init__(
            coordinates,
            age,
            7,
            "mountain",
            "#808080",
            ["plains"],
            0.17
        )

    def infect(self, other: Cell, coeff: int = 0) -> None:
        """
        Mountain cell's infect method
        """
        if (
            other.type in self.submissive
            and self.age <= self.threshold_age
            and (coeff in range(1, 3) or random.random() > 0.7)
        ):
            self._change_state(other)
