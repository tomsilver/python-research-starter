# pylint: disable=attribute-defined-outside-init
# mypy: disable-error-code="attr-defined"
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
class BodyState(State):
    """Single Body State.

    This is a subclass of np.ndarray, and allows access to kinematic
    states as properties.
    """

    n_dofs: int
    kinematics_slice: slice
    pos_slice: slice
    vel_slice: slice
    acc_slice: slice

    def __new__(cls, input_array: np.ndarray, n_dofs: int = 6) -> "BodyState":
        assert len(input_array) == 3 * n_dofs

        obj = np.asarray(input_array).view(cls)
        obj.n_dofs = n_dofs

        obj.kinematics_slice = slice(0, 3 * obj.n_dofs)
        obj.pos_slice = slice(0, obj.n_dofs)
        obj.vel_slice = slice(obj.n_dofs, 2 * obj.n_dofs)
        obj.acc_slice = slice(2 * obj.n_dofs, 3 * obj.n_dofs)

        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.n_dofs = getattr(obj, "n_dofs", None)

    @property
    def pos(self):
        """Get position."""
        return self[self.pos_slice]

    @property
    def vel(self):
        """Get velocity."""
        return self[self.vel_slice]

    @property
    def acc(self):
        """Get acceleration."""
        return self[self.acc_slice]


class LRState(State):
    """Limb Repositioning State.

    This is a subclass of np.ndarray, and allows access to active and
    passive kinematic states as properties.
    """

    def __new__(
        cls, input_array: np.ndarray, active_n_dofs: int = 6, passive_n_dofs: int = 6
    ) -> "LRState":
        assert len(input_array) == 3 * (active_n_dofs + passive_n_dofs)

        obj = np.asarray(input_array).view(cls)
        obj.active_n_dofs = active_n_dofs
        obj.passive_n_dofs = passive_n_dofs

        return obj

    def __init__(self):  # pylint: disable=super-init-not-called
        self.active_kinematics_slice = slice(0, 3 * self.active_n_dofs)
        self.active_pos_slice = slice(0, self.active_n_dofs)
        self.active_vel_slice = slice(self.active_n_dofs, 2 * self.active_n_dofs)
        self.active_acc_slice = slice(2 * self.active_n_dofs, 3 * self.active_n_dofs)

        self.passive_kinematics_slice = slice(
            3 * self.active_n_dofs, 3 * self.active_n_dofs + 3 * self.passive_n_dofs
        )
        self.passive_pos_slice = slice(
            3 * self.active_n_dofs, 3 * self.active_n_dofs + self.passive_n_dofs
        )
        self.passive_vel_slice = slice(
            3 * self.active_n_dofs + self.passive_n_dofs,
            3 * self.active_n_dofs + 2 * self.passive_n_dofs,
        )
        self.passive_acc_slice = slice(
            3 * self.active_n_dofs + 2 * self.passive_n_dofs,
            3 * self.active_n_dofs + 3 * self.passive_n_dofs,
        )

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.active_n_dofs = getattr(obj, "active_n_dofs", None)
        self.passive_n_dofs = getattr(obj, "passive_n_dofs", None)

    @property
    def active_kinematics(self):
        """Get active kinematics."""
        return self[self.active_kinematics_slice]

    @property
    def active_pos(self):
        """Get active position."""
        return self[self.active_pos_slice]

    @property
    def active_vel(self):
        """Get active velocity."""
        return self[self.active_vel_slice]

    @property
    def active_acc(self):
        """Get active acceleration."""
        return self[self.active_acc_slice]

    @property
    def passive_kinematics(self):
        """Get passive kinematics."""
        return self[self.passive_kinematics_slice]

    @property
    def passive_pos(self):
        """Get passive position."""
        return self[self.passive_pos_slice]

    @property
    def passive_vel(self):
        """Get passive velocity."""
        return self[self.passive_vel_slice]

    @property
    def passive_acc(self):
        """Get passive acceleration."""
        return self[self.passive_acc_slice]
