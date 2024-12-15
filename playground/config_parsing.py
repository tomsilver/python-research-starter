"""Testing config parsing."""
from dataclasses import dataclass

import omegaconf
from omegaconf import OmegaConf

from limb_repo.structs import Pose, State


@dataclass
class PyBulletConfig:
    """The configuration of the PyBullet environment."""

    active_pose: Pose
    active_config: State
    active_urdf: str
    passive_pose: Pose
    passive_config: State
    passive_urdf: str
    wheelchair_pose: Pose
    wheelchair_config: State
    wheelchair_urdf: str


def parse_config(path_to_yaml: str) -> omegaconf.DictConfig:
    """Parse the configuration file."""
    yaml_conf = OmegaConf.load(path_to_yaml)
    config = OmegaConf.structured(PyBulletConfig(**yaml_conf))
    return config
