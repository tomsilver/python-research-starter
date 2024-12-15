# pylint: disable=attribute-defined-outside-init
"""Data structures."""

from typing import TypeAlias

import numpy as np

# Define some data structures for this example repository (to be changed).
State: TypeAlias = np.ndarray
Action: TypeAlias = np.ndarray
Goal: TypeAlias = State
Pose: TypeAlias = np.ndarray


class Task:
    """An initial state and goal."""

    init: State
    goal: Goal


class Controller:
    """A controller for the agent to interact with the environment."""


# Limb Repo Structs
class LR_State(State):
    """Limb Repositioning State.

    This is a subclass of np.ndarray, and allows access to active and
    passive kinematic states as properties.
    """

    def __new__(
        cls, input_array: np.ndarray, active_n_dofs: int = 6, passive_n_dofs: int = 6
    ) -> "LR_State":
        assert len(input_array) == 3 * (active_n_dofs + passive_n_dofs)

        obj = np.asarray(input_array).view(cls)
        obj.active_n_dofs = active_n_dofs
        obj.passive_n_dofs = passive_n_dofs

        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.active_n_dofs = getattr(obj, "active_n_dofs", None)
        self.passive_n_dofs = getattr(obj, "passive_n_dofs", None)

    @property
    def active_kinematics(self):
        """Get active kinematics."""
        return self[: 3 * self.active_n_dofs]

    @property
    def active_pos(self):
        """Get active position."""
        return self[: self.active_n_dofs]

    @property
    def active_vel(self):
        """Get active velocity."""
        return self[self.active_n_dofs : 2 * self.active_n_dofs]

    @property
    def active_acc(self):
        """Get active acceleration."""
        return self[2 * self.active_n_dofs : 3 * self.active_n_dofs]

    @property
    def passive_kinematics(self):
        """Get passive kinematics."""
        return self[
            3 * self.active_n_dofs : 3 * self.active_n_dofs + 3 * self.passive_n_dofs
        ]

    @property
    def passive_pos(self):
        """Get passive position."""
        return self[
            3 * self.active_n_dofs : 3 * self.active_n_dofs + self.passive_n_dofs
        ]

    @property
    def passive_vel(self):
        """Get passive velocity."""
        return self[
            3 * self.active_n_dofs
            + self.passive_n_dofs : 3 * self.active_n_dofs
            + 2 * self.passive_n_dofs
        ]

    @property
    def passive_acc(self):
        """Get passive acceleration."""
        return self[
            3 * self.active_n_dofs
            + 2 * self.passive_n_dofs : 3 * self.active_n_dofs
            + 3 * self.passive_n_dofs
        ]
