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
    ) -> None:
        self.x, self.y = coordinates
        self.age = age
        self.threshold_age = threshold_age
        self.type = type_
        self._color = color
        self.submissive = submissive
        self.height = 10
        self.changed = False
        self.active = False
        self.texture = False

    def _change_state(self, other: "Cell"):
        other.age = self.age + 1
        ran = random.random()
        if self.type != 'water':
            if ran < 0.2:
                other.height -= 1
            elif ran > 0.8:
                other.height += 1
        self.active = True
        other.active = True
        other.__class__ = self.__class__
        other._color = self._color
        other.threshold_age = self.threshold_age
        other.type = self.type
        other.submissive = self.submissive
        other.changed = True

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
        # if 1 - self.SUBTYPES[sub] >= random.random():
        #     return sub
        # return "regular"
    @property
    def color(self):
        '''Calculates the color of the cell based on its type and height'''
        if self.type == 'water':
            return self._color
        rgb = colors.hex2color(self._color)
        rgb = (min(max(rgb[0]+(self.height-10)/100, 0), 1), \
min(max(rgb[1]+(self.height-10)/100, 0), 1), min(max(rgb[2]+(self.height-10)/100, 0), 1))
        return colors.to_hex(rgb)

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
        super().__init__(coordinates, age, 500, "water", "#1A4480", ["void"])

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

    SUBTYPES = {"grassy": 0.95, "house": 0.05}

    def __init__(self, coordinates: tuple[int, int], age: int = 0) -> None:
        super().__init__(coordinates, age, 50, "plains", "#66C61C", ["water"])

    def infect(self, other: Cell, coeff: int = 0) -> None:
        """
        Plain cell's infect method
        Infects only water cells, with a 60% + {k} chance, where k = coeff / 200
        """
        if (
            other.type in self.submissive
            and random.random() + coeff**2 / 200 > 0.8
            and self.age <= self.threshold_age
        ) or (
            other.type == "desert"
            and random.random() + coeff**2 / 200 > 0.99
            and self.age <= self.threshold_age
        ):
            self._change_state(other)


class Desert(Cell):
    """
    Desert cell class
    A cell class that represents an area of desert type
    """

    SUBTYPES = {"cacti": 0.7, "wasteland": 0.295, "pyramid": 1}

    def __init__(self, coordinates: tuple[int, int], age: int = 0) -> None:
        super().__init__(coordinates, age, 35, "desert", "#f6d7b0", ["water"])

    def infect(self, other: Cell, coeff: int = 0) -> None:
        """
        Desert cell's infect method
        Infects only water cells, either with a 75% + {k} chance, where k = coeff / 120
        """
        if (
            other.type in self.submissive
            and random.random() + coeff**2 / 120 > 0.9
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
        super().__init__(coordinates, age, 15, "forest", "#44801a", ["plains"])

    def infect(self, other: Cell, coeff: int = 0) -> None:
        """
        Forest cell's infect method
        """
        if (
            other.type in self.submissive
            and (random.random() > 0.7 or coeff in range(0, 3))
            and self.age <= self.threshold_age
        ):
            print(coeff)
            self._change_state(other)


class Swamp(Cell):
    """
    Swamp cell class
    A cell class that represents an area of swamp type
    """

    SUBTYPES = {"swamp": 1}

    def __init__(self, coordinates: tuple[int, int], age: int = 0) -> None:
        super().__init__(
            coordinates, age, 10, "swamp", "#3e443c", ["forest", "plains", "water"]
        )

    def infect(self, other: Cell, coeff: int = 0) -> None:
        """
        Swamp's cell infect method
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

    def __init__(self, coordinates: tuple[int, int], age: int = 0) -> None:
        super().__init__(coordinates, age, 7, "snow", "#FFFFFF", ["forest", "plains"])
        self.prev_type = None

    def infect(self, other: Cell, coeff: int = 0) -> None:
        """
        Snowy cell's infect method
        """
        if (
            other.type in self.submissive
            and self.age <= self.threshold_age
            and (random.random() > 0.5 or coeff in range(1,3))
        ):
            tmp = other.type
            self._change_state(other)
            other.prev_type = tmp

    def get_subtype(self):
        """
        Get snowy cell's subtype
        """
        return self.prev_type if self.prev_type else "snowy"


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
