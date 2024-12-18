import numpy as np

from limb_repo.environments.lr_pybullet_env import LRPyBulletEnv
from limb_repo.structs import BodyState

parsed_config = LRPyBulletEnv.parse_config("assets/configs/test_env_config.yaml")

env = LRPyBulletEnv(config=parsed_config)

active_state = BodyState(np.concatenate([parsed_config.active_config, np.zeros(6 + 6)]))
passive_state = BodyState(
    np.concatenate([parsed_config.passive_config, np.zeros(6 + 6)])
)

env.set_body_state(env.active_id, active_state)
env.set_body_state(env.passive_id, passive_state)

input()
