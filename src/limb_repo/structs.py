"""Data structures."""

from typing import TypeAlias

import numpy as np

# Define some data structures for this example repository (to be changed).
State: TypeAlias = np.ndarray
Action: TypeAlias = np.ndarray
Goal: TypeAlias = State
Pose :TypeAlias = np.ndarray

class Task:
    """An initial state and goal."""

    init: State
    goal: Goal


class Controller:
    """A controller for the agent to interact with the environment."""


# Limb Repo Structs
LRState: TypeAlias = State
