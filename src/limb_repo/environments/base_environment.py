"""Abstract Base Environment."""

import abc
from dataclasses import dataclass

from limb_repo.structs import LR_State


@dataclass
class EnvState:
    """The state of the environment."""


class BaseEnvironment(abc.ABC):
    """An environment for the agent to interact with."""

    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def get_state(self) -> LR_State:
        """Get the state of the environment agent."""

    @abc.abstractmethod
    def update_state(self, state: LR_State) -> None:
        """Update the state of the environment agent."""
