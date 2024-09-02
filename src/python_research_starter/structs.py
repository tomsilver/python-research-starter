"""Data structures."""

from dataclasses import dataclass
from typing import TypeAlias

import numpy as np
from numpy.typing import NDArray

# Define some data structures for this example repository (to be changed).
State: TypeAlias = NDArray[np.int8]
Action: TypeAlias = int
Goal: TypeAlias = str


@dataclass(frozen=True)
class Task:
    """An initial state and goal."""

    init: State
    goal: Goal
