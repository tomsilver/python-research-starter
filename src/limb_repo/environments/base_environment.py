import abc

from limb_repo.structs import *


@dataclass
class Config:
    """The configuration of the environment."""
    pass

@dataclass
class EnvState:
    """The state of the environment."""
    pass

class BaseEnvironment(abc.ABC):
    """An environment for the agent to interact with."""
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def get_state(self) -> State:
        """Get the state of the environment agent."""

    @abc.abstractmethod
    def update_state(self, state: State) -> None:
        """Update the state of the environment agent."""
