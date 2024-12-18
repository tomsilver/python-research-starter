"""Test Limb Repo PyBullet Environment."""

import omegaconf

from limb_repo.environments.lr_pybullet_env import LRPyBulletEnv


def test_config_parsing():
    """Test if config parsing does not raise errors."""
    config_dict = LRPyBulletEnv.parse_config("assets/configs/test_env_config.yaml")

    assert isinstance(config_dict.pybullet_config, omegaconf.DictConfig)
