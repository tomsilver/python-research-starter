"""Testing config parsing."""

import omegaconf
from omegaconf import OmegaConf

from limb_repo.environments.pybullet_environment import PyBulletConfig


def parse_config(path_to_yaml: str) -> omegaconf.DictConfig:
    """Parse the configuration file."""
    config = omegaconf.DictConfig(OmegaConf.load(path_to_yaml))

    # to get around mypy "Keywords must be strings"
    # and "value after ** should be a mapping"
    config_dict = {str(key): value for key, value in dict(config).items()}

    config = OmegaConf.structured(PyBulletConfig(**config_dict))
    return config


if __name__ == "__main__":
    print(parse_config("assets/configs/test_env_config.yaml"))
