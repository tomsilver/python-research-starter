import hydra
import omegaconf

from limb_repo.environments.base_environment import *
from limb_repo.structs import *


class PyBulletEnvironment(BaseEnvironment):
    """Pybullet environment for Limb Repositioning."""
    class PyBulletConfig(Config):
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
        
    def __init__(self):
        super().__init__()

    def parse_config(self, config_file: str) -> Config:
        """Parse the configuration file."""
        self.config = omegaconf.OmegaConf.load(config_file)

        self.config = hydra.compose(config_name=config_file)
        self.config = Config(**self.config)