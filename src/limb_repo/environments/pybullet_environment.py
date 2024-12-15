"""PyBullet environment for Limb Repositioning."""
from dataclasses import dataclass

import numpy as np
import omegaconf
from omegaconf import OmegaConf

from limb_repo.environments.base_environment import BaseEnvironment
from limb_repo.structs import Pose


@dataclass
class PyBulletConfig:
    """The configuration of the PyBullet environment."""

    active_pose: Pose
    active_config: np.ndarray
    active_urdf: str
    passive_pose: Pose
    passive_config: np.ndarray
    passive_urdf: str
    wheelchair_pose: Pose
    wheelchair_config: np.ndarray
    wheelchair_urdf: str


class PyBulletEnvironment(BaseEnvironment):
    """Pybullet environment for Limb Repositioning."""

    def __init__(self, path_to_yaml: str):
        # super().__init__()
        self.config: omegaconf.DictConfig = self.parse_config(path_to_yaml)

    def parse_config(self, path_to_yaml: str) -> omegaconf.DictConfig:
        """Parse the configuration file."""
        yaml_conf = OmegaConf.load(path_to_yaml)
        config = OmegaConf.structured(PyBulletConfig(**yaml_conf))
        return config
