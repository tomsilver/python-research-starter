"""Testing numpy subclassing."""

import numpy as np
from typing import TypeAlias

class RealisticInfoArray(np.ndarray):
    def __new__(cls, input_array, info=None):
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        obj = np.asarray(input_array).view(cls)
        # add the new attribute to the created instance
        obj.info = info
        # Finally, we must return the newly created object:
        return obj


class RealisticInfoArrayWithArrayFinalize(np.ndarray):
    def __new__(cls, input_array, info=None):
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        obj = np.asarray(input_array).view(cls)
        # add the new attribute to the created instance
        obj.info = info
        # Finally, we must return the newly created object:
        return obj

    def __array_finalize__(self, obj):
        # see InfoArray.__array_finalize__ for comments
        if obj is None:
            return
        self.info = getattr(obj, "info", None)


State: TypeAlias = np.ndarray

class LR_State(State):
    """Limb Repositioning State.

    This is a subclass of np.ndarray, and allows access to active and
    passive kinematic states as properties.
    """

    def __new__(
        cls, input_array: np.ndarray, active_n_dofs: int = 6, passive_n_dofs: int = 6
    ):
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
        return self[: 3 * self.active_n_dofs]

    @property
    def active_pos(self):
        return self[: self.active_n_dofs]

    @property
    def active_vel(self):
        return self[self.active_n_dofs : 2 * self.active_n_dofs]

    @property
    def active_acc(self):
        return self[2 * self.active_n_dofs : 3 * self.active_n_dofs]

    @property
    def passive_kinematics(self):
        return self[
            3 * self.active_n_dofs : 3 * self.active_n_dofs + 3 * self.passive_n_dofs
        ]

    @property
    def passive_pos(self):
        return self[
            3 * self.active_n_dofs : 3 * self.active_n_dofs + self.passive_n_dofs
        ]

    @property
    def passive_vel(self):
        return self[
            3 * self.active_n_dofs
            + self.passive_n_dofs : 3 * self.active_n_dofs
            + 2 * self.passive_n_dofs
        ]

    @property
    def passive_acc(self):
        return self[
            3 * self.active_n_dofs
            + 2 * self.passive_n_dofs : 3 * self.active_n_dofs
            + 3 * self.passive_n_dofs
        ]


if __name__ == "__main__":
    # LR_State Testing
    state = LR_State(np.arange(36), active_n_dofs=6, passive_n_dofs=6)

    print(state.active_kinematics)
    print(state.active_pos * 10)
    print(type(state.active_pos))
    print(type(state.passive_acc + 3))
    print(type(state.passive_pos + np.array([1, 2, 3, 4, 5, 6])))

    '''
    [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17]
    [ 0 10 20 30 40 50]
    <class '__main__.LR_State'>
    <class '__main__.LR_State'>
    <class '__main__.LR_State'>
    '''


    # Subclassing Testing
    a = np.array([1, 2, 3])
    b = RealisticInfoArray(a, info="b")
    c = RealisticInfoArrayWithArrayFinalize(a, info="c")
    d = RealisticInfoArrayWithArrayFinalize(a, info="d")

    # raises error because no array finalize
    try:
        print(a + b, (a + b).info, type(a + b), type(b[1:]))
    except Exception as e:
        print(e)

    # [2 4 6] c c <class '__main__.RealisticInfoArrayWithArrayFinalize'> <class '__main__.RealisticInfoArrayWithArrayFinalize'>
    print(a + c, (a + c).info, (c + a).info, type(c[1:]), type(a + c))

    # prints c info
    print((c + d).info)
