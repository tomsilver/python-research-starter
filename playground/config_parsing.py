"""Testing config parsing."""

import omegaconf
from omegaconf import OmegaConf

from limb_repo.environments.lr_pybullet_env import LRPyBulletConfig


def parse_config(path_to_yaml: str) -> omegaconf.DictConfig:
    """Parse the configuration file."""
    config = omegaconf.DictConfig(OmegaConf.load(path_to_yaml))

    # to get around mypy "Keywords must be strings"
    # and "value after ** should be a mapping"
    config_dict = {str(key): value for key, value in dict(config).items()}

    config = OmegaConf.structured(LRPyBulletConfig(**config_dict))

    return config


if __name__ == "__main__":
    parsed_config = parse_config("assets/configs/test_env_config.yaml")
    print(parsed_config)
    print(parsed_config.sim_config)
