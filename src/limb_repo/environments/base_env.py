"""Abstract Base Environment."""

import abc


class BaseEnv(abc.ABC):
    """An environment for the agent to interact with."""

    def __init__(self) -> None:
        pass

    # @abc.abstractmethod
    # def get_lr_state(self) -> LRState:
    #     """Get the state of the active and passive arm."""

    # @abc.abstractmethod
    # def update_state(self, state: LRState) -> None:
    #     """Teleports the active and passive arm to the desired state.

    #     *Does not step*.
    #     """

    # @abc.abstractmethod
    # def send_action(self, action: Action) -> None:
    #     """Send an action to the active arm.

    #     *Does not step*.
    #     """

    # @abc.abstractmethod
    # def step(self) -> None:
    #     """Step the environment."""

    # @abc.abstractmethod
    # def reset(self) -> None:
    #     """Reset the environment."""
