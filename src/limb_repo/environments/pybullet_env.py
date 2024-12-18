"""PyBullet environment for Limb Repositioning."""

from dataclasses import dataclass

import numpy as np
import omegaconf
import pybullet
import pybullet_utils.bullet_client as bc
from omegaconf import OmegaConf

from limb_repo.environments.base_env import BaseEnv


@dataclass
class PyBulletConfig:
    """Configuration for a PyBullet environment."""

    robot_ee_to_human_ee: np.ndarray
    use_gui: bool
    real_time_simulation: bool
    gravity: np.ndarray
    dt: float


class PyBulletEnv(BaseEnv):
    """Pybullet environment for Limb Repositioning."""

    def __init__(self, config: omegaconf.DictConfig):
        # super().__init__()
        # Create pybullet sim
        if config.use_gui:
            self.p = bc.BulletClient(
                connection_mode=pybullet.GUI, options="--width=1000 --height=1000"
            )
        else:
            self.p = bc.BulletClient(connection_mode=pybullet.DIRECT)

        self.p.setGravity(*config.gravity)
        self.p.setRealTimeSimulation(1 if config.real_time_simulation else 0)
        self.p.setTimeStep(config.dt)
        self.p.setPhysicsEngineParameter(
            constraintSolverType=self.p.CONSTRAINT_SOLVER_LCP_DANTZIG,
            globalCFM=0.000001,
        )

    @staticmethod
    def parse_config(path_to_yaml: str) -> omegaconf.DictConfig:
        """Parse a configuration file."""
        config = omegaconf.DictConfig(OmegaConf.load(path_to_yaml))
        OmegaConf.register_new_resolver("eval", eval, use_cache=False)

        # to get around mypy "Keywords must be strings"
        # and "value after ** should be a mapping"
        config_dict = {str(key): value for key, value in dict(config).items()}

        config = OmegaConf.structured(PyBulletConfig(**config_dict))

        return config
