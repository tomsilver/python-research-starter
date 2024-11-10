"""Data structures."""

from dataclasses import dataclass
from typing import Hashable, TypeAlias
import numpy as np

# Define some data structures for this example repository (to be changed).
State: TypeAlias = np.ndarray
Action: TypeAlias = np.ndarray
Goal: TypeAlias = State

class Controller:
    """A controller for the agent to interact with the environment."""

# Limb Repo Structs
LRState: TypeAlias = State
